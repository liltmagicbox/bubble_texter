def text2row(textlist):
    t = ''
    for text in textlist:
        t+=text+' '
    return t

def text2rows(textlist):
    textrows=[]
    t = ''
    for text in textlist:
        t+=text+' '
    textrows.append(t)
    return textrows

def text2txt(textrows,txtname):
    totxt = ''
    for r in textrows:
        totxt += r+'\n'    
    with open(txtname,'w',encoding='utf-8') as f:
        f.write(totxt)