#encoding:utf-8
import os
import cv2
import numpy as np

def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    """
    We create an empty list, dataset. 
    From the dataPath, find out the two folder that store images.
    Use "od.listdir()" two get the name of images.
    Use for loop and "cv2.imread()" to convert each image to numpy array and append to dataset
	return dataset
    """
    dataset = []
    face_path = dataPath+'/face'
    nonface_path = dataPath+'/non-face'
    face_files = os.listdir(face_path)
    for face_file in face_files:
        face_file = face_path+'/'+face_file
        img = cv2.imread(face_file,-1)
        dataset.append((img,1))
    
    nonface_files = os.listdir(nonface_path)
    for nonface_file in nonface_files:
        nonface_file = nonface_path+'/'+nonface_file
        img = cv2.imread(nonface_file,-1)
        dataset.append((img,0)) 
   
    # End your code (Part 1)
    return dataset
