import pygame
import random
import time



class board:
    def __init__(self):
        self.orignal=[[-1,-1,-1,-1,-1,8,-1,2,7],[-1,4,-1,1,-1,-1,-1,-1,8],[-1,1,-1,-1,7,-1,-1,9,4],[-1,-1,-1,3,-1,-1,-1,-1,9],[-1,-1,3,-1,-1,-1,8,-1,-1],[6,-1,-1,-1,-1,4,-1,-1,-1],[1,8,-1,-1,9,-1,-1,6,-1],[9,-1,-1,-1,-1,5,-1,1,-1],[3,6,-1,7,-1,-1,-1,-1,-1]]
        self.board = [[-1,-1,-1,-1,-1,8,-1,2,7],[-1,4,-1,1,-1,-1,-1,-1,8],[-1,1,-1,-1,7,-1,-1,9,4],[-1,-1,-1,3,-1,-1,-1,-1,9],[-1,-1,3,-1,-1,-1,8,-1,-1],[6,-1,-1,-1,-1,4,-1,-1,-1],[1,8,-1,-1,9,-1,-1,6,-1],[9,-1,-1,-1,-1,5,-1,1,-1],[3,6,-1,7,-1,-1,-1,-1,-1]]

        self.constraints = [[[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []], [[], [], [
        ], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []]]

    def getValue(self, x, y):
        if self.board[x][y] != -1:
            return str(self.board[x][y])
        else:
            return "-"

    def setValue(self, x, y, z):
        self.board[x][y] = z

    def getConstraint(self, x, y):
        return self.constraints[x][y]

    def boardSize(self):
        return len(self.board)

    def printBoard(self):
        for x in range(len(self.board)):

            for y in range(len(self.board)):
                print(self.getValue(x, y), ' ', end="")
            print(" ")

    def valid(self, x, y, value):
        for i in range(self.boardSize()):

            if(self.getValue(i, y) == str(value)):
                return False
            if(self.getValue(x, i) == str(value)):
                return False

        if(x < 3):
            if(y < 3):
                if(not self.checkBlock(0, 3, 0, 3, value)):
                    return False
            elif(y < 6):
                if(not self.checkBlock(3, 6, 0, 3, value)):
                    return False
            else:
                if(not self.checkBlock(6, 9, 0, 3, value)):
                    return False
        elif(x < 6):
            if(y < 3):
                if(not self.checkBlock(0, 3, 3, 6, value)):
                    return False

            elif(y < 6):
                if(not self.checkBlock(3, 6, 3, 6, value)):
                    return False

            else:
                if(not self.checkBlock(6, 9, 3, 6, value)):
                    return False
        else:
            if(y < 3):
                if(not self.checkBlock(0, 3, 6, 9, value)):
                    return False
            elif(y < 6):
                if(not self.checkBlock(3, 6, 6, 9, value)):
                    return False

            else:
                if(not self.checkBlock(6, 9, 6, 9, value)):
                    return False

        return True

    def checkBlock(self, hs, he, vs, ve, value):
        for i in range(hs, he):
            for j in range(vs, ve):
                if self.getValue(j, i) == str(value):
                    return False
        return True

    def calculateConstraints(self):
        self.constraints = [[[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []], [[], [], [
        ], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], []]]
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if(self.getValue(i, j) == "-"):
                    for k in range(1, 10):
                        if self.valid(i, j, k):
                            self.constraints[i][j].append(k)

    def printConstraints(self):
        for i in self.constraints:
            print(i)

    def selectLowestHeuristic(self):
        min = 9999
        minx = -1
        miny = -1
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if(len(self.constraints[i][j]) > 0 and len(self.constraints[i][j]) < min):
                    min = len(self.constraints[i][j])
                    minx = i
                    miny = j

        return (minx, miny)

    def boardComplete(self):
        for i in self.board:
            for j in i:
                if(j == -1):
                    return False

        return True


def run(board):
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
        solve(board,screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


def solve(board,screen):
    if(not board.boardComplete()):
        run = True
        while(run and not board.boardComplete()):
            run = False
            for i in range(board.boardSize()):
                for j in range(board.boardSize()):
                    x = board.getConstraint(i, j)
                    if(len(x) == 1):
                        run = True
                        board.setValue(i, j, x[0])
                        board.calculateConstraints()
                        printNum(screen,board)

        x, y = board.selectLowestHeuristic()
        queue = [[board.getConstraint(x, y), [x, y]]]
        board.calculateConstraints()
        if(not board.boardComplete()):
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                
                c = queue.pop()

                if(len(c[0]) == 0):
                    board.setValue(c[1][0], c[1][1], -1)
                    printNum(screen,board)
                else:
                    value = c[0].pop()
                    queue.append(c)

                    board.setValue(c[1][0], c[1][1], value)
                    if board.boardComplete():
                        break
                    board.calculateConstraints()
                    x, y = board.selectLowestHeuristic()

                    if(x == -1):

                        while(x == -1):
                            c = queue.pop()
                
                            if(len(c[0]) == 0):
                                board.setValue(c[1][0], c[1][1], -1)
                                printNum(screen,board)
                            else:
                                queue.append(c)
                                value = c[0].pop()
                                board.setValue(c[1][0], c[1][1], value)
                            board.calculateConstraints()
                            x, y = board.selectLowestHeuristic()
                            printNum(screen,board)

                    else:
                        queue.append([board.getConstraint(x, y), [x, y]])
                        printNum(screen,board)
                


            
        if(board.boardComplete()):
            print("done")
        else:
            print("board cannot be solved")
def printNum(screen,board):
    BOXCOLOR = (0, 60, 80)
    FONTCOLOR = (255, 255, 255)
    FONTCOLOR1 = (200, 0, 0)
    NUMOFFSETX = 18
    NUMOFFSETY = 6
    DELAY = 0.00
    myfont = pygame.font.SysFont('Impact', 25)
    y = 5
    for i in range(0, 9):
        x = 5
        for j in range(0, 9):
            pygame.draw.rect(screen, BOXCOLOR, (x, y, 45, 45))
            if(board.orignal[i][j]==-1):
                screen.blit(myfont.render(board.getValue(i, j), True,FONTCOLOR), (x+NUMOFFSETX, y+NUMOFFSETY))
            else:
                screen.blit(myfont.render(board.getValue(i, j), True,FONTCOLOR1), (x+NUMOFFSETX, y+NUMOFFSETY))
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
board = board()
board.calculateConstraints()


# print(board.selectLowestHeuristic())
#print("here")tic())
#print("here")
#solve(board)
# print(valid(board,5,0,7))
run(board)
#solve(board)
