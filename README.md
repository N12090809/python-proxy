# Proxy Browser

This project is a simple proxy server and browser interface that allows you to browse the internet through a proxy. It is intended to be run on Gitpod.

## Files

- `proxy_server.py`: Contains the Python code for the proxy server.
- `index.html`: Contains the HTML and JavaScript for the simple browser interface.
- `.gitpod.yml`: Configuration file for Gitpod.
- `.gitpod.Dockerfile`: Dockerfile for setting up the Gitpod environment.
- `requirements.txt`: Python dependencies.

## How to Set Up and Run

### Step 1: Open Gitpod

Go to [Gitpod](https://gitpod.io/) and log in using your GitHub account.

### Step 2: Create a New Workspace

Create a new workspace using the URL of this repository.

### Step 3: Run the Proxy Server

1. Open the terminal in Gitpod.
2. Run the following command to start the proxy server:
   ```sh
   python proxy_server.py
   ```

### Step 4: Expose the Port

Gitpod will prompt you to open port 8888 for external access. Accept this prompt.

### Step 5: Get the URL

Gitpod will provide a URL where your server is running. Replace `YOUR_GITPOD_URL` in `index.html` with this URL.

### Step 6: Access the HTML Interface

1. Open the `index.html` file using the provided Gitpod URL.
2. Enter a URL in the address bar and click "Go" to load the page through the proxy server.

Enjoy browsing the web through your proxy server!
