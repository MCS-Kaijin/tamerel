from socket import AF_INET, SOCK_STREAM, socket

# create server socket
sock = socket(AF_INET, SOCK_STREAM)

# bind socket to local address and listen for connections
sock.bind(('0.0.0.0', 80))
sock.listen(5)

while True:
    # accept a connection and get the request
    client, addr = sock.accept()
    request = client.recv(1024)

    # parse request (for now this'll just 1. look for
    # a get and tell them the site is under construction
    # 2. listen for the SHUTDOWNSERVER=1 argument
    req, pth, pro = request.decode().splitlines()[0].split(' ')
    args = request.decode().splitlines()[1:]
    if 'SHUTDOWNSERVER=1' in args:
        client.close()
        break
    if req == 'GET':
        client.send('''HTTP/1.0 200 OK\r
\r
<html>
    <head>
        <title>UNDER CONSTRUCTION</title>
        <meta charset="utf-8"/>
    </head>
    <body>
        Under Construction.
    </body>
</html>'''.encode('utf-8'))
    client.close()

sock.close()
