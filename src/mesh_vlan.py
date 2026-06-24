import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class MeshVLANConfig:
    def __init__(self):
        self.config = {}

    def load_config(self, config_data):
        self.config = json.loads(config_data)

    def save_config(self):
        return json.dumps(self.config)

    def update_config(self, key, value):
        self.config[key] = value

class MeshVLANWebUI(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>Mesh VLAN Configurator</h1><a href="/config">Configure</a></body></html>')
        elif parsed_path.path == '/config':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'config': mesh_vlan_config.config}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_data = json.loads(post_data.decode())
        mesh_vlan_config.update_config(parsed_data['key'], parsed_data['value'])
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Configuration updated')

mesh_vlan_config = MeshVLANConfig()

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MeshVLANWebUI)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mesh VLAN Web UI')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on')
    args = parser.parse_args()
    run_server(args.port)
