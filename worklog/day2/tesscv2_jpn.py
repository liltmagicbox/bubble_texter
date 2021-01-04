import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"



img = cv2.imread('d.png')
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#print( pytesseract.image_to_string(img) )
#print( pytesseract.image_to_boxes(img) )

#boxs= pytesseract.image_to_boxes(img).splitlines()
#cong = r'--oem 3 --psm 6 outputbase digits'
#cong = r'--oem 3 --psm 5 -l jpn_vert -c preserve_interword_spaces=0 lstm_use_matrix=0 paragraph_text_based=0 textord_old_baselines=0'
cong = r'--psm 12 -l jpn'
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
