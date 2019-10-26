import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Client(BaseHTTPRequestHandler):

	def do_POST(self):
		# 受け取ったデータ
		content_len = int(self.headers.get('content-length'))
		requestBody = self.rfile.read(content_len).decode('ascii')
		print(requestBody)
		requestJson = json.loads(requestBody)
		print(requestJson)
		print("length = " + str(content_len))
		body = b'OK' # 返す文字列
		self.send_response(200)
		self.send_header('Content-type', 'text/plain') # 返す文字列によって変える
		self.send_header('Content-length', len(body))
		self.end_headers()
		self.wfile.write(body)



server = HTTPServer(('', 86), Client)
server.serve_forever()
