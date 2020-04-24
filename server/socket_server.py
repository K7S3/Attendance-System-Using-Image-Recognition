from recognize_face import recognize_face
import socket
import numpy
import pickle
import select
import _thread

class Server:
    '''Main server class for handling and managing records'''
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket()
        self.sock.bind((ip, port))
        self.sock.listen(1)

    def accept_connection(self):
        '''Accept the connection from a requesting client'''
        return self.sock.accept()

    def send_msg(self, csock, msg):
        '''Send text msg to a client'''
        try:
            csock.send(msg.encode())
            return "Message Sent"
        except:
            return "Error occurred in sending message"

    def recv_msg(self, csock):
        '''Receives text msg from a client'''
        try:
            return csock.recv(1024).decode()
        except:
            return "Error occurred in receiving message"

    def recv_vector(self, csock):
        '''Receives face vector from the client'''
        try:
            block = csock.recv(1024)
            data = b'' + block
            while len(block) == 1024:
                block = csock.recv(1024)
                data += block
        
            return pickle.loads(data, encoding='bytes')
        except:
            return "Error occurred in receiving the vector"

    def close_connection(self, csock, caddr):
        '''Close connection with the client'''
        try:
            csock.close()
            return "Connection Closed with " + str(caddr)
        except:
            return "Error occurred in closing connection"


def start_procedure(server, csock, caddr):
    '''Function for starting the procedure to mark attendance'''
    msg = server.recv_msg(csock)
    print(str(caddr) + " -> "+ msg)
    out = server.send_msg(csock, "Connection complete")
    print(out)
    while True:
        out = server.recv_msg(csock)
        if out == "Y":
            face_vec = server.recv_vector(csock)
            if isinstance(face_vec, str):
                out = server.send_msg(csock, face_vec)
            else: 
                roll_number = recognize_face(face_vec, 100)
                if roll_number is not None:
                    out = server.send_msg(csock, roll_number + " marked present")
                else:
                    out = server.send_msg(csock, "Face not recognized")
        else: 
            out = server.close_connection(csock, caddr)
            print(out)
            break
    return None
        

if __name__ == '__main__':
    server = Server("127.0.0.1", 8000)
    while True:
        csock, caddr = server.accept_connection()
        _thread.start_new_thread(start_procedure,(server, csock, caddr))
        
        