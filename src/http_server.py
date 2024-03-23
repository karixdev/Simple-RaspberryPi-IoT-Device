import socket
import json

class HttpRequestContext:
  def __init__(self):
    self.content = b''

  def write_json(self, code, body):
    response_body = json.dumps(body)
    self.content = b'HTTP/1.1 {} OK\r\nContent-Type: application/json\r\nContent-Length: {}\r\n\r\n{}'.format(code, len(response_body), response_body)

  def write_html(self, code, html):
    self.content = b'HTTP/1.1 {} OK\r\nContent-Type: text/html\r\nContent-Length: {}\r\n\r\n{}'.format(code, len(html), html)

class HttpServer:
  def __init__(self, host, port, ip):
    addr = socket.getaddrinfo(host, port)[0][-1]
    self.server = socket.socket()
    self.server.bind(addr)

    self.ip = ip

    self.routes = {}

  def listen(self):
    self.server.listen(1)
    while True:
      client_socket, addr = self.server.accept()
      
      try:
          request = client_socket.recv(1024)

          print(f'Client connected from: {addr}. Request: {request.decode('utf-8')}')

          split = request.decode('utf-8').split(' ')

          if len(split) < 2:
            client_socket.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')
            client_socket.close()

          self.route_request(client_socket, split)
      except Exception as e:
          print(e)
          client_socket.sendall(b'HTTP/1.1 500 Internal Server Error\r\n\r\n')
      finally:
          client_socket.close()

  def register_route(self, path, method, callback):
    self.routes[path] = {
      'path': path,
      'method': method,
      'callback': callback
    }

  def not_found(self, client_socket):
    client_socket.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n');

  def route_request(self, client_socket, request):
    method, url = request[0], request[1]
    print(f'Looking for route {method} {url}')

    if not self.ip in url:
      if not url in self.routes:
        print(f'Could not found route {method} {url}')
        self.not_found(client_socket)
        return

      route = self.routes[url]
      
      if not route['method'] == method:
        print(f'Could not found route {method} {url}')
        self.not_found(client_socket)
        return
      
      ctx = HttpRequestContext()
      route['callback'](ctx)

      client_socket.sendall(ctx.content)
      return
  
    prefix = f'/{self.ip}/'
    path = url[len(prefix):]

    route = self.routes[path]
    if not route['method'] == method:
      print(f'Could not found route {method} {url}')
      self.not_found(client_socket)
      return
    
    ctx = HttpRequestContext()
    route['callback'](ctx)

    client_socket.sendall(ctx.content)
    return