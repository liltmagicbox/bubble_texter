#-*- coding:utf-8 -*-
import cv2
import numpy as np 
from getdirs import onlydirs, getimgs, iscoll,timeprinter,loopcounter

from tess_img2rect import img2text
from textdealer import text2rows, text2txt, text2row

from time import sleep
import os

from jsonio import loadJson, saveJson

from cv_tnffy import tnf

def imgload(imgpath):
    #img = cv2.imread(imgpath)#kr path cv cant
    img = imreadkr(imgpath)
    if type(img) == None:
        print('img no!')
        img = np.zeros((480,640,3), np.uint8)
    #img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    return img

def cropimg(img,box):
    a,b = box
    x1,y1=a
    x2,y2=b
    #print(x1,y1,x2,y2)
    return img[ y1:y2, x1:x2, :]

def imreadkr(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

class rectdealer():
    def __init__(self, imgw, color = (255,0,255) ):
        self.color = color
        self.drawing = False #Mouse가 클릭된 상태 확인용
        self.afterpage = 0
        self.oldcord = -1,-1
        self.newcord = -1,-1
        
        self.rectlist = []
        
        self.sizeu = int(imgw/16)#was 100. but bad 1400w.        

    def setnew(self,x,y):
        self.newcord = x,y
    def setold(self,x,y):
        self.oldcord = x,y
    
    
    def addrect(self,x,y):
        ix,iy = self.oldcord
        #toosmall not draw
        #print('rect',abs(ix-x)+abs(iy-y),'sizeu',self.sizeu)
        #if (ix-x)**2+(iy-y)**2 > self.sizeu:
        if abs(ix-x)+abs(iy-y) > self.sizeu:
            if ix>x:
                x,ix = ix,x
            if iy>y:
                y,iy = iy,y
            self.rectlist.append( [(ix,iy),(x,y)] )        
    def delrect(self,x,y):
        for idx,r in enumerate(self.rectlist):
            area = r
            if iscoll(x,y,area):
                del self.rectlist[idx]
                break        
    def lclick(self,x,y):
        self.drawing=True
        self.setold(x,y)
        self.setnew(x,y)        
    def lup(self,x,y):
        self.drawing = False
        self.addrect(x,y)
    def mmove(self,x,y):
        if self.drawing:
            self.setnew(x,y)
    def ldclick(self,x,y):
        self.delrect(x,y)




def loaddirs(self):
        dirlist = onlydirs()        
        for idx,d in enumerate(dirlist):
            pass

class pagedealer():
    def __init__(self):
        self.idx = 0
        
        #self.mode = "bubble"
        self.mode = 2
        
        self.rect = {}
        self.rectidxs=[2,3,4,5,6]#6 for all del mode
        for i in self.rectidxs:
            self.rect[i]={}
        self.rectcolor = {}        
        self.rectcolor[2] = (255,0,255)
        self.rectcolor[3] = (0,180,255)
        self.rectcolor[4] = (0,255,0)
        self.rectcolor[5] = (170,70,170)
        self.rectcolor[6] = (0,0,255)
        
        self.rectname = {}
        self.rectname[2] = "bubble"
        self.rectname[3] = "comment"
        self.rectname[4] = "deforme"
        self.rectname[5] = "effect"
        self.rectname[6] = "notused"#as for file io.
        
        
        self.imgname = {}
        self.img = {}
        #self.imgraw = {}
        
        self.idx = 0
        self.idxmin = 0
        self.idxmax = 0
        self.afterpage = True
        self.looper = True
        self.winname = 'bubbles'
        self.unitsize={}
        self.dirname = ''
        
        self.fps = 30
        
        
    def loadimgs(self,dirname):
        self.dirname = dirname
        imglist = getimgs(dirname)        
        if len(imglist)==0:
            print('imglist empty!')
            idx = 0            
            self.img[idx] = np.zeros( (500,500,3),np.uint8)
            self.unitsize[0] = self.img[0].shape[1]//15
            for ridx in self.rectidxs:
                imgw = self.img[idx].shape[1]
                self.rect[ridx][idx] = rectdealer(imgw)
        else:        
            self.idxmin = 0
            for idx, i in enumerate(imglist):
                self.idxmax = idx
                print(i)
                self.imgname[idx] = i
                img = imgload(i)
                self.img[idx] = np.ndarray.copy(img)
                #self.imgraw[idx] = np.ndarray.copy(img)#more realable maybe..            
                
                self.unitsize[idx] = self.img[idx].shape[1]//15
                for ridx in self.rectidxs:
                    imgw = self.img[idx].shape[1]
                    self.rect[ridx][idx] = rectdealer(imgw)
        self.idx = 0
        
    def updateimg(self):
        self.fps = 30
    
    def up(self,x,y):
        if self.idx < self.idxmax:
            self.idx+=1
            print(self.idx)
        self.afterpage = True
    def down(self,x,y):
        if self.idx > self.idxmin:
            self.idx-=1
            print(self.idx)
        self.afterpage = True
    def getimg(self):
        idx = self.idx
        img = self.img[idx]#it occurs re-write. use copy instead.!
        img = np.ndarray.copy(img)
        img = self.drawfliprect(img)
        linew = self.getlinew(img)
        #draws all rects.
        for i in self.rectidxs:
            colornow = self.rectcolor[i]
            for no,r in enumerate(self.rect[i][idx].rectlist):
                o,n = r                
                cv2.rectangle(img,o,n,colornow,linew)
                uu = self.unitsize[self.idx]
                cv2.putText(img, str(no), o,cv2.FONT_HERSHEY_DUPLEX,uu//40,colornow,linew,cv2.LINE_4)
        #now dragging
        if self.rect[self.mode][idx].drawing:
            ix,iy = self.rect[self.mode][idx].oldcord
            nx,ny = self.rect[self.mode][idx].newcord
            cv2.rectangle(img,(ix,iy),(nx,ny),(0,0,255),linew)
        
        uu = self.unitsize[self.idx]
        cv2.rectangle(img,(0,0),(uu,uu),(0,0,255),-1)
        return img
    
    def getlinew(self,img):
        return img.shape[1]//200
    
    def drawfliprect(self,img):
        linew = self.getlinew(img)
        
        pagerects = self.getfliprect(img)
        for r in pagerects:
            a,b = r
            cv2.rectangle(img,a,b,(255,0,80),linew)
        #select button now
        a,b = pagerects[self.mode]
        color = self.rectcolor[self.mode]
        cv2.rectangle(img,a,b,color,linew)
        return img

    #as now, window bad since event outs original img's cord.
    #x,y,w,h = cv2.getWindowImageRect('speedbubble')
    def getfliprect(self,img):
        imh,imw,d = img.shape        
        window_w = imw
        window_h = imh
        pagerectw = window_w//15
        pagerecth = window_h//15
        pagey = window_h//2
        flipa = [(0,pagey-pagerecth),(pagerectw,pagey+pagerecth)]
        flipb = [(window_w-pagerectw,pagey-pagerecth),(window_w,pagey+pagerecth)]
        pagerects = [ flipa, flipb ]
        
        #mode buttons.
        w = window_w//15
        h = window_w//15
        for i in self.rectidxs:            
            ba = (w*(i),0)
            bb = (w*(i+1),h)
            bubble = [ba,bb]
            pagerects.append(bubble)
        
        return pagerects
    
    def lclick(self,x,y):
        #self.page[self.idx].lclick(x,y) #rectdealer
        self.rect[self.mode][self.idx].lclick(x,y)
        self.afterpage = False
    def mmove(self,x,y):
        self.rect[self.mode][self.idx].mmove(x,y) #rectdealer
        self.updateimg()
    def lup(self,x,y):
        #if it's on button, don't draw.
        img = self.img[self.idx]
        for idx,i in enumerate(self.getfliprect(img)):
            area = i
            if iscoll(x,y,area):
                self.rect[self.mode][self.idx].drawing = False
                self.updateimg()
                return False#escape below.
        
        if not self.afterpage:
            self.rect[self.mode][self.idx].lup(x,y) #rectdealer
        self.updateimg()
        
    def ldclick(self,x,y):
        uu = self.unitsize[self.idx]
        if x<uu and y<uu:
            self.loopstop()
            return False
        img = self.img[self.idx]
        for idx,i in enumerate(self.getfliprect(img)):
            area = i
            if iscoll(x,y,area):
                if idx==0:                
                    self.down(x,y)#for no rect occur.
                    self.updateimg()
                    return False
                elif idx==1:                
                    self.up(x,y)
                    self.updateimg()
                    return False
                else:
                    self.mode = idx
                    self.updateimg()
                    return False            
        
        self.rect[self.mode][self.idx].ldclick(x,y) #rectdealer
        
        #last button del all rects
        if self.mode == self.rectidxs[-1]:
            for ridx in self.rectidxs:
                self.rect[ridx][self.idx].ldclick(x,y) #rectdealer            
        self.updateimg()

    def postloop(self):# exit or esc or dblclick
        #print(self.img
        tnt = tnf()
        tnt.show()
        
        imgs_origin = []
        imgs_letter = []
        
        recttext = {}
        def setrecttext(idx):
            if recttext.get(idx) == None:
                recttext[idx] = []#for each rects.
        
        bubblepath = os.path.join(self.dirname,"bubble")
        os.makedirs( bubblepath ,exist_ok=True)
        
        originpath = os.path.join(bubblepath, "origin")
        letterpath = os.path.join(bubblepath, "brush")
        os.makedirs( originpath ,exist_ok=True)
        os.makedirs( letterpath ,exist_ok=True)
        
        def originsave(i,no,img):
            idxname = self.rectname[i]
            #idxpath = os.path.join(originpath,idxname)
            #os.makedirs( idxpath ,exist_ok=True)
            imname = "{}_{}.png".format( idxname, no)
            path = os.path.join(originpath,imname)
            cv2.imwrite(path,img)
        def lettersave(i,no,img):
            idxname = self.rectname[i]
            #idxpath = os.path.join(letterpath,idxname)
            #os.makedirs( idxpath ,exist_ok=True)
            imname = "{}_{}.png".format( idxname, no)
            path = os.path.join(letterpath,imname)
            cv2.imwrite(path,img)
        
        def txtsave(recttext, bubble_idx =2):#sametxt,diff.name.
            basiclen = self.idxmax+1
            for i, textrows in recttext.items():
                if len(textrows)>basiclen:
                    idxname = self.rectname[i]
                    if i == bubble_idx:
                        txtname = '{}\\{}_{}.txt'.format(bubblepath,idxname,"japanese")
                        text2txt(textrows,txtname )
                    txtname = '{}\\{}_{}.txt'.format(bubblepath,idxname,"input")
                    text2txt(textrows,txtname )
            #get bubble txt name.
            idxname = self.rectname[bubble_idx]
            txtname = '{}\\{}_{}.txt'.format(bubblepath,idxname,"input")
            return txtname#trans.txt.
        
        # wheter brush mode do or dont
        #export-import mode or instant trans mode
        for idx in range(self.idxmax+1):# 0-4 to 5.
            img = self.img[idx]
            for i in self.rectidxs: #loop by rects. bubble, comment ...                
                textrows = []
                setrecttext(i)
                for no,r in enumerate(self.rect[i][idx].rectlist):
                    print('imgstart',i,r)
                    cropped = cropimg(img,r)
                    imgs_origin.append(cropped)#get original crop.. later, by idx.
                    originsave(i,no,cropped)
                    b = brusher(cropped)
                    
                    #-----------img pre-process
                    h,w,n =cropped.shape
                    mult = 400/w
                    sizerule = int(w*mult),int(h*mult)
                    cropped = cv2.resize(cropped, sizerule, interpolation = cv2.INTER_LINEAR)
                    cropped = cv2.erode(cropped,(3,3),iterations=1)
                    
                    #sharpening_1 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
                    sharpening_2 = np.array([[-1, -1, -1, -1, -1],
                             [-1, 2, 2, 2, -1],
                             [-1, 2, 9, 2, -1],
                             [-1, 2, 2, 2, -1],
                             [-1, -1, -1, -1, -1]]) / 9.0
                    cropped = cv2.filter2D(cropped, -1, sharpening_2)
                    #print(cropped.shape)
                    #showme = np.ndarray.copy(cropped)
                    #cv2.imshow( 'see',showme)
                    #infloop                
                    #-----------img pre-process
                    
                    cropped = b.show()
                    #cv2.imshow( 'see',cropped)
                    
                    #---add changed img. export.. just export.?no.
                    backsize = w,h#lucky!
                    lettered = cv2.resize(cropped, backsize, interpolation = cv2.INTER_LINEAR)
                    imgs_letter.append(lettered)
                    #lettered img write
                    lettersave(i,no,lettered)
                    
                    texts = img2text(cropped)
                    print('img2text done')
                    
                    t = text2row(texts)
                    textrows.append(t)
                textrows.append('---pageidx {}'.format(idx) )
                recttext[i].extend(textrows)        
        
        txtname = txtsave(recttext)#returns nameof txt.
        os.system(txtname)#open input. note cmd uses backslash. '/' can't.
        print('done')
        
        
        
    def makewindow(self):
        cv2.namedWindow(self.winname,cv2.WINDOW_NORMAL  )#seems only one, but works only resizeable
        cv2.setMouseCallback(self.winname,self.mousehandle)
        window_w = 400
        window_h = 700
        cv2.resizeWindow(self.winname,window_w,window_h)    
        
    def loopstop(self):
        self.looper = False
        
    def loop(self):
        img = self.getimg()
        cv2.imshow(self.winname, img)
        while self.looper:
            if cv2.getWindowProperty(self.winname, 0) ==-1:
                self.loopstop()
                #return False#prevent below run. bubble shown up last..
                break
            img = self.getimg()
            cv2.imshow(self.winname, img)
            
            
            if self.fps>1:
                self.fps -= 0.3
            sleepms = int(1000/self.fps)
            #print(self.fps)#wonderful!
            k = cv2.waitKey(sleepms) & 0xFF
            if k == 27:        # esc를 누르면 종료
                self.loopstop()
                break
        cv2.destroyWindow(self.winname)
        self.postloop()
        return self
        
    def mousehandle(self,event, x,y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN: #마우스를 누른 상태
            self.lclick(x,y)
            
        elif event == cv2.EVENT_MOUSEMOVE: # 마우스 이동
            self.mmove(x,y)        

        elif event == cv2.EVENT_LBUTTONUP:
            self.lup(x,y)
        
        elif event == cv2.EVENT_LBUTTONDBLCLK:
            self.ldclick(x,y)

def brush(img,point):
    x,y=point
    img[ y-20:y+20,x-20:x+20,:]

class brusher():
    def __init__(self,img):
        h,w,non = img.shape
        vert_ref = h/300        
        w = int(w/vert_ref)
        h = int(h/vert_ref)
        img = cv2.resize(img, (w,h), interpolation = cv2.INTER_LINEAR)
        
        self.img = img
        self.showme = np.ndarray.copy(self.img)
        self.huriloop = True
        self.radius = img.shape[0]//30
        self.drawing = False
        self.lastpoint = 0,0
        self.winname = 'brush'
            
    def breakwindow(self):
        self.huriloop = False        
    
    def hurigana(self,event, x,y, flags, param):
        if event == cv2.EVENT_RBUTTONDOWN:
            pass
            #self.breakwindow()
        elif event == cv2.EVENT_MOUSEMOVE: # 마우스 이동
            if self.drawing:
                cord = x,y
                cv2.circle(self.showme,cord, self.radius,(255,255,255),-1)
            #self.lastpoint = x,y
            #print(lastpoint)
        elif event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
        elif event == cv2.EVENT_LBUTTONDBLCLK:
            self.showme = np.ndarray.copy(self.img)
        elif event == cv2.EVENT_MOUSEHWHEEL:
            pass
#             self.radius+=2
#             if self.radius<4:
#                 self.radius = 4
#             elif self.radius>100:
#                 self.radius = 100
    def show(self):
        self.huriloop = True
        winname = self.winname
        cv2.namedWindow(winname)
        cv2.setMouseCallback(winname,self.hurigana)
        cv2.imshow(winname,self.showme)
        
        while self.huriloop:
            if cv2.getWindowProperty(self.winname, 0) ==-1:
                break
            cv2.imshow(winname,self.showme)
            cv2.waitKey(20)
        cv2.destroyWindow(self.winname)
        return self.showme

#img = imgload('1.jpg')
#imgold=np.ndarray.copy(img)
#imh,imw,d=img.shape
        
#img = np.zeros((imh,imw,3), np.uint8)
#cv2.namedWindow('image')
#cv2.setMouseCallback('image',draw_circle)

#window_w = 800
#window_h = 1000

#cv2.namedWindow('speedbubble',flags = cv2.WINDOW_NORMAL&cv2.WINDOW_KEEPRATIO&cv2.WINDOW_GUI_EXPANDED )
#cv2.resizeWindow('speedbubble',window_w,window_h)
#cv2.resizeWindow('speedbubble',imw,imh)

#cv2.rectangle(img,(600, 100), (800, 600),(0,0,80),5)
#cv2.line(img, (0,900), (80,1100), (255, 0, 0), 5)



# Mouse Callback함수
def mousehandle(event, x,y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN: #마우스를 누른 상태
        page.lclick(x,y)
        
    elif event == cv2.EVENT_MOUSEMOVE: # 마우스 이동
        page.mmove(x,y)        

    elif event == cv2.EVENT_LBUTTONUP:
        page.lup(x,y)
    
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        page.ldclick(x,y)




    
    

#     t = timeprinter()
#     l = loopcounter()
# 
#     while True:    
#         img = page.getimg()
#         cv2.imshow('speedbubble', img)    
#         
#         #l.loop()
#         #t.timeprint(l)
#         
#         k = cv2.waitKey(1) & 0xFF
# 
#         #if k == ord('m'):    # 사각형, 원 Mode변경
#             #mode = not mode
#         if k == 27:        # esc를 누르면 종료
#             break
# 
#     cv2.destroyAllWindows()

#img = imgload('1.jpg')
#rect = rectdealer(img)



      


if __name__ == '__main__':
    page = pagedealer()
    page.loadimgs('as')
    page.makewindow()
    page.loop()
    
