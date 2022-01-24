from .utils.node import Node, Connection
from .utils.data import Packet

port = int(input("Choose port to run on: "))
nickname = input("Choose a nickname: ")
node = Node(port, nickname, {"name": "Shoji's net"})

node.start()

while True:
    command = input("Input a command> ")
    if command == 'PEERS':
        print(node.peers)
    elif command == 'CONN':
        host = input("Host: ")
        port = int(input("Port: "))
        conn = Connection(node.nickname, host, port)
        node.connect(conn)
    elif command == 'DATA':
        print(node.data)
    elif command == 'PING':
        packet = Packet({'type': 'ping'}, "Hello World")
        print(node.peers.keys())
        peer = input("Peer: ")
        node.send_packet(node.peers[peer].client, packet)
    elif command == 'EXIT':
        break
