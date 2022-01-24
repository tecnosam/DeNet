from typing import List, Dict
from threading import Thread
from .utils import setup_server_socket, setup_client_socket
from .machine import Machine
from .connection import Connection
from .data import Data, Packet
from .default_processors import process_new_peers, process_ping

from .adt.sequence import Sequencer

import ipaddress


class Node:
    def __init__(self, port: int, nickname: str, schema: dict):
        self.peers: Dict[str, Machine] = dict()
        self.data: List[Data] = []

        self.processors = Sequencer()
        self.load_default_processors()

        self.nickname = nickname
        self.net_schema = schema

        self.__port = port
        self.__socket = setup_server_socket(port)
        self.__socket.listen()

        self.__listeners: Dict[Machine, Thread] = dict()

    def start(self):
        Thread(target=self.server_thread, daemon=True).start()

    def attach_processor(self, tag: str, processor):
        self.processors.enqueue(tag, processor)

    def load_default_processors(self):
        self.attach_processor('PROCESS NEW PEER', lambda packet: process_new_peers(self, packet))
        self.attach_processor('PROCESS PING', process_ping)

    def server_thread(self):
        # server thread to handle new peers
        print(f"Server Thread running on port {self.__port}")
        while True:
            client, address = self.__socket.accept()

            self.send_packet(client, Connection(self.nickname, '0', 0).to_packet())

            machine = Machine(address[0], address, client)

            conn_info = self.receive_packet(machine)

            machine.nickname = conn_info.body['nickname']

            self.add_machine(machine)

            print("New machine connected ", address[0])

    def connect(self, conn: Connection):
        client = setup_client_socket(conn.ip, conn.port)

        if client is not None:
            machine = Machine(conn.ip, (conn.ip, conn.port), client)

            conn_info = self.receive_packet(machine)  # receive conn info from peer

            machine.nickname = conn_info.body.get('nickname')

            self.send_packet(client, conn.to_packet())

            self.add_machine(machine)
            return machine

    @property
    def peer_list(self):
        # [print(p) for p in self.peers]
        return ([p.ip, p.port] for p in self.peers.values())

    @staticmethod
    def send_peer_list(client, peers: List[list]):
        # send list of peers to a client
        packet = Packet({'type': "peer-update"}, peers)
        Node.send_packet(client, packet)
        return packet

    @staticmethod
    def send_packet(client, packet: Packet):
        payload, size = packet.dump()
        client.send(size)  # send size of buffer
        client.send(payload)  # send packet
        return packet

    @staticmethod
    def receive_packet(machine: Machine) -> Packet:
        size = int.from_bytes(machine.client.recv(64), 'big')  # size of data

        packet = Packet.load(machine.client.recv(size))  # process data
        packet.header['source'] = machine.ip

        return packet

    def listen(self, machine: Machine):
        # function to listen to requests from peers
        while True:
            packet = self.receive_packet(machine)

            data = Data(self, machine, packet)

            # run preprocessor
            self.processors.execute(packet)

            self.data.append(data)

    def add_machine(self, machine: Machine):
        ip = ipaddress.ip_address(machine.ip)
        key = f"{machine.nickname}-{int(ip)}"
        self.peers[key] = machine  # store machine in peers list

        # Set up listener
        listener = Thread(target=self.listen, args=(machine,), daemon=True)
        self.__listeners[machine] = listener  # store listener thread for reference
        self.__listeners[machine].start()  # start listening for incoming packets
