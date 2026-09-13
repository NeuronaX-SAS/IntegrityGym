"""
IntegrityGym Dashboard Server
Serves the 4-screen interactive flight recorder and observer-effect product.
"""

import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8080
DIRECTORY = Path(__file__).resolve().parent


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)


def start_server(open_browser: bool = False):
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print("==================================================================")
        print("           INTEGRITYGYM PRODUCT DASHBOARD ONLINE")
        print("==================================================================")
        print(f"Server URL: {url}")
        print("Serving Screens: Experiment Controller, Live Swarm, Black Box, Observer Diff, Incident Forensics")
        print("Press Ctrl+C to terminate.")
        print("==================================================================")
        if open_browser:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")


if __name__ == "__main__":
    start_server(open_browser=False)
