# Colab Jupyter Server
I created this library because I want to use Colab/Kaggle as a remote Jupyter server, which I can connect to as a kernel for my local Jupyter notebook in VS Code.

## How to run
Install the library first:
```
pip install -U colab-jupyter-server
```
Then, run this command:
```
colab_jupyter_server --ngrok_authtoken=<NGROK_AUTHTOKEN>
```

### Command Parameters
- `ngrok_authtoken`: Your ngrok authtoken. You can get it here: https://dashboard.ngrok.com/get-started/your-authtoken

- `ngrok_down_url`: The default download URL is for ngrok on Linux (x86-64) (https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz). Find other download URLs here: https://ngrok.com/download

<!-- - `jupyter_password`: The Jupyter server password. You will be asked for a password if not set. -->

- `port`: The default port is 8889. **Avoid using port 8888**, as it is already in use by the notebook you open in Colab/Kaggle.

- `wait_time`: The duration to wait for the Jupyter server info to be retrieved. The default is 10s. **A shorter wait time may result in failure to retrieve the Jupyter serrver token, returning an empty token.**