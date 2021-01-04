#-*- coding:utf-8 -*-
import cv2
import numpy as np 

drawing = False #Mouse가 클릭된 상태 확인용
mode = True # True이면 사각형, false면 원
ix,iy = -1,-1
rectlist=[]
nx,ny = -1,-1
#nx for draw current rect.

pagerects = []

afterpage = 0

rectlistidx = 0
rectpage = {}
rectpage[0]=[]

class rectpage():
    def __init__(self):
        self.idx = 0
        self.page = {}
        self.page[self.idx]=[]
        self.rectlist=[]
    def up(self):
        self.idx+=1
        self.load()
    def down(self):
        self.idx-=1
        self.load()
    def load(self):
        if self.page.get(self.idx) == None:
            self.page[self.idx] = []
        self.rectlist = self.page[self.idx]
    def save(self):
        self.page[self.idx] = self.rectlist
bubbles = rectpage()

def imgload(imgpath):
    img = cv2.imread(imgpath)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    return img

def pagemove(go,x,y):
    #global img, imgold, rectlistidx,rectlist,rectpage
    global img, imgold, bubbles
    global afterpage
    afterpage = 1
    
    #rectpage[rectlistidx] = rectlist
    #bubbles.page[bubbles.idx] = bubbles.rectlist
    bubbles.save()
    
    if go:
        imgpath = '2.jpg'
        #bubbles.idx +=1
        #rectlistidx += 1
        bubbles.up()
    else:
        imgpath = '1.jpg'
        #rectlistidx -= 1
        #bubbles.idx -=1
        bubbles.down()
    
    #if rectpage.get(rectlistidx) == None:
    #    rectpage[rectlistidx] =[]
    #rectlist = rectpage[rectlistidx]
    #bubbles.load()
    
    img = imgload(imgpath)
    imgold=np.ndarray.copy(img)

def pagemovechk(x,y):
    for idx,r in enumerate(pagerects):
        o,n=r
        x1,y1=o
        x2,y2=n
        
        go = idx%2#0 or 1 hopely..
        if x>x1 and x<x2 and y>y1 and y<y2:            
            pagemove(go,x,y)
            break

def getpagerect(window_w,window_h):
    pagerectw = window_w//15
    pagerecth = window_h//15
    pagey = window_h//2
    pagerects = [ [(0,pagey-pagerecth),(pagerectw,pagey+pagerecth)],
                [(window_w-pagerectw,pagey-pagerecth),(window_w,pagey+pagerecth)] ]
    #print(pagerects)
    return pagerects
#y,x!


def drawpagerect(img):
    global pagerects
    imy,imx,d = img.shape
    pagerects = getpagerect(imx,imy)
    for r in pagerects:
        a,b = r
        cv2.rectangle(img,a,b,(255,0,80),2)
    return img

def delrect(x,y):        
    for idx,r in enumerate(rectlist):
        o,n=r
        x1,y1=o
        x2,y2=n            
        if x>x1 and x<x2 and y>y1 and y<y2:
            del rectlist[idx]
            break

# Mouse Callback함수
def draw_circle(event, x,y, flags, param):
    global ix,iy, drawing, mode, rectlist, nx,ny, afterpage

    if event == cv2.EVENT_LBUTTONDOWN: #마우스를 누른 상태
        drawing = True
        ix, iy = x,y
        nx,ny=x,y
        #cv2.line(img, (x, y), (x-20, y), (0, 0, 255), 2)
        #cv2.line(img, (x, y), (x, y-20), (0, 0, 255), 2)
        #this triggers last event.
        if afterpage:
            afterpage=0
    elif event == cv2.EVENT_MOUSEMOVE: # 마우스 이동
        if drawing == True:            # 마우스를 누른 상태 일경우
            if mode == True:
                pass
                cv2.rectangle(img,(ix,iy),(x,y),(255,0,0),2)
            else:
                cv2.circle(img,(x,y),5,(0,255,0),-1)
            #update new position
            nx,ny=x,y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False;             # 마우스를 때면 상태 변경
        if mode == True:
            cv2.rectangle(img,(ix,iy),(x,y),(255,0,0,0.2),1)            
        else:
            cv2.circle(img,(x,y),5,(0,255,0),-1)
        
        #skip if afterpage.
        if afterpage:
            return False
        #toosmall nodraw
        if (ix-x)**2+(iy-y)**2 > 100:
            if ix>x:
                x,ix = ix,x
            if iy>y:
                y,iy = iy,y
            rectlist.append( [(ix,iy),(x,y)] )            
    
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        delrect(x,y)
        pagemovechk(x,y)
        #cv2.circle(img,(x,y),5,(0,255,0),-1)



img = imgload('1.jpg')
imgold=np.ndarray.copy(img)
imh,imw,d=img.shape
#img = np.zeros((imh,imw,3), np.uint8)
#cv2.namedWindow('image')
#cv2.setMouseCallback('image',draw_circle)

#window_w = 800
#window_h = 1000

cv2.namedWindow('speedbubble',cv2.WINDOW_NORMAL  )#seems only one, but works only resizeable
#cv2.namedWindow('speedbubble',flags = cv2.WINDOW_NORMAL&cv2.WINDOW_KEEPRATIO&cv2.WINDOW_GUI_EXPANDED )
#cv2.resizeWindow('speedbubble',window_w,window_h)
cv2.resizeWindow('speedbubble',imw,imh)
cv2.setMouseCallback('speedbubble',draw_circle)

from time import time
oldt=time()

def drawrect(img):
    for r in rectlist:
        o,n = r        
        cv2.rectangle(img,o,n,(255,0,255),2)
    if drawing:
        cv2.rectangle(img,(ix,iy),(nx,ny),(0,0,255),2)
    return img

while True:
    img = np.ndarray.copy(imgold)
    img = drawrect(img)
    img = drawpagerect(img)
    
    #(720, 400), (800, 600)
    #cv2.rectangle(img,(600, 100), (800, 600),(0,0,80),5)
    #cv2.line(img, (0,900), (80,1100), (255, 0, 0), 5)
    #cv2.line(img, (0, 0), (511, 511), (255, 0, 0), 5)
    cv2.imshow('speedbubble', img)    
    
    newt=time()
    if newt-oldt>1:
        oldt=newt
        #print(oldt)

    k = cv2.waitKey(1) & 0xFF

    if k == ord('m'):    # 사각형, 원 Mode변경
        mode = not mode
    elif k == 27:        # esc를 누르면 종료
        break

cv2.destroyAllWindows()
