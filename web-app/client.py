from get_face_vector import get_face_vector
import socketio

import numpy
import pickle

sio = socketio.Client()



@sio.event
def connect():
    print("Connected")

    print("Ready?")
    inp = input("Ready? Y or N : ")
    if inp == "Y":
        send_feature_vector()
    else:
        sio.disconnect()


def send_feature_vector():
    face_vec = get_face_vector(.95)
    serialized_data = pickle.dumps(face_vec, protocol=2)
    sio.emit('join lecture', {'face_vec': serialized_data})


@sio.event
def connect_error():
    print("The connection failed!")


@sio.event
def disconnect():
    print("Disconnected!")


@sio.on('message')
def on_message(data):
    print(data)


sio.connect('http://localhost:8000/')