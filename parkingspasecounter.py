import cvzone
import cv2
import pickle
import numpy as np

capture = cv2.VideoCapture('CarPark_vid.mp4')

def checkparkingspace(img_filter):
    freespace =0
    for pos in pos_list:
        x,y = pos
        crop_img = img_filter[y : y+height ,x:x+width]
        #cv2.imshow(str(x*y),crop_img)
        count = cv2.countNonZero(crop_img)
        #cvzone.putTextRect(img,str(count),(x,y+height-5),scale= 1.3 , offset= 8,colorR = (0,0,0))

        if count< 950:
            color=(0,255,255)
            thickness = 6
            freespace +=1
        else:
            color = (40,40,240)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height),color , thickness)
    cvzone.putTextRect(img, f'{freespace} Free', (100,50), scale=4, offset=20, colorR=(200, 0, 0))

with open('carpark_pos', 'rb') as f:
    pos_list = pickle.load(f)

width, height = 107,48

while True:
    if capture.get(cv2.CAP_PROP_POS_FRAMES) == capture.get(cv2.CAP_PROP_FRAME_COUNT):
        capture.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img = capture.read()
    Gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    Blur = cv2.GaussianBlur(Gray, (3,3), 1)
    Threshold = cv2.adaptiveThreshold(Blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    Median = cv2.medianBlur(Threshold,5)
    kernal = np.ones((3,3),np.uint8)
    Dilate = cv2.dilate(Median,kernal,iterations = 1,)

    checkparkingspace(Dilate)

    cv2.imshow("image",Dilate)
    cv2.waitKey(2)
