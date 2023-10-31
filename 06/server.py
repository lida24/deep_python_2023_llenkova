import socket

sock = socket.socket()
sock.bind(('127.0.0.1', 8000))
sock.listen(1)
conn, addr = sock.accept()
print('connected: ', addr)
while True:
    data = conn.recv(1024)
    if not data:
        break
    conn.send(data.upper())
conn.close()
