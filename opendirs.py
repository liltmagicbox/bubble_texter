import cv2
import numpy as np 
from getdirs import onlydirs, getimgs, iscoll,timeprinter,loopcounter
from textspliter import textbox

from PIL import ImageFont, ImageDraw, Image
def getkrtext(text,color = (255,255,255,0)):
    img = np.zeros((200,400,3),np.uint8)
    b,g,r,a = 255,255,255,0
    fontpath = "ridibatang.ttf"
    font = ImageFont.truetype(fontpath, 20)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text((60, 70),  text, font=font, fill=(b,g,r,a))
    img = np.array(img_pil)
    return img
#img = getkrtext('므히히히히')
#cv2.imshow('haha',img)

def fillkr(img,text,cord,size, color=(255,0,255)):
    #img = np.zeros((600,400,3),np.uint8)
    fontpath = "ridibatang.ttf"
    font = ImageFont.truetype(fontpath, size)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text(cord,  text, font=font, fill=color)
    img = np.array(img_pil)
    return img

def loaddirs():
    dirlist = onlydirs()        
    drawrects(dirlist)

def drawrects(dirlist):
    
    window_w = 600
    window_h = 900
    
    w = window_w//2
    h = window_w//10
    #img = np.zeros((800,400,3), np.uint8)#800짜리가 400줄있고,그안에 rgb이다.
    img = np.ones((800,400,3), np.uint8)*250
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        
    
    for i,d in enumerate(dirlist):
        text = d
        ba = (h,h*(i+1))
        bb = (w,h*(i+2))
        size = 1.2
        thick = 2
        color = (255,255,0)
        textlow = (h,h*(i+1)+h//2)
        #cv2.putText(img, text, textlow, cv2.FONT_HERSHEY_SIMPLEX, size, color, thick, cv2.LINE_AA)
        
        cord = (h,h*(i+1))
        #size = 30
        letters = len(text)
        coin = 1.5# seems size fits height. eng 1.5, kor,1.?
        
        size = 30
        img = fillkr(img,text,cord,size,color=color)
        
        
#         nsize = size        
#         while nsize*textl>boxw:
#             nsize = int(nsize*0.9)
#             print(size,nsize, nsize*textl)
#             if nsize < boxh*0.5:
#                 break
#         ncolor = (255,0,255)
#         img = fillkr(img,text,cord,nsize,color=ncolor)
        #step 1 done.

        rawsize = 30
        door =  h
        wide =  w-h
        
        row = 1
        divider = 2
        texts = text.split(' ')
        textrow=[]
        #longman = ''.join(texts)        
        textrow.append(texts)
        
        #loop1
        textrow[0]=texts
        text = ''.join(texts)
        man = len(text)
        while size * man > wide:
            size = int(size*0.9)
            if size < door/2:
                break
        if not size * man > wide:
            draw()
        
        #loop 2
        textrow[0]=texts
        textrow[1]=[]
        
        pop = textrow[0].pop()
        textrow[1].append(pop)        
        text = ''.join(textrow[0])
        man = len(text)
        
        while size * man > wide:
            pop = textrow[0].pop()
            textrow[1].append(pop)
            text = ''.join(textrow[0])
            man = len(text)
            text1 = ''.join(textrow[1])
            man1 = len(text1)
            if size * man1 > wide:
                break
        for man in mans:
        if not size * man > wide:
            draw()
        
            
                size = int(size*0.9)
                if size < door/3:
                    break
        if not size * man > wide:
            draw()
        
        #loop 1
        #def checker(textrow,size,wide,door,divider):
            for idx,texts in enumerate(textrow):
                text = ''.join(texts)
                man = len(text)
                while size * man > wide:
                    if size < door/divider:
                        textrow
                    size = int(size*0.9)
                    
            return False
        while( checker(textrow,size,wide,door,divider) ):
              divider+=1
                    
        
                    
#             while man * size > wide:
#                 size = mario(size,man,wide,door,divide)
                
        
        
        
        
#         def mario(size,man,wide,door,divide=2):
#             while size * man > wide:
#                 size = int(size*0.9)
#                 if size < door/divider:
#                     break
#             return size

        
        #ntextl = textl
        #ntext = text
                
#         texts = [ntext]
#         textrow = []
#         for idx,text in enumerate(texts):
#             textrow[idx] = ""
#             maxidx = len(text.split(' '))-1
#             while nsize * len(text) > boxw:
#                 for i,t in enumerate(text.split(' ')):
#                     if i == maxidx:
#                         textrow[idx+1] += t
#                         break
#                     text1 += t
#                 ntextl = len(text1)
#                 print(text1)
#                 print(text2)
            
        
        
        
#         while size*letters*coin>boxw:
#             #size = int(size/2*coin)
#             #letters = int(letters/2)
#             size = int(size*0.9)
#             #letters = int(letters/2)
#             print(size*letters*coin,boxw,size)
#         
#         cut = int(len(text)/2)
#         texta = text[:cut]
#         img = fillkr(img,texta,cord,size)
#         textb = text[cut:]
#         cord = cord[0],cord[1]+size
#         img = fillkr(img,textb,cord,size)
        
        #texts = [text]
#         texts = text.split(' ')
#         size = h
#         while size*letters>boxw:
#             size= int(size/2)
#             letters = int(letters/2)
#             texts = [text[:letters]]
#             
#         #size = int((w-h)/letters*coin)
#         
#         for text in texts:
#             #cord = cord[0]+len(text)*size,cord[1]
#             img = fillkr(img,text,cord,size)
        
        a,b=ba,bb
        cv2.rectangle(img,a,b,(0,0,200),2)
    cv2.imshow('speedbubble', img)
loaddirs()

