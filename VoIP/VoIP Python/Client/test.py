import socket
soc = socket.socket()
soc.bind(('0.0.0.0', 23))
soc.listen(5)
client, addr = soc.accept()
while True:
    print client.recv(1024)