import socket

sock = socket.socket()
sock.connect(('127.0.0.1', 8000))
sock.send('hello, world!'.encode())

data = sock.recv(1024)
sock.close()

print(data)
