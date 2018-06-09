"""
This module provides a CLI server implementation
for running an easy game.
"""
import sqlite3
import socket
import collections


class Server:
    """
    Class providing a backend server for an easy game.
    """
    def __init__(self,
                 network_type="local",
                 db_file = "~/.easy_game/game.db",
                 port=41444, # Random non-privileged
                 host="localhost",
                 logs="~/.easy_game/log",
                 resolution=50,
                 world_=None,
                 action_sz=1024):
        """
        Generates a new server instance.
        DB file:
            sqlite3 database file
        Network type:
            'local' -> Local (singleplayer) via Unix sockets
            'LAN'/'lan' -> Local (multiplayer) on LAN
            'internet' -> Networked multiplayer
        Resolution:
            Time interval (milliseconds) between server updates
            DATA received from clients independent of
                server updates
        Action size:
            Size in bytes of maximum datagram to accept from
                a client at a time. Recommend to keep default.
        """
        self.network_type = network_type
        self.db_file = db_file
        self.port = port
        self.host = host
        self.logs = logs
        self.resolution = resolution
        self.world = world_
        self.action_sz = action_sz

        # Initializations
        self.clients = collections.deque()
        self.actions = collections.deque()

    def prepare(self):
        """
        Ensure server is properly setup in order to begin operation.
        Connects to sqlite3 database.
        """
        # TODO check file paths
        pass

    def listen(self):
        """
        Establish udp listener for clients.
        Executed by a thread.
        """
        # Generate udp internet socket
        self.socket = socket.socket(family=socket.AF_INET,
                                    type=socket.SOCK_DGRAM,
                                    proto=0)

        # Bind to specified host and port
        self.socket.bind(self.host, self.port)

        while True:
            # Serve clients
            # Accept one datagram at a time, of max size
            # self.action_sz
            self.rec_buf, sender = self.socket.recvfrom(self.action_sz)


if __name__ == "__main__":
    pass
