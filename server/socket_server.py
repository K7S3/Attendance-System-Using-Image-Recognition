from recognize_face import recognize_face
from utils import mark_present, enroll_student
import socket
import numpy
import pickle
import sys
import _thread


class Server:
    '''
    Main server class for managing the server and attendance records
    '''
    
    def __init__(self, ip, port):
        ''' 
        creates a server using a ip address and a port
        :param ip:  {str} the ip on which the server will be hosted
        :param port: {int} the port which the server will be using
        '''
        self.ip = ip
        self.port = port
        self.sock = socket.socket()
        self.sock.bind((ip, port))
        self.sock.listen(1)

    def accept_connection(self):
        '''
        Accept the connection from a requesting client
        :return: Client Socket and Client address
        '''
        
        return self.sock.accept()

    def send_msg(self, csock, msg):
        '''
        Send text msg to a client
        :param csock: {socket} Client socket to which the message has to be sent
        :param msg: {str} the message that has to be sent
        :return: {str} confirmation/error message
        '''
        
        try:
            csock.send(msg.encode())
            return "Message Sent"
        except:
            return "Error occurred in sending message"

    def recv_msg(self, csock):
        '''
        Receives text msg from a client
        :param csock: {socket} Client socket from which the message has to be received
        :return: {str} The recieved message or an error message
        '''
        
        try:
            return csock.recv(1024).decode()
        except:
            return "Error occurred in receiving message"

    def recv_vector(self, csock):
        '''
        Receives a vector from the client
        :param csock: {socket} Client socket from which the vector has to be received
        :return: {np.ndarray / str} The recieved vector or an error message
        '''
        
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
        '''
        Close connection with the client
        :param csock: {socket} Client socket to be closed
        :param msg: {str} Client address
        :return: {str} confirmation/error message
        '''
        
        try:
            csock.close()
            return "Connection Closed with " + str(caddr)
        except:
            return "Error occurred in closing connection"


def start_procedure(server, csock, caddr):
    '''
    Function for starting the procedure to mark attendance, each procedure ran on a new thread
    :param csock: {socket} Client socket to be closed
    :param msg: {str} Client address
    :return: {none} when the control exits    
    '''

    msg = server.recv_msg(csock)
    print(str(caddr) + " -> "+ msg)
    out = server.send_msg(csock, "Connection complete")
    print(out)
    while True:
        out = server.recv_msg(csock)
        if out == "A":
            print("marking attendance for " + str(caddr))
            face_vec = server.recv_vector(csock)
            if isinstance(face_vec, str):
                out = server.send_msg(csock, face_vec)
            else: 
                roll_number = recognize_face(face_vec, 100)
                if roll_number is not None:
                    mark_present(roll_number)
                    out = server.send_msg(csock, roll_number + " marked present")
                else:
                    out = server.send_msg(csock, "Face not in server")
        
        elif out == "E":
            print("Enrolling student for " + str(caddr))
            roll_number = server.recv_msg(csock)
            face_vec = server.recv_vector(csock)
            if isinstance(face_vec, str):
                out = server.send_msg(csock, face_vec)
            else: 
                enroll_student(roll_number, face_vec)
                server.send_msg(csock, roll_number + " Enrolled and marked present for today")

        elif out == "X": 
            out = server.close_connection(csock, caddr)
            print(out)
            break
    return None
        

if __name__ == '__main__':
    server = Server("127.0.0.1", 8000)
    while True:
        try:
            csock, caddr = server.accept_connection()
            _thread.start_new_thread(start_procedure,(server, csock, caddr))
        except:
            sys.exit(0)