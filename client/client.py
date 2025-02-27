from get_face_vector import get_face_vector
import socket
import numpy
import pickle

class Client():
    '''
    Client class for individual cameras
    '''
    
    def __init__(self, server_ip, server_port):
        ''' 
        creates a client, and connects it to the server ip address port
        :param ip:  {str} the ip on which the server is hosted
        :param port: {int} the port which the server is using
        '''

        self.sock = socket.socket()
        self.sock.connect((server_ip, server_port))
    
    def send_msg(self, msg):
        '''
        Sends a text msg to the server
        :param msg: {str} the message that has to be sent
        :return: {str} confirmation/error message
        '''

        try:
            self.sock.send(msg.encode())
            return "Message Sent"
        except:
            return "Error occurred in sending message"

    def recv_msg(self):
        '''
        receives a text msg from the server
        :return: {str} The recieved message or an error message
        '''
        
        try:
            return self.sock.recv(1024).decode()
        except:
            return "Error occurred in receiving message"

    def send_vector(self, data):
        '''
        sends a vector to the server
        :param: {np.ndarray} The vector to be sent
        :return: {str} confirmation/error message
        '''
        
        try: 
            serialized_data = pickle.dumps(data, protocol=2)
            self.sock.sendall(serialized_data)
            return "Vector Sent"
        except:
            return "Error occurred in sending the vector"
    
    def close_connection(self):
        '''
        ends the connection with the server
        :return: {str} confirmation/error messaage
        '''
        
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
        inp = input("What would you like to do? \n" + "Type E for enrollment, A for attendance X for exit: ")
        
        if inp == "A":
            out = client.send_msg(inp)
            face_vec = get_face_vector(.95)
            out = client.send_vector(face_vec)
            msg = client.recv_msg()
            print("server -> " + msg)
        
        elif inp == "E":
            out = client.send_msg(inp)
            roll_no = input("Enter Roll Number :")
            out = client.send_msg(roll_no)
            face_vec = get_face_vector(0.95)
            out = client.send_vector(face_vec)
            msg = client.recv_msg()
            print("server -> " + msg)

        elif inp == "X":
            out = client.send_msg(inp)
            print("Finished")
            out = client.close_connection()
            break
        else:
            print("Choose out of the given options\n")