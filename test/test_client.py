import unittest
import threading
import sys
import numpy as np
sys.path.append('../client/')
from client import *

class TestClient(unittest.TestCase):

    def run_fake_server_for_test_1(self):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 8000))
        sock.listen(1)
        csock, caddr = sock.accept()
        self.assertEqual(csock.getpeername(), caddr)
        self.assertEqual(csock.getsockname(), ("127.0.0.1", 8000)) 
        csock.close()
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        
    def test_client_init(self):
        server_thread = threading.Thread(target = self.run_fake_server_for_test_1)
        server_thread.start()
        test_client = Client("127.0.0.1", 8000)
        self.assertEqual(test_client.sock.getpeername(), ("127.0.0.1", 8000))
        test_client.sock.close()
        server_thread.join()

    def run_fake_server_for_test_2(self):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 8001))
        sock.listen(1)
        csock, caddr = sock.accept()
        out = csock.recv(1024).decode()
        self.assertEqual(out, "test_msg")
        csock.close()
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        
    def test_send_msg(self):
        server_thread = threading.Thread(target = self.run_fake_server_for_test_2)
        server_thread.start()
        test_client = Client("127.0.0.1", 8001)
        out = test_client.send_msg("test_msg")
        self.assertEqual(out , "Message Sent")
        test_client.sock.close()
        server_thread.join()
    
    def run_fake_server_for_test_3(self):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 8002))
        sock.listen(1)
        csock, caddr = sock.accept()
        csock.send("test_msg".encode())
        csock.close()
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        
    def test_recv_msg(self):
        server_thread = threading.Thread(target = self.run_fake_server_for_test_3)
        server_thread.start()
        test_client = Client("127.0.0.1", 8002)
        out = test_client.recv_msg()
        self.assertEqual(out , "test_msg")
        test_client.sock.close()
        server_thread.join()
    
    def run_fake_server_for_test_4(self):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("127.0.0.1", 8003))
        sock.listen(1)
        csock, caddr = sock.accept()
        block = csock.recv(1024)
        data = b'' + block
        while len(block) == 1024:
            block = csock.recv(1024)
            data += block
        out = pickle.loads(data, encoding='bytes')
        self.assertEqual(np.sum(out - np.zeros([512])), 0)
        csock.close()
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

    def test_send_vec(self):
        server_thread = threading.Thread(target = self.run_fake_server_for_test_4)
        server_thread.start()
        test_client = Client("127.0.0.1", 8003)
        out = test_client.send_vector(np.zeros([512]))
        self.assertEqual(out , "Vector Sent")
        test_client.sock.close()
        server_thread.join()


if __name__ == '__main__':
    unittest.main()
    