import numpy as np
import os
import math
import cv2
from fer import FER
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
from keras.models import load_model
from flask import Flask, render_template, Response, request
import  tensorflow as tf
from keras.utils import image_utils as image
# sample code
graph=tf.compat.v1.get_default_graph()
writer=None
model=load_model('IBM.h5')
font = cv2.FONT_HERSHEY_SIMPLEX
vals=['A','B','C','D','E','F','G','H','I']
emotion_detector = FER(mtcnn=True)
app=Flask(__name__,template_folder="templates")

print("Accessing video stream..")
app.static_folder = 'static'
source=cv2.VideoCapture(0)
pred=""
language = 'en'

def gen():
    color_dict=(0,255,0)
    img_size=64
    minValue = 0
    count = 0
    string = " "
    prev = " "
    prev_val = 0
    while (source.isOpened()):
        
        success, frame = source.read()
        frame=cv2.GaussianBlur(frame, (5,5),0)
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # sample code
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('image1.html')
@app.route('/sign_to_speech')
def sign_to_speech():
    return render_template('image2.html')
@app.route('/speech_to_sign')
def speech_to_sign():
    return render_template('image3.html')
    

@app.route('/video',methods=['GET', 'POST'])
def video():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
if (__name__ == "__main__"):
    app.run(debug=True)
