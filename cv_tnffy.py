import cv2
import numpy as np

# def mousehandle(event, x,y, flags, param):
#     if event == cv2.EVENT_LBUTTONDOWN: #마우스를 누른 상태
#         page.lclick(x,y)
#     elif event == cv2.EVENT_MOUSEMOVE: # 마우스 이동
#         page.mmove(x,y)
#     elif event == cv2.EVENT_LBUTTONUP:
#         page.lup(x,y)
#     elif event == cv2.EVENT_LBUTTONDBLCLK:
#         page.ldclick(x,y)
#
# def makewindow(self):
#     cv2.namedWindow(self.winname,cv2.WINDOW_NORMAL  )#seems only one, but works only resizeable
#     cv2.setMouseCallback(self.winname,self.mousehandle)
#     window_w = 400
#     window_h = 700
#     cv2.resizeWindow(self.winname,window_w,window_h)
#
#
# cv2.namedWindow('image')
# cv2.setMouseCallback('image',mousehandle)







class Bwindow():
    def __init__(self, w=400, h=300, winname='Bwindow'):
        self.w = w
        self.h = h
        self.img = np.zeros((h,w,3), np.uint8)
        self.winname = winname
        self.looper = True
        self.fps = 30

        self.Blist = []
        self.trans_w = 1
        self.trans_h = 1
        self.return_var = None

        self.key_esc = 27

    def run(self):
        self.show()
        self.loop()
        return self.postloop()

    def show(self):
        winname = self.winname
        w = self.w
        h = self.h
        cv2.namedWindow(winname,cv2.WINDOW_NORMAL)
        cv2.resizeWindow(winname,w,h)
        cv2.setMouseCallback(winname, self.mousehandle)

    #----------------- event listner
    def mousehandle(self,event, x,y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.LBUTTONDOWN(event, x,y, flags, param)
        elif event == cv2.EVENT_MOUSEMOVE:
            self.MOUSEMOVE(event, x,y, flags, param)
        elif event == cv2.EVENT_LBUTTONUP:
            self.LBUTTONUP(event, x,y, flags, param)
        elif event == cv2.EVENT_LBUTTONDBLCLK:
            self.LBUTTONDBLCLK(event, x,y, flags, param)


    def LBUTTONDOWN(self,event, x,y, flags, param):
        for B in self.Blist:
            B.click(x,y)
        self.LBUTTONDOWN_post(x,y)
    def MOUSEMOVE(self,event, x,y, flags, param):
        self.fpsreset()
        for B in self.Blist:
            B.move(x,y)
        self.MOUSEMOVE_post(x,y)
    def LBUTTONUP(self,event, x,y, flags, param):
        for B in self.Blist:
            B.unclick(x,y)
        self.LBUTTONUP_post(x,y)
    def LBUTTONDBLCLK(self,event, x,y, flags, param):
        False
        self.LBUTTONDBLCLK_post(x,y)

    #those for just use x,y. simply.
    def LBUTTONDOWN_post(self,x,y):
        0
    def MOUSEMOVE_post(self,x,y):
        0
    def LBUTTONUP_post(self,x,y):
        0
    def LBUTTONDBLCLK_post(self,x,y):
        0

    #abstracted add-func-function. works great!
    def add_lbdown(self,text,func):
        LBUTTONDOWN_tmp = self.LBUTTONDOWN_post
        def LBUTTONDOWN_new(x,y):
            LBUTTONDOWN_tmp(x,y)
            for B in self.Blist:
                if B.coll(x,y) and B.text == text:
                    func(self,B)
        self.LBUTTONDOWN_post = LBUTTONDOWN_new
    def add_mhover(self,text,func):#note, it's hover, when cursor on button..
        MOUSEMOVE_tmp = self.MOUSEMOVE_post
        def MOUSEMOVE_new(x,y):
            MOUSEMOVE_tmp(x,y)
            for B in self.Blist:
                if B.coll(x,y) and B.text == text:
                    func(self,B)
        self.MOUSEMOVE_post = MOUSEMOVE_new
    def add_lbup(self,text,func):
        LBUTTONUP_tmp = self.LBUTTONUP_post
        def LBUTTONUP_new(x,y):
            LBUTTONUP_tmp(x,y)
            for B in self.Blist:
                if B.coll(x,y) and B.text == text:
                    func(self,B)
        self.LBUTTONUP_post = LBUTTONUP_new
    def add_lbdbl(self,text,func):
        LBUTTONDBLCLK_tmp = self.LBUTTONDBLCLK_post
        def LBUTTONDBLCLK_new(x,y):
            LBUTTONDBLCLK_tmp(x,y)
            for B in self.Blist:
                if B.coll(x,y) and B.text == text:
                    func(self,B)
        self.LBUTTONDBLCLK_post = LBUTTONDBLCLK_new


    #-----------global event, not button
    #orignal move event. compared hover.
    def add_mmove(self,func):
        MOUSEMOVE_tmp = self.MOUSEMOVE_post
        def MOUSEMOVE_new(x,y):
            MOUSEMOVE_tmp(x,y)
            func(self,x,y)
        self.MOUSEMOVE_post = MOUSEMOVE_new

    def add_loopstop(self,func):
        loopstop_tmp = self.loopstop
        def loopstop_new():
            loopstop_tmp()
            func(self)
        self.loopstop = loopstop_new
    #----------------- event listner


    #-----------------loop stuffs

    def key_wait(self,ms):
        return cv2.waitKey(ms) & 0xFF
    def img_show(self,img):
        cv2.imshow( self.winname, img)
    def img_resize(self,img,size):
        return cv2.resize(img, size, interpolation = cv2.INTER_LINEAR)
    def img_cover(self,big,small,a,b):
        bh,bw,bd = big.shape
        sh,sw,sd = small.shape
        if bh<sh or bw<sw or bd!=sd:
            return big
        #for safe cause. simple,fine.
        x1,y1 = a
        x2,y2 = b
        print(a,b)
        try:
            big[ y1:y2, x1:x2, :] = small
        except:
            print('img cover size not fit !')
            pass#size fail
        return big
    def img_copy(self):
        return np.ndarray.copy(self.img)
    def img_shape(self,img):
        return img.shape
    def img_rgba2rgb(self,img):
        return cv2.cvtColor(img,cv2.COLOR_RGBA2RGB)
    def window_alive(self):
        return cv2.getWindowProperty(self.winname, 0) ==-1
    def window_destroy(self):
        cv2.destroyWindow(self.winname)

    def fpsreset(self):
        self.fps = 30
    def loop(self):
        while self.looper:
            if self.window_alive():
                self.loopstop()
                break

            img = self.img_copy()
            self.drawB(img)
            self.img_show(img)

            if self.fps>1:
                self.fps -= 0.3
            sleepms = int(1000/self.fps)
            k = self.key_wait(sleepms)
            if k == self.key_esc:
                self.loopstop()
                break

        self.window_destroy()

    def postloop(self):
        return self.return_var

    def loopstop(self):
        self.looper = False



    def background(self,newimg,px,py,pw,ph):

        img = self.img
        ih,iw, dimention = self.img_shape(img)
        x = int(iw/10*px)
        y = int(ih/10*py)
        w = int(iw/10*pw)
        h = int(ih/10*ph)
        a = int(x-w/2), int(y-h/2)
        b = int(x+w/2), int(y+h/2)

        backsize = w,h#lucky!
        if dimention ==4:
            newimg = self.img_rgba2rgb(newimg)
        resized = self.img_resize(newimg,backsize)
        self.img = self.img_cover(img,resized, a,b)



    #------------------------button feature
    def Bfind(self,text):
        for B in self.Blist:
            if B.text == text:
                return B
    
    def addB(self, px,py,bw=1,bh=1,text ='button',value=None,hold = False,color=(255,255,0),thick=5,nocoll=False):
        ih,iw = self.img_shape(self.img)[:2]
        x = int(iw/10*px)
        y = int(ih/10*py)
        w = int(iw/10*bw)
        h = int(iw/10*bh)# for 1:1 rect.
        newB = self.B(x,y,w,h,text,value,hold,color,thick,nocoll)
        self.Blist.append( newB )
    def drawB(self,img):
        for B in self.Blist:
            B.draw(img)

    class B():
        def __init__(self,x,y,w,h,text,value,hold,color,thick, nocoll):
            self.x = x
            self.y = y
            self.w = w
            self.h = h
            
            #for x,y move
#             a = int(x-w/2), int(y-h/2)
#             b = int(x+w/2), int(y+h/2)
#             self.a = a
#             self.b = b
            self.color = color
            self.thick = thick

            self.text = text
            self.value = value
            self.text_color = (255,0,255)
            self.text_thick = 2

            self.pressed = False
            self.over = False
            self.hold = hold
            self.nocoll = nocoll
        def put_rect(self,img, a,b,color,thick):
            cv2.rectangle(img, a,b,color,thick)
        def put_text(self, img,text,textpos,font,size,color,thick,lineaa):
            cv2.putText(img,text,textpos,font,size,color,thick,lineaa)
        
        def getab(self):
            x = self.x
            y = self.y
            w = self.w
            h = self.h
            a = int(x-w/2), int(y-h/2)
            b = int(x+w/2), int(y+h/2)
            return a,b
        
        def draw(self, img):
            #----button shape
            a,b = self.getab()
            color,thick = self.color, self.thick
            if self.over:
                color = (255,0,255)
            self.put_rect(img, a,b,color,thick)
            if self.pressed:
                a = a[0]+thick,a[1]+thick
                b = b[0]-thick,b[1]-thick
                thick =-1
                color = (255,255,0)
                self.put_rect(img, a,b,color,thick)

            #----button img?

            #----button text
            text = self.text
            size = 1

            tx = self.x-len(text)*size*8
            ty = self.y+8
            textpos = int(tx),int(ty)

            color = self.text_color
            thick = self.text_thick
            font = cv2.FONT_HERSHEY_SIMPLEX
            lineaa = cv2.LINE_AA
            self.put_text(img,text,textpos,font,size,color,thick,lineaa)

        def coll(self,x,y):
            #print(self.x,x, self.w)
            if self.nocoll:
                return False
            return abs(x-self.x) < self.w/2 and abs(y-self.y) < self.h/2
        def click(self,x,y):
            if self.coll(x,y):
                self.pressed = not self.pressed
        def unclick(self,x,y):
            if self.coll(x,y):
                if not self.hold:
                    self.pressed = False
        def move(self,x,y):
            self.over = self.coll(x,y)

class tnf(Bwindow):
    def __init__(self,message='yes or no'):
        Bwindow.__init__(self)#self means activated assigned live class object.
        #Bwindow.addB(self,2,5,2,1,text = 'no',value=False, hold = True)
        self.addB(2,5,2,1,text = 'no',value=False)
        self.addB(8,5,2,1,text = 'yes',value =True)
        self.addB(5,2,4,1,text = message ,value =None, nocoll = True)
        #self.addB(8,5,2,1,text = 'yes',value =True) #maybe it better?.. yeah.

        #those func-in-func automatically inputs self, as first instance.. but not of in.
        #thanks to great add_eventfunc, don't use it.
#         LBUTTONDOWN = Bwindow.LBUTTONDOWN
#         def newlb(event, x,y, flags, param):#this in-event func not requires self in.
#             LBUTTONDOWN(self,event, x,y, flags, param)
#             for B in self.Blist:
#                 if B.coll(x,y):
#                     self.return_var = B.value
#                     self.loopstop()
#         self.LBUTTONDOWN = newlb
        def answerout(self,B):
            self.return_var = B.value
            self.loopstop()
        self.add_lbdown('yes', answerout)
        self.add_lbdown('no', answerout)
        #Bwindow.lup


class manyB(Bwindow):#just an example of hold, event function and return list. use your own!
    def __init__(self):
        Bwindow.__init__(self)

        self.return_var = []

        self.addB(2,5,2,1,text = '1',value=1, hold = True)
        self.addB(2,7,2,1,text = '2',value =2, hold = True)

        self.addB(8,5,2,1,text = 'randomcolor', hold = False,)
        self.addB(0.5,0.7,0.7,0.7,text = 'x', color = (0,150,255), )

        #self.add_mmove( lambda self,x,y: print(x,y) )


#------------behold, this below was function-add-func. but we made it more abstract...!

#         LBUTTONDOWN = self.LBUTTONDOWN
#         def newlb(event, x,y, flags, param):#this in-event func not requires self in.
#             LBUTTONDOWN(event, x,y, flags, param)
#             for B in self.Blist:
#                 if B.coll(x,y) and B.value == 'exit':
#                     self.loopstop()
#                 if B.coll(x,y) and B.value == 'rcolor':
#                     rcolor(B)
#         self.LBUTTONDOWN = newlb
        #Bwindow.lup

        def rcolor(self,button):#this self is not upper self. means just 2 args.
            #print(self.return_var)
            r=np.random.random()*255
            g=np.random.random()*255
            b=np.random.random()*255
            button.color = r,g,b
        self.add_lbdown("randomcolor",rcolor)

        self.add_lbdown("x",lambda s,b: s.loopstop() )
#------------just 2 lines.

#         loopstop = self.loopstop
#         def newlsp():
#             loopstop()#since it's form of object's func. prevent inf.loop..
#             for B in self.Blist:
#                 if B.pressed:
#                     self.return_var.append(B.value)
#         self.loopstop = newlsp
        def addlistvar(self):
            for B in self.Blist:
                if B.pressed:
                    self.return_var.append(B.value)
        self.add_loopstop(addlistvar)
#------------and more 1 line!

class sizer(Bwindow):
    def __init__(self):
        Bwindow.__init__(self, 600,900)
        s = 1.5
        self.addB(3,1,s,s,text = 'Erase')
        self.addB(5,1,s,s,text = 'Neon')
        self.addB(7,1,s,s,text = 'brush')
        
        s=1
        uu = int(self.w/10)
        self.addB(7.9,8.6,s,s,text = 'w-', value = -uu,)
        self.addB(4.5,8.9,s,s,text = 'add B')
        self.addB(9.2,8.6,s,s,text = 'w+', value = uu, )
        
        self.addB(7.9,9.4,s,s,text = 'h-', value = -uu,)
        self.addB(9.2,9.4,s,s,text = 'h+', value = uu, )
        
        for B in self.Blist:
            B.fixed = True
        def buttonmove(self,x,y):
            for B in self.Blist:
                if B.pressed and B.coll(x,y):
                    if not 'fixed' in dir(B):
                        B.x = x
                        B.y = y
        self.add_mmove( buttonmove )
        
        def prtxy(self,b):
            px = str(b.x/ self.w*10)[:3]
            py = str(b.y/ self.h*10)[:3]
            print( px,py )
        for B in self.Blist:
            self.add_lbdbl( B.text , prtxy )
        
        
        #make----------sizer
        def wsizech(self,b):
            B = self.Bfind('add B')
            B.w += b.value            
        self.add_lbdown( 'w+' , wsizech )
        self.add_lbdown( 'w-' , wsizech )
        
        def hsizech(self,b):            
            B = self.Bfind('add B')
            B.h += b.value
        self.add_lbdown( 'h+' , hsizech )
        self.add_lbdown( 'h-' , hsizech )
        
        #lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        lorem = 'Yume Nijino Hime Shiratori Elza Forte Mahiru Kasumi Ako Saotome Laura Sakuraba Yozora Kasumi'
        texts = lorem.split(' ')
        def addb(self,b):
            w = b.w
            h = b.h
            pw = int(w/ self.w*10)
            ph = int(h/ self.w*10)
            
            text = texts.pop()
            #text = 'new B'
            self.addB(5,5,pw,ph,text)
            self.add_lbdbl( text , prtxy )
        self.add_lbdown( 'add B', addb )

class painter(Bwindow):
    def __init__(self):
        Bwindow.__init__(self)

        self.brush_points = []

        #self.addB(2,5,2,1,text = 'brush+',value=1, hold = True)
        self.addB(2,5,2,1,text = 'brush+')
        self.addB(2,7,2,1,text = 'brush-')

        self.addB(8,5,2,1,text = 'color', hold = False,)
        self.addB(0.5,0.7,0.7,0.7,text = 'x', color = (0,150,255), )

        #self.add_mmove( lambda self,x,y: print(x,y) )


        def rcolor(self,button):#this self is not upper self. means just 2 args.
            #print(self.return_var)
            r=np.random.random()*255
            g=np.random.random()*255
            b=np.random.random()*255
            button.color = r,g,b
        self.add_lbdown("randomcolor",rcolor)

        self.add_lbdown("x",lambda s,b: s.loopstop() )

        def addlistvar(self):
            for B in self.Blist:
                if B.pressed:
                    self.return_var.append(B.value)
        self.add_loopstop(addlistvar)


if __name__ =='__main__':
    #a=tnf()
    #print(a.run())
    #a=manyB()
    #print(a.run())
    a=sizer()
    a.run()

# if __name__ =='__main__':
#     winname = 'tnfwindow'
#     a = tnfwindow(winname)
#     a.addB(2,5,2,1,text = 'no')
#     a.addB(8,5,2,1,text = 'yes')
#     print(a.show())
