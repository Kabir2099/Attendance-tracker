from deepface import DeepFace
import cv2
import matplotlib.pyplot as plt
import numpy as np
import face_recognition
import os
from datetime import datetime

path='imageFolder' #Image location
images=[]
personName=[]  #collcet person Nmae
myList=os.listdir(path) #list of image
# print(myList)

for cu_img in myList:
    current_img=cv2.imread(f'{path}\\{cu_img}') #read image through location
    images.append(current_img) #add image in thr images
    personName.append(os.path.splitext(cu_img)[0]) #get person name

print(personName)

def FaceEnoding(images):
    encodeList=[]

    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    
    return encodeList

encode_ImageFolder=FaceEnoding(images)
print("All Encoding Done")

def attandace(name):
    with open('attandacerecord.csv','r+') as f:
        Data=f.readlines()
        nameLits=[]

        for line in Data:
            entry=line.split(',')
            nameLits.append(entry[0])
        
        if name not in nameLits:
            time_now=datetime.now()
            tstr=time_now.strftime('%H:%M:%S')
            dstr=time_now.strftime('%d/%m/%y')
            f.writelines(f'{name},{tstr},{dstr}\n')



cap=cv2.VideoCapture(0)

while True:
    ret,frame=cap.read()
    faces=cv2.resize(frame,None,fx=0.25,fy=0.25)
    faces=cv2.cvtColor(faces,cv2.COLOR_BGR2RGB)
    face_Find_Frame=face_recognition.face_locations(faces)
    encode_Frame=face_recognition.face_encodings(faces,face_Find_Frame)

    for encodeFace,faceLoc in zip(encode_Frame,face_Find_Frame):
        matches=face_recognition.compare_faces(encode_ImageFolder,encodeFace)
        face_Dist=face_recognition.face_distance(encode_ImageFolder,encodeFace)
        match_idx=np.argmin(face_Dist)

        if matches[match_idx]:
            name=personName[match_idx]
            print(name)
            y1,x2,y2,x1=faceLoc
            y1,x2,y2,x1=y1 *4,x2 *4,y2 *4,x1 *4
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            attandace(name)
            try:
                 analyze=DeepFace.analyze(frame,actions=['emotion'])
                 cv2.putText(frame,str(analyze['dominant_emotion']),(200,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
            except:
                pass
    cv2.imshow("Camera",frame)


    if cv2.waitKey(1)==13:
        break


cap.release()
cv2.destroyAllWindows()
