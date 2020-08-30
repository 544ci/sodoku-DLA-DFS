import random
import math
import pygame
import time

class node:
    def __init__(self,value,active,x,y,up,down,left,right):
        self.position=(x,y)
        self.up=up
        self.down=down
        self.left=left
        self.right=right
        self.value=value
        self.active=active

   
    def addBottom(self,node):
        if(self.down==None):
            self.down=node
            node.up=self
        else:
            x=self
            while(x.down!=None):
                x=x.down
            x.down=node
            node.up=x
        return(self)

    def addRight(self,node):
        if(self.right==None):
            self.right=node
            node.left=self
        else:
            x=self
            while(x.right!=None):
                x=x.right
            x.right=node
            node.left=x
        return(self)



def updateValues(list):
    temp=list
    while(temp!=None):
        temp1=temp.down
        count=0
        while(temp1!=None):
            if(temp1.active==1):
                count+=1
            temp1=temp1.down
            
        temp.value=count
        temp=temp.right


def ll():
    x=node(11,1,-1,-1,None,None,None,None)
    for i in range(0,324):
        x.addRight(node(9,1,i,-1,None,None,None,None))
    return x


def constraint1(list):
    temp=list
    ii=0
    for i in range(0,81):
        jj=0
        for j in range(0,9):
            temp.addBottom(node(0,1,temp.position[0],jj+ii,None,None,None,None)) 
            jj+=1 
        ii+=9
        temp=temp.right

        
    return(list)

def constraint2(list):
    temp=list
    while(temp.position[0]!=81):
        temp=temp.right
        
    
    s=0
    for i in range(0,9):
        off=0
        for j in range(0,9):    
            t=0
            for k in range(0,9):
                temp.addBottom(node(0,1,temp.position[0],s+off+t,None,None,None,None))
                t=t+9
            temp=temp.right

            off=off+1
        s=s+81
    return (list)
    
def constraint3(list):
    temp=list
    while(temp.position[0]!=162):
        temp=temp.right
    ii=0
    for i in range(81):
        jj=0
        for j in range(9):
            temp.addBottom(node(0,1,temp.position[0],ii+jj,None,None,None,None))
            jj+=81
        temp=temp.right
        ii+=1
    return (list)

def constraint4(list):
    temp=list
    while(temp.position[0]!=243):
        temp=temp.right
    mm=0
    for m in range(0,3):
        ll=0
        for l in range(0,3):
            ii=0
            for i in range(0,9):
                jj=0
                for j in range(0,3):
                    kk=0
                    for k in range(0,3):
                        temp.addBottom(node(0,1,temp.position[0],kk+jj+ii+ll+mm,None,None,None,None))
                        kk+=9
                    jj+=81
                temp=temp.right
                ii+=1
            ll+=27
        mm+=243
    return(list)
        

def join1(list):
    for i in range(729):
        cols=[]
        temp=list
        while(temp!=None):
            temp1=temp.down
            while(temp1!=None):
                if(temp1.position[1]==i):
                    cols.append(temp1)
                temp1=temp1.down
            temp=temp.right    

        cols[0].left=None
        for j in range(len(cols)-1):
            cols[j].right=cols[j+1]
            cols[j+1].left=cols[j]
        cols[len(cols)-1].right=None





def coverIndex(list,x,y):
    temp=list
    while temp.position[0]!=x :
        temp=temp.right
    temp.value-=1
    while temp.position[1]!=y:
        temp=temp.down
    

    if(temp.down!=None):
        temp.down.up=temp.up
        temp.up.down=temp.down
    else:
        temp.up.down=None

    if temp.left!=None and temp.right!=None:
        temp.left.right=temp.right
        temp.right.left=temp.left
    elif temp.left!=None:
        temp.left.right=None
    elif temp.right!=None:
        temp.right.left=None

    return temp

def uncoverNode(n):
    node=n
    if(node.down!=None):
        node.down.up=node
    if(node.up!=None):
        node.up.down=node
    if(node.right!=None):
        node.right.left=node
    if(node.left!=None):
        node.left.right=node

    while node.up!=None:
        node=node.up
    node.value+=1


def coverColumn(node):
    temp=node
    nodes=[]
    
    while(temp.up!=None):
        temp=temp.up
        
    while(temp!=None):
        if(temp.right!=None and temp.left!=None):
            temp.right.left=temp.left
            temp.left.right=temp.right
        elif(temp.right!=None):
            temp.right.left=None
        elif(temp.left!=None):
            temp.left.right=None
        
        nodes.append(temp)
        temp=temp.down 
    return(nodes)

def coverRow(node):
    nodes=[]
    if(node.position[1]!=-1):
        
        temp=node
        
        while(temp.left!=None):
            temp=temp.left


        while(temp!=None):
            if(temp.up!=None and temp.down!=None):
                temp.up.down=temp.down
                temp.down.up=temp.up
            elif(temp.up!=None):
                temp.up.down=None
            elif(temp.down!=None):
                temp.down.up=None
            if(node.position!=temp.position):
                nodes.append(temp)

            temp1=temp
            while temp1.up!=None:
                temp1=temp1.up
            temp1.value-=1
            temp=temp.right
    return nodes

