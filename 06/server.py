import socket

sock = socket.socket()
sock.bind((socket.gethostname(), 8000))
sock.listen(10)
conn, addr = sock.accept()
print('connected: ', addr)
while True:
    try:
        data = conn.recv(4096)
        if not data:
            break
    except Exception:
        continue
    conn.send(data.upper())
    print(data)
conn.close()
