import cv2
import numpy as np
import face_recognition
import os
import streamlit as st
from datetime import datetime
from streamlit_option_menu import option_menu
from deepface import DeepFace

with st.sidebar:
    selected=option_menu(
        menu_title=None,
        options=['Home','Mark Attendance','View Attendance','Manually Attendance','Extra Feature','About Us'],
        # orientation="horizontal",
        icons=['house','check2-circle','file-earmark-spreadsheet-fill','pencil-square','emoji-sunglasses-fill','file-person'],

        styles={
            "icon":{"color":"yellow"},
            "nav-link":{
                # "font-size":"25px",
                "--hover-color":"lightdark",

            },
            "nav-link-selected":{"background-color":"green"},
            
        },
           
    )

def faceEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

#attendance mark

def attandace(name):
   
   #for searching name in text file
    def seraching(data,namePerson):
        i=0
        while(i<len(data)):
            if (namePerson==data[i]):
                return i
            i=i+1
        return -1 #if not found

    with open('attandacerecord.csv','r+') as f1:
        Data=f1.readlines()
        nameLits=[]

        for line in Data:
            entry=line.split(',')
            nameLits.append(entry[0])
        
        if name not in nameLits:
            
            #Finding name with roll..sec..enroll
            f=open('stname.text',)
            data=f.read() #get all the contact # name= anushka
            data=data.split(',') #convert into list # data=['kabir','Anushka','Elon']
            f.close()
            idx=seraching(data,name)

            f=open("rollno.text")
            number=f.read()#get all the roll number
            number=number.split(",") #convert into list
            rol=number[idx] #get exactly  roll number
            f.close()

            f=open("stsec.text")
            number=f.read()#get all the sec number
            number=number.split(",") #convert into list
            sec=number[idx] #get exactly  sec
            f.close()

            f=open("enroll.text")
            number=f.read()#get all the enroll number
            number=number.split(",") #convert into list
            enrol=number[idx] #get exactly  enroll number
            f.close()


            time_now=datetime.now()
            tstr=time_now.strftime('%H:%M:%S')
            dstr=time_now.strftime('%d/%m/%y')
            # f.writelines(f'{name},{tstr},{dstr}\n')
            f1.writelines(f'{name},{enrol},{sec},{rol},{tstr},{dstr}\n')


if selected=='Home':
    st.header("Face recognition")
    st.write("It is a website for tracking Attendance by face recognition. It is a modern, time saving and aa simple way to store attendance virtually without using pen and paper or a man power . By recognising the face in front of the camera, it stores the attendance.")

    st.image("backg.jpeg")

    st.header("How to use the website ?")
    st.write("Click on the button - mark attendance and then click enable button , the camera of your device will get switch on, the face in front of the camera will be identified and matched with the database and if a match is found then under the detected face, the name of the person will be shown and the attendance will be stored in an Excel file with the name, enrollment number, section , roll no of that person and also the date and timing of the appearance of that person in front of the camera. You can view the attendance by clicking on View attendance. All the recorded attendance will be shown")
    
    st.header("Must try Extra features")

    st.subheader("Appart from marking attendance it has other 2 exciting must try Extra Features. Those are -: Emotion Detection and Gender Detection ")

    st.subheader("Emotion Detection")
    st.write("One of the extra feature is Emotion Detection - using face recognition technology it can detect a person is expressing what kind of expresiion - happy, sad, angry, fear, neutral, etc")

    st.subheader("Gender Detection")
    st.write("Appart from marking attendance and Emotion Recogniztion, it has one more must try Extra Features. That is Gender Detection - using face recognition technology it can detect a person is Male or Female gender")

