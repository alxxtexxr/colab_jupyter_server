import os
import fire
import subprocess
import patoolib
import requests
import time
import signal
import sys
from jupyter_server.auth import passwd

def run_cmd(cmd):
    print(f">>> !{cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout)
    elif res.stderr:
        print(res.stderr)
    else:
        print("Something wrong!")
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

def cleanup():
    # Kill Jupyter, if it exists
    run_cmd('pkill -9 jupyter; echo "Jupyter is cleaned up"')
    
    # Kill ngrok, if it exists
    run_cmd('pkill -9 ngrok; echo "ngrok is cleaned up"')

def create_jupyter_server(
    ngrok_authtoken,

    # Get ngrok download URL here: https://ngrok.com/download
    ngrok_down_url = 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz', # Linux (x86-64)
    # ngrok_down_url = 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-arm64.zip', # Mac OS - Apple Silicon (ARM64)

    jupyter_password = None,
    port = 8888,
    wait_time = 3, # (Seconds)
):
    # Set up Jupyter Notebook
    run_cmd('jupyter notebook --JupyterApp.generate_config=True --JupyterApp.answer_yes=True')
    set_jupyter_password(jupyter_password)

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

    cleanup()

    try:
        # Run Jupyter Notebook in the background using '&' at the end
        run_cmd_bg(f'jupyter notebook --allow-root --no-browser --port={port}', show_output=False)
        
        # Run ngrok server
        run_cmd_bg(f'./ngrok http {port}', show_output=False)

        print(f"Waiting for Jupyter server URL... ({wait_time}s)")
        time.sleep(wait_time)

        r = requests.get('http://localhost:4040/api/tunnels')
        jupyter_server_url = r.json()['tunnels'][0]['public_url']
        print("Access Jupyter server URL on:", jupyter_server_url)

        signal.pause()
    except KeyboardInterrupt:
        print("Interrupted!")
        cleanup()
        sys.exit(0)

    except Exception as e:
        print(f"Something wrong! {e}")
        cleanup()
        sys.exit(1)

def main(): 
    fire.Fire(create_jupyter_server)

if __name__ == '__main__':
    main()