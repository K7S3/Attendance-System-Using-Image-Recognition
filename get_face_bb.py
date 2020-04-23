from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import numpy as np
import cv2

def get_face_bb(detection_thresh):
    ''' Uses facenet to detect face and then an inception net to calculate the embedding of the detected face'''
    device = 'cpu'
    mtcnn = MTCNN(
        image_size=160, margin=0, min_face_size=20,
        thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
        device=device
    )
    resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        print('camera started')
        x_aligned, prob = mtcnn(frame, return_prob=True)
        if x_aligned is not None:
            print('Face detected with probability: {:8f}'.format(prob))
            if prob > detection_thresh:
                break
            
    face_embedding = resnet(torch.stack([x_aligned]))

    return face_embedding