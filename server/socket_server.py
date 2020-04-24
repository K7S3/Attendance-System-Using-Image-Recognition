import sys
import socket
import numpy
import pickle

class Server:
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket()
        self.sock.bind((ip, port))
        self.sock.listen(1)

    def accept_connection(self):
        return self.sock.accept()

    def send_msg(self, csock, msg):
        try:
            csock.send(msg.encode())
            return "Message Sent"
        except:
            return "Error occurred in sending message"

    def recv_msg(self, csock):
        try:
            return csock.recv(1024).decode()
        except:
            return "Error occurred in receiving message"



if __name__ == "__main__":
    server = Server("127.0.0.1", 8000)
    while True:
        csock, caddr = server.accept_connection()
        msg = server.recv_msg(csock)
        print(msg)
        out = server.send_msg(csock, "Connection complete")

        
        