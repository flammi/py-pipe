#!/usr/bin/python3

import socket
import threading
import queue
from time import sleep

class RecvError(Exception):
    pass

class RecvThread(threading.Thread):
    def __init__(self, socket):
        super(RecvThread, self).__init__()
        self.socket = socket

    def __recv_until_newline(self):
        buffer = b""
        while True:
            data = self.socket.recv(1)
            if not data:
                raise RecvError()
            if data == b"\n":
                break
            buffer += data
        return buffer

    def run(self):
        try:
            while True:
                filename = self.__recv_until_newline().decode("utf-8")
                size = int(self.__recv_until_newline())
                print("Receiving new file (name={0}, size={1})".format(filename, size))

                recvfile = open(filename, "wb")
                received = 0
                while received < size:
                    buf = self.socket.recv(size - received)
                    if not buf:
                        raise RecvError

                    received += len(buf)
                    recvfile.write(buf)

                    print("Got data (received={0})".format(received))
                recvfile.close()
                print("File transfer complete")

        except RecvError:
            pass
        print("Receiver Thread terminates...")

class ServerThread(threading.Thread):
    def __init__(self, port):
        super(ServerThread, self).__init__()
        self.port = port
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", self.port))
        s.listen(2)

        #Server forever
        while True:
            conn, addr = s.accept()
            print("New Connection from {0}".format(addr))

            #Start Send and Recv Thread
            receiver = RecvThread(conn)
            receiver.start()

class PipeServer:
    def __init__(self, port):
        """Start server in a seperate thread and return"""
        self.serverThread = ServerThread(port)
        self.serverThread.start()
    def connect(self, ip, port):
        """Connect to another instance of pipe and return a object that allows 
        sending files to it"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip,port))
        return PipeConnection(s)

class PipeConnection:
    """Connection to another pipe server"""
    def __init__(self, socket):
        self.socket = socket
    def sendFile(self, filename, buffer):
        print("Sending file...")
        self.socket.sendall(filename.encode("utf-8") + b"\n")
        import os
        buffer.seek(0, os.SEEK_END)
        size = buffer.tell()
        buffer.seek(0, os.SEEK_SET)
        print("Size: {0}".format(size))
        self.socket.sendall("{0}\n".format(size).encode("utf-8"))
        
        #Send file
        sendsize = 0
        chunksize = 1024
        while sendsize < size:
            buf = buffer.read(chunksize)
            self.socket.sendall(buf)
            sendsize += chunksize
        
    def close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

if __name__ == "__main__":
    PipeServer(5000)
