from copy import copy

def maxlen(texts):    
    return len(''.join(texts))+len(texts)

def splitted(text, fontsize, box, multiply=1,multi_vert=1, minsize=3, debug = 0 ):
    'fits box, change fontsize. debug to see rows.'
    size = fontsize
    wide,long = box
    texts = text.split(' ')
    row = 1
    while True:
        textrow = []
        for r in range(row):
            textrow.append([])
        
        splits = copy(texts)
        for i in range(row):
            tmprow = []
            while maxlen( tmprow +[splits[0]] )*size*multiply < wide:
                tmprow.append( splits.pop(0) )
                if len(splits) ==0:
                    break
            if debug:print(row,tmprow)
            textrow[i] = tmprow
            
            if len(splits)==0:
                break
        
        
        if len(splits) !=0:
            if (row+1)*size/multi_vert < long:
                row+=1
            else:
                size=size*0.9
                if debug:print(row,'size',size)
            if debug:print('--next!--')
        else:
            break
    
    if size < minsize:
        size = minsize
    size = int(size)
    textlist = [x for x in textrow if x != []]
    mergelist=[]
    for idx,texts in enumerate(textlist):
        rowtext=''
        for text in texts:
            rowtext += text+' '
        rowtext = rowtext[:-1]# last space del
        mergelist.append( rowtext )
    return size,mergelist
        
if __name__ == "__main__":
    size = 30
    wide = 100
    long = 150
    box = wide,long
    #text = '앗! 에마쨩은 이런 표정도 짓는구나. 평소엔 늘 활기찬 모습만 봐 왔는데.'
    text = "그렇지 않다 뭐. 마이카 쨩이 모르는 모습도 많다구요!"
    newsize,textrow = splitted(text,size,box)
    print( newsize, textrow )