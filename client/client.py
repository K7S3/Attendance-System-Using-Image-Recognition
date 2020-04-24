from get_face_vector import get_face_vector
import socket
import numpy
import pickle

class Client():
    '''Client class for individual cameras'''
    def __init__(self, server_ip, server_port):
        self.sock = socket.socket()
        self.sock.connect((server_ip, server_port))
    
    def send_msg(self, msg):
        '''Sends a text msg to the server'''
        try:
            self.sock.send(msg.encode())
            return "Message Sent"
        except:
            return "Error occurred in sending message"

    def recv_msg(self):
        '''receives a text msg from the server'''
        try:
            return self.sock.recv(1024).decode()
        except:
            return "Error occurred in receiving message"

    def send_vector(self, data):
        '''sends a vector to the server'''
        try: 
            serialized_data = pickle.dumps(data, protocol=2)
            self.sock.sendall(serialized_data)
            return "Vector Sent"
        except:
            return "Error occurred in sending the vector"
    
    def close_connection(self):
        '''ends the connection with the server'''
        try:
            self.sock.close()
            return "Connection Closed"
        except:
            return "Error occurred in closing connection" 


if __name__ == '__main__':
    client = Client("127.0.0.1", 8000)
    out = client.send_msg("Request to connect")
    msg = client.recv_msg()
    print("server -> " + msg)
    while True:
        inp = input("Ready? Y or N : ")
        out = client.send_msg(inp)
        if inp == "Y":
            face_vec = get_face_vector(.95)
            out = client.send_vector(face_vec)
            msg = client.recv_msg()
            print("server -> " + msg)
        else:
            print("Finished")
            out = client.close_connection()
            break