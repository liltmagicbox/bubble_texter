import cv2
import numpy as np 
from getdirs import onlydirs, getimgs, iscoll,timeprinter,loopcounter
from textspliter import splitted

from PIL import ImageFont, ImageDraw, Image

def boxkr(text,size, box, color=(255,0,255) ,center=False):
    #fontpath = "ridibatang.ttf"
    fontpath = 'NotoSerifKR-Medium.otf'
    multiply = 0.85
    multi_vert = 0.9
    minsize = 10
    
    interrow = 1.0 #image area height and each row.
        
    bw,bh = box
    bh = int(bh*interrow)
    img = np.ones((bh,bw,3),np.uint8)*255
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    
    #font = ImageFont.truetype(fontpath, size)
    #draw.text(cord, text, font=font, fill=color)
    
    size,texts = splitted(text, size, box, multiply=multiply,multi_vert=multi_vert, minsize=minsize)
    print(size,texts)
    font = ImageFont.truetype(fontpath, size)
    for i,text in enumerate(texts):        
        if center==True:
            gap = bw-len(text)*multiply*size
            print(gap)
            if gap>size*2:
                cordx = int(gap/2)
                
        cordx = 0+2#tooclose!
        cordy = size*i*interrow
        cord = cordx,cordy
        draw.text(cord, text, font=font, fill=color, align ="right")    
    img = np.array(img_pil)    
    cv2.imshow(text,img)
    return img



def overwrite(body,attach,cord ,trans = False):
#     if len(body[0][0]) != len(attach[0][0]):
#         raise ValueError("demention not match")
    
    
    mh,mw, md = attach.shape
    
    x,y = cord
    b,a = y+mh,x+mw
    
    #whiteboard = np.ones((mh,mw,3),np.uint8)*255
    
    
    if trans:#not working. hollow letter..
        #_, mask = cv2.threshold(img_fg[:,:,3], 1, 255, cv2.THRESH_BINARY)
        mask = cv2.cvtColor(attach,cv2.COLOR_RGB2GRAY)
        mask = abs(mask-255)
        _, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        
        img_fg = attach[:,:]
        img_bg = body[y:b,x:a]
        masked_fg = cv2.bitwise_and(img_fg, img_fg, mask=mask)
        masked_bg = cv2.bitwise_and(img_bg, img_bg, mask=mask_inv)
        
        added = masked_fg + masked_bg
        body[y:b,x:a ] = added
        
        #for i in range( len(body[0][0]) ):
            #body[y:b,x:a, i] = body[y:b,x:a, i] + attach[:,:,i]#over255
            #body[y:b,x:a, i] = cv2.add( body[y:b,x:a, i] ,attach[:,:,i] )
            #body[y:b,x:a, i] = cv2.add( whiteboard[:,:,i], attach[:,:,i] )
            
    else:
        for i in range( len(body[0][0]) ):
            body[y:b,x:a, i] = attach[:,:,i]
    #img = cv2.cvtColor(body,cv2.COLOR_BGR2RGB)
    #img = body


def mousehandle(event, x,y, flags, param):
    global dirlist
    if event == cv2.EVENT_LBUTTONDBLCLK: #마우스를 누른 상태
        for idx,r in enumerate(rectboxlist):
            o,n=r
            x1,y1=o
            x2,y2=n            
            if x>x1 and x<x2 and y>y1 and y<y2:
                dirnumber = idx
                #print(idx)
                #del dirlist[idx]
                break
        dirnumber
        #drawrects(dirlist)

windowname = 'dirshow'
rectboxlist = []
def drawwindow():
    cv2.namedWindow(windowname,cv2.WINDOW_NORMAL  )
    cv2.setMouseCallback(windowname,mousehandle)
    
    window_w = 400
    window_h = 700
    cv2.resizeWindow(windowname,window_w,window_h)    
    
