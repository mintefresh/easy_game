"""
This module provides UDP messages between client and server.
"""

from enum import Enum
import collections
import threading

from .errors import *


class Identifier(Enum):
    """
    Provides useful constants for this module.
    """
    # Sizes
    MSG_MAX_SIZE = 1024
    # Client messages
    # Action IDs
    KEEP_ALIVE = 0xFF01
    DISCONNECT = 0xFFFF
    CONNECT = 0xFF02
    REQUEST_INFO = 0xFF03

    # Server messages
    # Status IDs
    S_CONNECTED = 0x00
    S_DISCONNECTED = 0x01
    # Type IDs
    S_UPDATES = 0x00
    S_INFO = 0x01


class Client_Messenger:
    """
    Class facilitating communication from
    client's end.
    """
    def __init__(self, server=None, socket=None):
        """
        Generates a new messenger.
        """
        self.server = server
        self.socket = socket
        self.listener = None
        self.msg_buffer = collections.deque()
        self.msg_lock = threading.Lock()

    def connect(self, keep_alive=True):
        """
        Initiates a connection to server.
        Can keep alive if possible.
        """
        self.keep_alive = True
        if not self.server:
            raise EG_NetworkError("No server specified.")
        if not self.socket:
            # Generate socket
            self.socket = socket()
            self.socket.connect(self.server)

    def disconnect(self):
        """
        Disconnects from the server ASAP.
        """
        if not self.socket:
            raise EG_NetworkError("Not connected")

    def get_info(self):
        """
        Requests server info.
        """
        self.send(Server_Message(self.client_id,
                                 Identifier.REQUEST_INFO))

    def send(self, message):
        """
        Sends a message to the server.
        """
        if not self.socket:
            raise EG_NetworkError("Not connected")
        # TODO add to send queue
        self.socket.sendall(message.content)

    def listen(self):
        """
        Listens for and processes messages from the server.
        """
        if not self.socket:
            raise EG_NetworkError("Not connected")
        if self.listener.is_alive():
            raise EG_NetworkError("Listener already active")
        self._listening = True

        self.listener = threading.Thread(target=self._listen)
        self.listener.start()
        
    def _listen(self):
        """
        Thread method.
        """
        while self._listening:
            # Thread activity here
            msg = self.socket.recv(Identifier.MSG_MAX_SIZE)
            self.msg_lock.acquire()
            # MSG buffer locked
            self.msg_buffer.append(Server_Message(
                data = msg))

            self.msg_lock.release()

    def cancel_listen(self):
        """
        End listening thread.
        """
        if not self.listener.is_alive():
            return
        self._listening = False
        self.listener.join(3)
        if self.listener.is_alive():
            # Thread failed to end
            raise EG_NetworkError("Thread not responding")


class Message:
    """
    Abstract class representing any message, any direction.
    """
    def _upper16(self, value):
        """
        Get upper bits from 16-bit integer.
        """
        return value >> 8

    def _lower16(self, value):
        """
        Get lower bits from 16-bit integer.
        """
        return value & 0x00FF

    def _2byte_to_16(self, two_bytes):
        """
        Returns an integer from two bytes.
        """
        return (int(two_bytes[0]) << 8 +
                int(two_bytes[1]))

    def bytes(self):
        """
        Get content as bytes.
        """
        return bytes(self.content)


class Client_Message(Message):
    """
    Message from client to server.
    """
    def __init__(self, client_id=None, action_id=None, data=None):
        """
        TODO
        """
        if data:
            self.content = bytearray(data)
            return
        self.content = bytearray(4)
        self.client_id = client_id
        self.action_id = action_id

    @property
    def client_id(self):
        return _2byte_to_16(self.content[0:2])

    @client_id.setter
    def client_id(self, value):
        self.content[0] = self._upper16(value)
        self.content[1] = self._lower16(value)

    @property
    def action_id(self):
        return _2byte_to_16(self.content[2:4])

    @action_id.setter
    def action_id(self, value):
        self.content[2] = self._upper16(value)
        self.content[3] = self._lower16(value)


class Server_Message(Message):
    """
    Message from client to server.
    """
    def __init__(self, status=None, type=None, data=None):
        """
        TODO
        """
        if data:
            self.content = bytearray(data)
            return
        self.content = bytearray(2)
        self.status = status
        self.type = type

    @property
    def status(self):
        return int(self.content[0])

    @status.setter
    def status(self, value):
        self.content[0] = value

    @property
    def type(self):
        return int(self.content[1])

    @type.setter(self, value):
        self.content[1] = value
