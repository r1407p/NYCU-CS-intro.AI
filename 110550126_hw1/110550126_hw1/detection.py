import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    """
    we first read the txt file, according the content in txtfile
    we convert the content into a list of tuple 
    with first element is the name of img and second element is the list of face rectangle
    """
    with open(dataPath) as f:
      txt_content = f.read().split('\n')
      print(txt_content)
      i = 0
      imgs = []
      while i < len(txt_content):
        img_name , recs = txt_content[i].split(" ")
        recs = int(recs)
        faces = txt_content[i+1:i+1+recs]
        faces = [face.split(" ") for face in faces]
        for j in range(len(faces)):
          faces[j] = [int(face) for face in faces[j]]
        imgs.append((img_name,faces))
        i+=recs+1
      for img_path,recs in imgs:
        img = cv2.imread('data/detect/'+img_path)
        cv2.imshow('Result',img)
        cv2.waitKey(0)
        #print(clf)
        is_face = []
        for rec in recs:
          face = img[rec[1]:rec[1]+rec[3]+1,rec[0]:rec[0]+rec[2]+1]
          #cv2.imshow('R',face)
          face = cv2.resize(face,(19,19),interpolation=cv2.INTER_AREA)
          face = cv2.cvtColor(face, cv2.COLOR_RGB2GRAY)
          #face= np.mean(face, axis=2)
          #(face)
          #print(face.shape)
          #print(type(face))
          #print(rec)

          """fig, ax = plt.subplots(1, 2)
          ax[0].axis('off')
          ax[0].set_title('Face')
          ax[0].imshow(face, cmap='gray')
          ax[1].axis('off')
          ax[1].set_title('Non face')
          ax[1].imshow(face, cmap='gray')
          plt.show()"""
         
          is_face.append(clf.classify(face))
        for i in range(len(is_face)):
          if is_face[i]==1:
            img = cv2.rectangle(img, (recs[i][0],recs[i][1]),(recs[i][0]+recs[i][2],recs[i][1]+recs[i][3]), (0,255,0), 2)
          else:
            img = cv2.rectangle(img, (recs[i][0],recs[i][1]),(recs[i][0]+recs[i][2],recs[i][1]+recs[i][3]), (0,0,255), 2)
        cv2.imshow('result',img)
        cv2.waitKey(0)
        #print(img)
        

        
        
    # End your code (Part 4)
