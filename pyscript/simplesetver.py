import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

class Client(BaseHTTPRequestHandler):

	def do_POST(self):
		content_len = int(self.headers.get('content-length'))
		body = b'OK'
		self.send_response(200)
		self.send_header('Content-type', 'text/plain')
		self.send_header('Content-length', len(body))
		self.end_headers()
		self.wfile.write(body)
		requestBody = self.rfile.read(content_len).decode('ascii')
		print("length = " + str(content_len))
		print("body = " + requestBody)

server = HTTPServer(('', 80), Client)
server.serve_forever()
