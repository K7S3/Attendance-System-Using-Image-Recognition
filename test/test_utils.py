import unittest
import sys
import os
import numpy as np
sys.path.append('../server/')
from utils import mark_present, enroll_student, add_facevec_to_records, add_student_to_attendance_sheet

class Testutils(unittest.TestCase):

    def test_mark_present(self):
        out = mark_present("20161088", './mock_attendance_sheet.csv')
        self.assertEqual(out, "Done")
    
    def test_add_student_to_attendance_sheet(self):
        out = add_student_to_attendance_sheet("20160000", './mock_attendance_sheet.csv')
        self.assertEqual(out, "Done")

    def test_add_facevec_to_records(self):
        out = add_facevec_to_records(np.ones([512]), "test_vec.npy")
        self.assertEqual(out, "Done")
        os.remove("../server/records/vectors/test_vec.npy")


if __name__ == "__main__":
    unittest.main()