def drawrects(dirlist):
    global rectboxlist  
    x,y,window_w, window_h = cv2.getWindowImageRect(windowname)
    w = window_w//2
    h = window_w//10
    
    #img = np.zeros((800,400,3), np.uint8)#800짜리가 400줄있고,그안에 rgb이다.
    img = np.ones((window_h,window_w,3), np.uint8)*255
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    
    
    for i,d in enumerate(dirlist):
        text = d
        
        ba = (h,h*(i+1))
        bb = (w,h*(i+2))
        a,b=ba,bb
        rectboxlist.append( (a,b) )
        cv2.rectangle(img,a,b,(0,0,200),2)
        
        #cv native writer.
        #size = 1.2
        #thick = 2
        #color = (255,255,0)        
        #textlow = (h,h*(i+1)+h//2)
        #cv2.putText(img, text, textlow, cv2.FONT_HERSHEY_SIMPLEX, size, color, thick, cv2.LINE_AA)
        
        #img = fillkr(img,text,cord,size,color=color)
        
        box = (w-h,h)
        size = 30
        color = (0,0,0)        
        boxk = boxkr(text,size, box, color=color)
        #windowname = text
        #cv2.imshow(windowname,boxk)
        #print( 'boxw,h',len(boxk[0]),len(boxk) )        
        cord = ba
        
        #mask = cv2.cvtColor(boxk,cv2.COLOR_RGB2GRAY)
        #_, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
        #boxk = cv2.bitwise_and(boxk, boxk, mask=mask)
        overwrite(img,boxk,cord, trans=False)
            
    cv2.imshow(windowname, img)


if __name__ == '__main__':
    dirlist = onlydirs()
    drawwindow()
    drawrects(dirlist)
    


#-------------------------below test functions
#basic korean writer
def fillkr(img,text,cord,size, color=(255,0,255)):
    #img = np.zeros((600,400,3),np.uint8)
    fontpath = "ridibatang.ttf"
    font = ImageFont.truetype(fontpath, size)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text(cord,  text, font=font, fill=color)
    img = np.array(img_pil)
    return img





# 0 0 2 0 4 0 6 ...array.
#np.array( range(1,10) ).reshape(3,3)
def evennumbers(row=10):
    n=np.array( range(row**2) ).reshape(row,row)
    for y,i in enumerate(n):
        for x,j in enumerate(i):
            if x%2==0 and y%2==0:
                #print('ha')
                n[y][x]=0
    print(n)
    return n
#evennumbers()



#tryed but fail.
def npmerge():
    row=100
    a=((np.array(range(row**2))+1)*255//(row**2)).reshape(row,row)
    b=np.zeros( (500,500),np.uint8)

    b[row:row*2,row:row*2] = a
    img = cv2.cvtColor(b,cv2.COLOR_BGR2RGB)
    cv2.imshow('is',img)
#tried, only works 1 dimention.
def npmerge2():
    row=100
    a=((np.array(range(row**2))+1)*255//(row**2)).reshape(row,row)
    b=np.zeros( (500,500,3),np.uint8)
    #(np.zeros( (500,500,2)))[ 100:200,100:200, 1]

    b[row:row*2,row:row*2, 0] = a
    #b[row:row*2,row:row*2, 1] = a.transpose()
    #b[row:row*2,row:row*2, 2] = a.transpose().transpose()
    b[row:row*2,row:row*2, 2] = a.transpose()
    img = cv2.cvtColor(b,cv2.COLOR_BGR2RGB)
    
    cv2.imshow('is',img)
#npmerge2()

#for make overwrite. 3 dimentions test.
# row = 100
# attach1=((np.array(range(row**2))+1)*255//(row**2)).reshape(row,row)
# attach2=((np.array(range(row**2))+1)*255//(row**2)).reshape(row,row).transpose()
# attach3=((np.array(range(row**2))+1)*255//(row**2)).reshape(row,row)
# attach = np.zeros( (100,100,3),np.uint8)
# attach[:,:,0] = attach1
# attach[:,:,1] = attach2
# attach[:,:,2] = attach3
# cv2.imshow('attach',attach)
# 
# body = np.zeros( (500,500,3),np.uint8)
# overwrite(body,attach,(300,300))
# cv2.imshow('attached',attach)