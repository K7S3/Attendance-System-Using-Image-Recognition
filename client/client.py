import socket
import numpy
import pickle

class Client():

    def __init__(self, server_ip, server_port):
        self.sock = socket.socket()
        self.sock.connect((server_ip, server_port))
    
    def send_msg(self, msg):
        try:
            self.sock.send(msg.encode())
            return "Message Sent"
        except:
            return "Error occurred in sending message"

    def recv_msg(self):
        try:
            return self.sock.recv(1024).decode()
        except:
            return "Error occurred in receiving message"


if __name__ == "__main__":
    client = Client("127.0.0.1", 8000)
    out = client.send_msg("Request to connect")
    msg = client.recv_msg()
    print(msg)    
# data= numpy.ones((1, 60))

# serialized_data = pickle.dumps(data, protocol=2)
# sock.sendall(serialized_data)
# sock.close()
# sock = socket.socket()
# data= numpy.zeros((1, 60))
# sock.connect(('localhost',8000))
# serialized_data = pickle.dumps(data, protocol=2)
# sock.sendall(serialized_data)
# sock.close()