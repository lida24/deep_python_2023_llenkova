import socket

sock = socket.socket()
sock.bind((socket.gethostname(), 8000))
sock.listen(1)
conn, addr = sock.accept()
print('connected: ', addr)
while True:
    data = conn.recv(1024)
    if not data:
        break
    conn.send(data.upper())
    print(data)
conn.close()
