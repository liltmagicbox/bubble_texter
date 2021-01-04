import os
def onlydirs():
    dirs = []
    for i in os.listdir():
        if os.path.isdir(i):
            dirs.append(i)
    return dirs

import glob

def getimgs(path):
    #a = glob.glob('./{}/*.jpg'.format(path))
    #b = glob.glob('./{}/*.png'.format(path))
    #a.extend(b)
    extlist = ['.jpg','.png']
    #print(path)
    imglist = []
    cwd = os.getcwd()
    for i in os.listdir(path):
        if os.path.splitext(i)[1].lower() in extlist:
            fname = os.path.join(cwd,path,i)
            imglist.append(fname)        
    return imglist

def iscoll(x,y,area):
    if len(area) ==2:#means rect. 2 points        
        x1,y1 = area[0]
        x2,y2 = area[1]
        return x>x1 and x<x2 and y>y1 and y<y2



from time import time,sleep

class timeprinter():
    def __init__(self):
        self.oldt = time()
        self.print = True
    def timeprint(self,counter):
        newt = time()
        if newt-self.oldt>1:
            self.oldt = newt
            counter.getfps()
            #print(newt,counter.fps)
            if self.print:
                print(counter.fps,"fps")
            
class loopcounter():
    def __init__(self):
        self.count = 0
        self.oldcount = 0
        self.fps = -1
        self.sleepmax = 0.020
        self.sleepmin = 0.002
        self.sleeptime = 0.006
        self.fpstarget = 30
    def loop(self):
        sleep(self.sleeptime)# 20 for 30fps. 6 for 60fps, but 30 2nd monitor.?
        self.count+=1        
    def getfps(self):
        dframe = self.count - self.oldcount
        self.oldcount = self.count
        self.fps = dframe
        self.sleeptime -= (self.fpstarget - self.fps)*0.0003
        #print(self.sleeptime) #to see sleeptime change. 0.0003 fine.
        if self.sleeptime > self.sleepmax:
            self.sleeptime = self.sleepmax
        elif self.sleeptime < self.sleepmin:
            self.sleeptime = self.sleepmin