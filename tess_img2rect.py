import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# class transbox():
#     def __init__(self):
#         self.

#cong = r'--oem 3 --psm 6 outputbase digits'
#cong = r'--oem 3 --psm 5 -l jpn_vert -c preserve_interword_spaces=0 lstm_use_matrix=0 paragraph_text_based=0 textord_old_baselines=0'
cong = r'--psm 5 -l jpn'

#img2text('./0.jpg')
'''
img = cv2.imread('./as/0.jpg')
img2text(img)
'''
def img2text(img):
    textlist = []
    #img = np.ndarray.copy(img)
    print('tess_starting..')
    boxs= pytesseract.image_to_data(img,config = cong).splitlines()
    for i,b in enumerate(boxs):
        b = b.split('\t')
        if i==0 or b[11]=="":
            continue
        x1,y1,x2,y2 = int(b[6]),int(b[7]),int(b[8]),int(b[9])
        #print(x1,y1,x2,y2)
        text = b[11]
        textlist.append(text)
        print('trans',text)        
        #cv2.rectangle(img, (x1,y1), (x1+x2,y1+y2) ,(0,255,0) )#color,thickness
        #cv2.putText(img, text, (x1,y1), cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255) )        
    print('textlist',textlist)
#     with open('tmp.txt','a',encoding='utf-8') as f:
#             f.write("\nbefore return")
    return textlist

if __name__=='__main__':
    img = cv2.imread('./as/0.jpg')    
    #img = cv2.imread('d.png')
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #print( pytesseract.image_to_string(img) )
    #print( pytesseract.image_to_boxes(img) )

    #boxs= pytesseract.image_to_boxes(img).splitlines()

    boxs= pytesseract.image_to_data(img,config = cong).splitlines()
    imh,imy,no = img.shape#note y,x.
    for i,b in enumerate(boxs):
        #print(b)
        b = b.split('\t')
        if i==0 or b[11]=="":
            continue
        x1,y1,x2,y2 = int(b[6]),int(b[7]),int(b[8]),int(b[9])
        #print(x1,y1,x2,y2)
        text = b[11]
        print(text)
        #cv2.rectangle(img, (x,y), (x+w,y+h) ,(0,0,255),1 )#color,thickness
        cv2.rectangle(img, (x1,y1), (x1+x2,y1+y2) ,(0,255,0) )#color,thickness
        cv2.putText(img, text, (x1,y1), cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255) )
    cv2.imshow('result',img)
    cv2.waitKey(0)