def getCol(list):
    temp=list.right
    lowestVal=10
    col=None
    while (temp!=None):
        if temp.active==1 :
            if(temp.value<lowestVal):
                lowestVal=temp.value
                col=temp
            elif(temp.value==lowestVal):
                if(random.randint(0,20)==1):
                    col=temp

            if(temp.value==0):
                return None
        temp=temp.right
    return col

def getRows(col):
    rows=[]
    temp=col.down
    while(temp!=None):
        rows.append(temp)
        temp=temp.down
    return(rows)

def C(node):
    n=node
    nodesCovered=[node]
    no=coverRow(n)
    
    for i in no:
        nodesCovered.append(i)
        co=coverColumn(i)
        
        for j in co:
            nodesCovered.append(j)
            ro=coverRow(j)
            for k in ro:
                nodesCovered.append(k)
    x=coverColumn(node) 
    for i in x:
        nodesCovered.append(i)               
    return nodesCovered

def U(nodes):
    for node in nodes:
        uncoverNode(node)        
def empty(list):
    if list.right==None:
        return True
    else:
        return False    
            
   
def sort(InputList):
    for i in range(1, len(InputList)):
        j = i-1
        nxt_element = InputList[i]	
        while (InputList[j].position[1] > nxt_element.position[1]) and (j >= 0):
            InputList[j+1] = InputList[j]
            j=j-1
        InputList[j+1] = nxt_element







def pb(array):
    board=[[],[],[],[],[],[],[],[],[]]
    for i in array:
        col=math.floor(i.position[1]/81)
        row= math.floor((i.position[1]-col*81)/9)
        num=  i.position[1]-((col*81)+(row*9))+1
        board[row].insert(col,num)
   
    for i in board:
        print (i)  
        



#d(x)
def run(board,list):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)


    pygame.init()
    pygame.font.init()
    size = (455, 455)
    screen = pygame.display.set_mode(size)
    myfont = pygame.font.SysFont('Arial', 25)
    pygame.display.set_caption("Sodoku ")

    done = False

    clock = pygame.time.Clock()

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill(WHITE)

        drawLines(screen)
        printNum(screen,board)
        solve(list,board,screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

def updateBoard(array,board):
    for i in array:
        col=math.floor(i.position[1]/81)
        row= math.floor((i.position[1]-col*81)/9)
        num=  i.position[1]-((col*81)+(row*9))+1
        board[row][col]=num

def solve(list,board,screen):
    sol=[]
    rowStack=[]
    covStack=[]
    c=0
    while(not empty(list)):
        col=getCol(list)
        if(col!=None):
            rowStack.append(getRows(col))
            covStack.append(C(rowStack[-1][0]))
            sol.append(rowStack[-1][0])
            updateBoard(sol,board)
            printNum(screen,board)
            updateValues(list)
        else:
            del(rowStack[-1][0])
            del(sol[-1])
            updateBoard(sol,board)
            printNum(screen,board)
            U(covStack[-1])
            updateValues(list)
            del(covStack[-1])
            if(rowStack[-1]):
                covStack.append(C(rowStack[-1][0]))
                sol.append(rowStack[-1][0])
                updateBoard(sol,board)
                printNum(screen,board)
                updateValues(list)
            else:
                del(rowStack[-1])
        c+=1
        if(c>100):
            for i in covStack:
                U(i)
            sol=[]
            updateBoard(sol,board)
            printNum(screen,board)
            rowStack=[]
            covStack=[]
            c=0
    #print("done")     

def printNum(screen,board):
    BOXCOLOR = (0, 60, 80)
    FONTCOLOR = (255, 255, 255)
    FONTCOLOR1 = (200, 0, 0)
    NUMOFFSETX = 18
    NUMOFFSETY = 6
    DELAY = 0.000
    pygame.event.get()
    myfont = pygame.font.SysFont('Impact', 25)
    y = 5
    for i in range(0, 9):
        x = 5
        for j in range(0, 9):
            pygame.draw.rect(screen, BOXCOLOR, (x, y, 45, 45))
            screen.blit(myfont.render(str (board[i][j]), True,FONTCOLOR), (x+NUMOFFSETX, y+NUMOFFSETY))
            x = x+50
        y = y+50
    pygame.display.flip()
    time.sleep( DELAY )
    
def drawLines(screen):
    LINECOLOR = (0, 0, 0)
    pygame.draw.line(screen, LINECOLOR, (152, 5), (152, 450), 5)
    pygame.draw.line(screen, LINECOLOR, (302, 5), (302, 450), 5)
    pygame.draw.line(screen, LINECOLOR, (5, 152), (450, 152), 5)
    pygame.draw.line(screen, LINECOLOR, (5, 302), (450, 302), 5)



x=ll()
x=x.right
constraint1(x)
constraint2(x)
constraint3(x)
constraint4(x)
join1(x)
updateValues(x)
x=x.left
board=[[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,-1,-1]]
run(board,x)