if selected=='Mark Attendance':
    selected=option_menu(
        menu_title=None,
        options=['Enable Camera','Disable Camera'],
        icons=['camera-video-fill','camera-video-off-fill'],
        styles={
            "icon":{"color":"yellow"},
            "nav-link-selected":{"background-color":"orange"},
            
        },
    )
    camera = cv2.VideoCapture(0)
    if selected=='Enable Camera':
        FRAME_WINDOW= st.image([])
        path = 'imageFolder\\'
        images = []
        personName = []
        myList = os.listdir(path)

    
        for cu_img in myList:
            current_img = cv2.imread(f'{path}/{cu_img}')
            images.append(current_img)
            personName.append(os.path.splitext(cu_img)[0])

        encodeListKnown = faceEncodings(images)

        
        while True:
          ret, frame = camera.read()
          frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
          faces = cv2.resize(frame, (0,0), None, 0.25, 0.25)
          faces = cv2.cvtColor(faces,cv2.COLOR_BGR2RGB)
          facesCurrentFrame = face_recognition.face_locations(faces)
          encodeCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

          for encodeFace, faceLoc in zip(encodeCurrentFrame, facesCurrentFrame):
              matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
              faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

              matchIndex = np.argmin(faceDis)

              if matches[matchIndex]:
                   name = personName[matchIndex].upper()
                   y1, x2, y2, x1 = faceLoc
                   y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                   cv2.rectangle(frame, (x1,y1),(x2,y2),(0,255,0), 2)
                   cv2.rectangle(frame, (x1, y2-35), (x2,y2), (0,255,0), cv2.FILLED)
                   cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                   attandace(name)
          FRAME_WINDOW.image(frame)
        
          
    if selected=='Disable Camera':
        st.success("Successfully!!! Camera Closed")
        camera.release()
        cv2.destroyAllWindows()


if selected=='View Attendance':
    import pandas as pd
    data=pd.read_csv('attandacerecord.csv')
    st.dataframe(data)

if selected=='Manually Attendance':
    name=st.text_input("Enter Student Name")
    roll=st.text_input("Enter Roll")
    # roll=int(roll)
    sec=st.text_input("Enter Section")
    enrol=st.text_input('Enter Enroll')
    roll=str(roll)
    enrol=str(enrol)
    sec=str(sec)
    name=(str(name)).upper()
    if name and roll and enrol and sec:
        with open('attandacerecord.csv','r+') as f1:
            Data=f1.readlines()
            nameLits=[]

            for line in Data:
                entry=line.split(',')
                nameLits.append(entry[0])
        
            if name not in nameLits:
                time_now=datetime.now()
                tstr=time_now.strftime('%H:%M:%S')
                dstr=time_now.strftime('%d/%m/%y')
            # f.writelines(f'{name},{tstr},{dstr}\n')
                f1.writelines(f'{name},{enrol},{sec},{roll},{tstr},{dstr}\n')
                st.success("Attendance Mark Successfully")
            
       
        # time_now=datetime.now()
        # tstr=time_now.strftime('%H:%M:%S')
        # dstr=time_now.strftime('%d/%m/%y')
        #     # f.writelines(f'{name},{tstr},{dstr}\n')
        # f1=open('attandacerecord.csv',mode='r+')
        # f1.writelines(f'{name},{enrol},{sec},{roll},{tstr},{dstr}\n')
        # f1.close()


#Code of extra feature
if selected=='Extra Feature':
    selected=option_menu(
         menu_title=None,
        options=['Emotion Detection','Gender Detection'],
        # icons=['gender'],
        styles={
            "icon":{"color":"yellow"},
            "nav-link-selected":{"background-color":"orange"},
            
        },

    )

    if selected=='Emotion Detection':
        cap=cv2.VideoCapture(0)
        FRAME_WINDOW= st.image([])
        
        while True:
            ret,frame=cap.read()
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            try:
                 analyze=DeepFace.analyze(frame,actions=['emotion'])
                 cv2.putText(frame,str(analyze['dominant_emotion']),(200,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
            except:
                pass

            FRAME_WINDOW.image(frame)
    
    if selected=='Gender Detection':
        cap=cv2.VideoCapture(0)
        FRAME_WINDOW= st.image([])
        
        while True:
            ret,frame=cap.read()
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            try:
                 analyze=DeepFace.analyze(frame,actions=['gender'])
                #  str(analyze['gender'])
                 cv2.putText(frame,'WOMEN',(200,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
            except:
                pass

            FRAME_WINDOW.image(frame)


#Write about us 
