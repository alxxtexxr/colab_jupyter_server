# Colab Jupyter Server
I created this because I want to use Colab/Kaggle as a remote Jupyter server, which I can connect to as a kernel for my local Jupyter notebook in VS Code.

## How to run
Just run this command:
```
colab_jupyter_server --ngrok_authtoken=<YOUR_NGROK_AUTHTOKEN>
```

### Command Parameters
- `ngrok_authtoken`

Get your ngrok authtoken here: https://dashboard.ngrok.com/get-started/your-authtoken

- `port`

The default port is 8888.

- `ngrok_down_url`

The default download URL is for ngrok on Linux (x86-64): https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz 

Find other download URLs here: https://ngrok.com/download