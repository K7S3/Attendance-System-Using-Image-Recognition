import numpy as np
import cv2
import os

def recognize_face(face_vector, recognition_thresh):
    ''' 
    Reads face vectors from the records, compares them with the input vector using l2 norm returns the rollnumber against the best match
    :param face_vector: {np.ndarray} The face vector which is to be matched.
    :param recognition_thresh: {float} The min threshold for l2 distance
    :return: {str} The matchde roll number or None
    '''
    
    records_dir = '/home/pranay/college/8/swe/Attendance-System-Using-Image-Recognition/server/records'
    min_dist = np.Infinity
    roll_number = None
    for vec_file in os.listdir(os.path.join(records_dir, 'vectors')):
        vec = np.load(os.path.join(records_dir, 'vectors',vec_file))
        dist = np.linalg.norm(face_vector - vec)
        if dist < min_dist:
            min_dist = dist
            roll_number = vec_file.split('.')[0]

    if min_dist < recognition_thresh:
        return roll_number
    else:
        return None

