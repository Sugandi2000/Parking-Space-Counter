import cv2
import pickle

width, height = 107,48

try:
    with open('carpark_pos', 'rb') as f:
         pos_list = pickle.load(f)
except:
    pos_list = []


def mouseclick(events,x,y,flags,para):
    if events == cv2.EVENT_LBUTTONDOWN:
        pos_list.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(pos_list):
            x1, y1 = pos
            if x1 < x < x1+width and y1 < y < y1+height:
                pos_list.pop(i)
    with open('carpark_pos','wb') as f:
        pickle.dump(pos_list,f)

while True:
    img = cv2.imread('CarPark_img.png')
    for pos in pos_list:
         cv2.rectangle(img,pos,(pos[0]+ width, pos[1]+ height),(255,0,255),2)

    cv2.imshow("image",img)
    cv2.setMouseCallback("image",mouseclick)
    cv2.waitKey(1)