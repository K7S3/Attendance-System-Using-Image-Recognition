import unittest
import sys
import numpy as np
sys.path.append('../client/')
from get_face_vector import get_face_vector

class Testget_face_vector(unittest.TestCase):

    def test_get_face_vector(self):
        out = get_face_vector(0.95)
        self.assertEqual(out.shape[0], 512)

if __name__ == "__main__":
    unittest.main()