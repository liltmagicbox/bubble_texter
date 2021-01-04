
# rectlistidx = 0
# rectpage = {}
# rectpage[0]=[]
# rectlistidx,rectlist,rectpage

class remona():    
    def __init__(self):
        self.price = 2000
    def show(self):
        print(self.price)
a=remona()
a.show()

class rectpage():
    def __init__(self):
        self.idx = 0
        self.page = {}
        self.page[self.idx]=[]
        self.rectlist=[]
    def up(self):
        self.idx+=1
        self.load()
    def down(self):
        self.idx-=1
        self.load()
    def load(self):
        if self.page.get(self.idx) == None:
            self.page[self.idx] = []
        self.rectlist = self.page[self.idx]
    def save(self):
        self.page[self.idx] = self.rectlist
a=rectpage()