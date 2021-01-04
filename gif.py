

import os
import subprocess
import sys
import tempfile
from PIL import ImageGrab
from PIL import Image

import time
import random

def grab(bbox=None, include_layered_windows=False, all_screens=False):

    offset, size, data = Image.core.grabscreen_win32(include_layered_windows, all_screens)
    im = Image.frombytes(
        "RGB",
        size,
        data,
        # RGB, 32-bit line padding, origin lower left corner
        "raw",
        "BGR",
        (size[0] * 3 + 3) & -4,
        -1,
        )
    if bbox:
            x0, y0 = offset
            left, top, right, bottom = bbox
            im = im.crop((left - x0, top - y0, right - x0, bottom - y0))
            
    return im


capturesec=input( 'how long sec?')
shots = int( int(capturesec)*1000/60 )

def capture(nan): #bbox=[0,0,600,600]
    global images
    print('start capture')
    #print(bbox)
    
    global images
    #boxrange= (600,600)
    #bbox=(0,0,boxrange[0],boxrange[1])
    global capturesize
    bbox = capturesize
    images=[]
    for i in range(shots):
        time.sleep(0.034)
        images.append(grab(bbox))
        if len(images)==30:print('30picsnow')
    print('done capture')

    #global states #what???>??!?!???
    states= 'Recording Done'
    statetext.SetLabel( states )
    

def savegif(nan):
    global images
    print('saving')
    li = os.listdir()
    i=1
    fname = 'saved'+str(i)+'.gif'
    while fname in li:
        i+=1
        fname = 'saved'+str(i)+'.gif'
        
    images[0].save( fname,
               save_all=True, append_images=images[1:], optimize=False, duration=60, loop=0)
    print('savedone')

    #global states
    states= 'SAVE Done'
    statetext.SetLabel( states )




#https://docs.wxpython.org/wx.Window.html

import wx      
app = wx.App()
frame = wx.Frame(None, -1, 'win.py' ,)
frame.SetSize(600,300,300,200)

frame.ToggleWindowStyle(wx.STAY_ON_TOP)


capturesize = [0,0,600,600]

print('ha')
states='notdone'

def onButton(event):
    global capturesize
    bob=capturesize
    prit ("rec pressed.")
    capture( bbox=bob ) #bug fixed !
    print('done')
    #seems func calls func, dosnt show it!
    
    
    
    
    
    
def saveButton(event):
    global states
    print ("save pressed.")
    savegif()
    states = 'savedone'
    statetext.SetLabel( states )




def getorigin(e):
    global capturesize
    global origin
    global end
    pos=frame.GetScreenPosition()
    print(pos)
    capturesize[0]=pos[0]
    capturesize[1]=pos[1]
    origin=str( capturesize[:2] )
    oritext.SetLabel( origin )
   
def getend(e):
    global capturesize
    global origin
    global end
    pos=frame.GetScreenPosition()
    #print( pos )
    capturesize[2]=pos[0]
    capturesize[3]=pos[1]
    print(capturesize)
    
    #origin=str( capturesize[:2] )
    end=str( capturesize[2:] )
    #oritext.SetLabel( origin )
    endtext.SetLabel( end )
    
origin=str( capturesize[:2] )
end=str( capturesize[2:] )
#states= 'recdone'

panel = wx.Panel(frame, wx.ID_ANY)

button1 = wx.Button(panel, wx.ID_ANY, 'capture', (50, 30)) #,(50, 30)
button1.Bind(wx.EVT_BUTTON, capture)

button2 = wx.Button(panel, wx.ID_ANY, 'save', (50, 80))
button2.Bind(wx.EVT_BUTTON, savegif)

button3 = wx.Button(panel, wx.ID_ANY, 'origin', (150, 30))
button3.Bind(wx.EVT_BUTTON, getorigin)

button4 = wx.Button(panel, wx.ID_ANY, 'end', (150, 80))
button4.Bind(wx.EVT_BUTTON, getend)

oritext = wx.StaticText(panel, pos=(160,10), size=(100,20) , label=origin)
endtext = wx.StaticText(panel, pos=(160,110), size=(100,20) ,label= end)

statetext = wx.StaticText(panel, pos=(5,5), size=(100,20) ,label= states)


frame.Show()
app.MainLoop()
