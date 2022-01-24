from .data import Packet
from .connection import Connection


def process_conn_info(node, packet: Packet):
    if packet.header.get('type') == 'conn-info':
        nickname = packet.body.get('nickname')
        machine = node.peers.get(nickname)
        if machine.ip != packet.body.get('ip'):
            #  todo do some network security stuff
            return packet

        node.send_packet(machine.client, packet)

    return packet


def process_new_peers(node, packet: Packet):
    # handle new peer connecting
    if packet.header.get('type') == 'peer-update':
        peers: list = packet.body

        for ip, port in peers:
            conn = Connection(ip, ip, port)
            node.connect(conn)  # todo: run this on a separate thread

        node.peers += peers

    return packet


def process_ping(packet: Packet):
    # Process A ping
    if packet.header.get('type') == 'ping':
        print(f"Ping from machine ", packet.header.get('source'))

    return packet
