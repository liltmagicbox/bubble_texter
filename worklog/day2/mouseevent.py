import numpy as np
import cv2

# callback함수
def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        print(x,y)
        cv2.circle(img,(x,y), 50,(0,0,250),2)
        cv2.imshow('mouse', img)

    if event == cv2.EVENT_RBUTTONUP:
        print(x,y)
        d = 20
        x1,x2 = x-d,x+d
        y1,y2 = y-d,y+d
        cv2.rectangle(img,(x1,y1), (x2,y2),(250,0,250),2)
        cv2.imshow('mouse', img)

    if event == cv2.EVENT_RBUTTONDOWN:
        d = 5
        x1,x2 = x-d,x+d
        y1,y2 = y-d,y+d
        cv2.rectangle(img,(x1,y1), (x2,y2),(250,0,0),1)
        cv2.imshow('mouse', img)
    if event == cv2.EVENT_MOUSEMOVE:
        if flags&cv2.EVENT_FLAG_CTRLKEY:
            d = 5
            x1,x2 = x-d,x+d
            y1,y2 = y-d,y+d
            cv2.rectangle(img,(x1,y1), (x2,y2),(250,0,0),1)
            cv2.imshow('mouse', img)

#이렇겐아닌듯.        
##    if event == cv2.EVENT_FLAG_CTRLKEY:
##        print("finally!!",event)
        

# 빈 Image 생성
img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('mouse')

cv2.setMouseCallback('mouse', draw_circle)

while(1):    
    cv2.imshow('mouse', img)
    print('ha')
    if cv2.waitKey(0) & 0xFF == 27:#esc
        print('esc!')
        break

cv2.destroyAllWindows()
