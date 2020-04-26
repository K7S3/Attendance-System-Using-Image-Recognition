import unittest
import threading
import sys
import numpy as np
sys.path.append('../server/')
from socket_server import *

class TestClient(unittest.TestCase):

    def test_server_init(self):
        test_server = Server("127.0.0.1", 8000)
        self.assertEqual(test_server.ip , "127.0.0.1")
        self.assertEqual(test_server.port, 8000)
        self.assertEqual(test_server.sock.getsockname(), ("127.0.0.1", 8000)) 
        test_server.sock.shutdown(socket.SHUT_RDWR)
        test_server.sock.close()
        
    def run_server_for_test_1(self):
        test_server = Server("127.0.0.1", 8001)
        csock, caddr = test_server.accept_connection()
        self.assertEqual(csock.getpeername(), caddr)
        self.assertEqual(csock.getsockname(), ("127.0.0.1", 8001)) 
        csock.close()
        test_server.sock.shutdown(socket.SHUT_RDWR)
        test_server.sock.close()
        
    def test_accept_connection(self):
        server_thread = threading.Thread(target = self.run_server_for_test_1)
        server_thread.start()
        sock = socket.socket()
        sock.connect(("127.0.0.1", 8001))
        sock.close()
        server_thread.join()

    def run_server_for_test_2(self):
        test_server = Server("127.0.0.1", 8002)
        csock, caddr = test_server.accept_connection()
        out = test_server.recv_msg(csock)
        self.assertEqual(out, "test_msg")
        csock.close()
        test_server.sock.shutdown(socket.SHUT_RDWR)
        test_server.sock.close()
    
    def test_recv_msg(self):
        server_thread = threading.Thread(target = self.run_server_for_test_2)
        server_thread.start()
        sock = socket.socket()
        sock.connect(("127.0.0.1", 8002))
        sock.send("test_msg".encode())
        sock.close()
        server_thread.join()
    
    def run_server_for_test_3(self):
        test_server = Server("127.0.0.1", 8003)
        csock, caddr = test_server.accept_connection()
        out = test_server.send_msg(csock, "test_msg")
        self.assertEqual(out, "Message Sent")
        csock.close()
        test_server.sock.shutdown(socket.SHUT_RDWR)
        test_server.sock.close()

    def test_send_msg(self):
        server_thread = threading.Thread(target = self.run_server_for_test_3)
        server_thread.start()
        sock = socket.socket()
        sock.connect(("127.0.0.1", 8003))
        out = sock.recv(1024).decode()
        self.assertEqual(out , "test_msg")
        sock.close()
        server_thread.join()
    
    def run_server_for_test_4(self):
        test_server = Server("127.0.0.1", 8004)
        csock, caddr = test_server.accept_connection()
        out = test_server.recv_vector(csock)
        self.assertEqual(np.sum(out - np.zeros([512])), 0)
        csock.close()
        test_server.sock.shutdown(socket.SHUT_RDWR)
        test_server.sock.close()

    def test_recv_vec(self):
        server_thread = threading.Thread(target = self.run_server_for_test_4)
        server_thread.start()
        sock = socket.socket()
        sock.connect(("127.0.0.1", 8004))
        serialized_data = pickle.dumps(np.zeros([512]), protocol=2)
        sock.sendall(serialized_data)
        sock.close()
        server_thread.join()

if __name__ == '__main__':
    unittest.main()
    