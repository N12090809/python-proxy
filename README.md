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

### Step 3: Wait for Initialization

Gitpod will initialize your workspace based on the `.gitpod.yml` configuration. This includes setting up the environment and installing any dependencies listed in `requirements.txt`.

### Step 4: Verify the Proxy Server is Running

The `.gitpod.yml` file is configured to automatically run the proxy server with the command `python proxy_server.py`. The terminal should show the message: `Serving on port 8888`.

### Step 5: Expose the Port

Gitpod will prompt you to open port 8888 for external access. Accept this prompt to expose the port.

### Step 6: Get the URL

Gitpod will provide a URL where your server is running. This URL will be in the format `https://8888-your-workspace-id.ws-eu.gitpod.io/`.

### Step 7: Update the HTML Interface

1. Open the `index.html` file in the Gitpod editor.
2. Replace `YOUR_GITPOD_URL` with the URL provided by Gitpod. For example:
    ```html
    <script>
        function loadPage() {
            const url = document.getElementById('url').value;
            const proxyUrl = `/${encodeURIComponent(url)}`;
            document.getElementById('browser-frame').src = proxyUrl;
        }
    </script>
    ```

### Step 8: Preview the HTML Interface

1. In Gitpod, open the `index.html` file and click on the "Open in Browser" button to preview the file in a new browser tab.
2. You can now use the proxy browser interface. Enter a URL in the address bar and click "Go" to load the page through the proxy server.

Enjoy browsing the web through your proxy server!
