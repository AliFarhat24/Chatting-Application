import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 12000))

while True:
    peers = []
    while True:
        data, address = sock.recvfrom(128)

        print('connection from: {}'.format(address))
        peers.append(address)

        sock.sendto(b'ready', address)

        if len(peers) == 2:
            print('got 2 clients, sending details to each')
            break

    p1 = peers.pop()
    p1_addr, p1_port = p1
    p2 = peers.pop()
    p2_addr, p2_port = p2

    sock.sendto('{} {} {}'.format(p1_addr, p1_port, p2_port).encode(), p2)
    sock.sendto('{} {} {}'.format(p2_addr, p2_port, p1_port).encode(), p1)
