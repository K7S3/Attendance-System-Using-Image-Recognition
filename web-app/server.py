from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import json
import random
import datetime

from recognize_face import recognize_face
import socket
import numpy
import pickle
import select
import _thread

# for socketio
import eventlet
eventlet.monkey_patch()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///../database/main.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['static_url_path'] = '/assets'
db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode='eventlet')
# socketio = SocketIO(app )

#recieve feature vector
#check if it exist in DB using L2 norm
#if not store return not present in database
#request photo again


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    feature_vector = db.Column(db.String(80), unique=True, nullable=False)


class Lecture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    teacher = db.Column(db.String(80), unique=True, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    

def l2_distance(a, b):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))


@socketio.on('insert records')
def insertRecords(user_list):
    for user in user_list:
        if User.query.get(user.id) not in user_list:
            db.session.add(user)
    db.session.commit()


@socketio.on('delete records')
def deleteRecords(user_list):
    for user in user_list:
        if User.query.get(user.id) not in user_list:
            db.session.delete(user)
    db.session.commit()


@socketio.on('insert lectures')
def createLecture(lecture_list):
    for lecture in lecture_list:
        if Lecture.query.get(lecture.id) not in lecture_list:
            db.session.add(lecture)
    db.session.commit()


@socketio.on('delete lectures')
def createLecture(lecture_list):
    for lecture in lecture_list:
        if Lecture.query.get(lecture.id) not in lecture_list:
            db.session.delete(lecture)
    db.session.commit()


@socketio.on('join lecture')
def handleFeatureVector(query):    
    start_procedure(query['face_vec'])
    # join_room(query['courses'])
    # send(user.name + ' has entered the room.', room=query['courses'])
    

@socketio.on('leave lecture')
def handleFeatureVector(query_vector, lecture):
    user = User.query.filter(func.min(l2_distance(User.feature_vector, query_vector)))
    # print(user.name + "Present")
    leave_room(lecture.id)
    send(user.name + ' has left the room.', room=lecture.id)
    
    # print(datetime.datetime.now(),'Message: ' + msg)
    # send(msg, broadcast=True)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def cas():
    # call cas
    return render_template("logged_in.html")
    pass

@app.route("/admin")
def admin():
    return render_template("admin.html")
# @app.route("/mark_attendance/<int: lecture_id")
# def mark_attendance():
    

def start_procedure(face_vec):
    '''Function for starting the procedure to mark attendance'''
    while True:
        if isinstance(face_vec, str):
            send('message', face_vec)
        else: 
            roll_number = recognize_face(face_vec, 100)
            if roll_number is not None:
                send('message', roll_number + " marked present")
            else:
                send('message', "Face not recognized")
    return None


if __name__ == '__main__':
    socketio.run(app, host="localhost", port="8000")