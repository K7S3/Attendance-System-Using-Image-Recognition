import pandas as pd
import numpy as np
from datetime import date
import os

def mark_present(roll_number, path = './attendance_sheet.csv'):
    '''Updates the attendance sheet for the day'''
    df = pd.read_csv(path)
    today = str(date.today())
    if today not in df.keys():
        df[today] = ['A']*len(df)
    for num, roll in enumerate(df['Rollnumber']):
        if roll == int(roll_number):
            df.at[num, today] = 'P'
    df.to_csv(path, index=False)

def add_facevec_to_records(face_vector, fname):
    '''adds face vector to records'''
    path = os.path.join('./records/vectors/', fname)
    np.save(path, face_vector)

def add_student_to_attendance_sheet(roll_number, path = './attendance_sheet.csv'):
    '''adds students rol number to the attendance sheet'''
    df = pd.read_csv(path)
    record = {}
    for key in df.keys():
        if key == 'Rollnumber':
            record[key] = [roll_number]
        else:
            record[key] = ['A']
    df1 = pd.DataFrame(data = record)
    df2 = df.append(df1)
    cols = df.columns.tolist()
    df2 = df2[cols]
    df2.to_csv(path, index=False)

def enroll_student(roll_number, face_vector):
    '''enrolls a student '''
    add_facevec_to_records(face_vector, roll_number+".npy")
    add_student_to_attendance_sheet(roll_number)
    mark_present(roll_number)