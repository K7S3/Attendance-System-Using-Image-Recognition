import unittest
import sys
import numpy as np
sys.path.append('../server/')
from recognize_face import recognize_face

class Testrecognize_face(unittest.TestCase):

    def test_recognize_face(self):
        vec1 = np.load('/home/pranay/college/8/swe/Attendance-System-Using-Image-Recognition/server/records/vectors/20161088.npy')
        out1 = recognize_face(vec1, 2)
        self.assertEqual(out1, "20161088")
        vec2 = np.arange(512)
        out2 = recognize_face(vec2, 2)
        self.assertEqual(out2, None)

if __name__ == "__main__":
    unittest.main()