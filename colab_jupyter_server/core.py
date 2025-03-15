import os
import fire
import subprocess
import patoolib
import requests
import time
import signal
import sys
import json
from jupyter_server.auth import passwd

def run_cmd(cmd, input=None, show_output=True):
    print(f">>> !{cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, input=input)
    if show_output:
        if res.stdout:
            print(res.stdout)
        elif res.stderr:
            print(res.stderr)
        else:
            print("Something wrong!")
            print()
    else:
        print()

def run_cmd_bg(cmd, show_output=True):
    print(f">>> !{cmd}")
    subprocess.Popen(cmd, shell=True, text=True, 
                     stdout=(None if show_output else subprocess.DEVNULL), 
                     stderr=(None if show_output else subprocess.DEVNULL))
    if not show_output:
        print()

def set_jupyter_password(jupyter_password):
    if jupyter_password:
        passwd(str(jupyter_password))
    else:
        cmd = 'jupyter notebook password'
        print(f">>> !{cmd}")
        process = subprocess.Popen(cmd, shell=True, text=True, 
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if out:
            print(out)
        elif err:
            print(err)
        else:
            print("Something wrong!")
            print()

def cleanup(port):
    # Kill Jupyter, if it exists
    run_cmd(f'lsof -ti :{port} | xargs kill -9; echo "Jupyter is cleaned up"')
    
    # Kill ngrok, if it exists
    run_cmd('pkill -9 ngrok; echo "ngrok is cleaned up"')

def get_jupyter_server_url(port):
    r = requests.get('http://localhost:4040/api/tunnels')
    url = r.json()['tunnels'][0]['public_url']

    res = subprocess.run('jupyter notebook list --jsonlist', shell=True, capture_output=True, text=True)
    out = res.stdout
    notebook_list = json.loads(out)
    token = next((nb['token'] for nb in notebook_list if nb['port'] == port), None)

    return f'{url}?token={token}'

def create_jupyter_server(
    ngrok_authtoken,

    # Get ngrok download URL here: https://ngrok.com/download
    ngrok_down_url = 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz', # Linux (x86-64)
    # ngrok_down_url = 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-arm64.zip', # Mac OS - Apple Silicon (ARM64)

    domain = None,
    password = None,
    # jupyter_password = None,
    port = 8889,
    wait_time = 10, # (Seconds)
):
    # Set up Jupyter Notebook
    run_cmd('jupyter notebook --generate-config', input='y\n')
    run_cmd('echo "c.NotebookApp.allow_remote_access = True" >> ~/.jupyter/jupyter_notebook_config.py', show_output=False)
    # run_cmd('echo "c.NotebookApp.open_browser = False" >> ~/.jupyter/jupyter_notebook_config.py', show_output=False)
    # set_jupyter_password(jupyter_password)

    if not os.path.exists('ngrok'):
        # Download ngrok
        run_cmd(f'wget {ngrok_down_url}')

        # Extract ngrok compressed file
        ngrok_file_name = ngrok_down_url.split('/')[-1]
        print(f">>> patoolib.extract_archive('{ngrok_file_name}', outdir='.')")
        patoolib.extract_archive(ngrok_file_name, outdir='.')
        print()
    else:
        print("ngrok already exists, no need to download")
        print()

    # Authenticate ngrok agent
    run_cmd(f'./ngrok config add-authtoken {ngrok_authtoken}')

    cleanup(port)

    try:
        # Run Jupyter Notebook in the background using '&' at the end
        password = f' --IdentityProvider.token="{password}" --ServerApp.password="{password}" ' if password != None else ' '
        run_cmd_bg(f'jupyter notebook --allow-root --no-browser --port={port}{password}', show_output=False)
        
        # Run ngrok server
        domain = f' --url="{domain}" ' if domain else ' '
        run_cmd_bg(f'./ngrok http{domain}{port}', show_output=False)

        print(f"Waiting for Jupyter server URL... ({wait_time}s)")
        time.sleep(wait_time)

        url = get_jupyter_server_url(port)
        print("Jupyter server URL:")
        print(url)

        signal.pause()
    except KeyboardInterrupt:
        print("Interrupted!")
        cleanup(port)
        sys.exit(0)

    except Exception as e:
        print(f"Something wrong! {e}")
        cleanup(port)
        sys.exit(1)

def main(): 
    fire.Fire(create_jupyter_server)

if __name__ == '__main__':
    main()
