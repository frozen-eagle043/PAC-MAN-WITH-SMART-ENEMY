import math
import pygame
vec = pygame.math.Vector2

from queue import PriorityQueue

WIDTH = 560
HEIGTH = 620
WINDOW = pygame.display.set_mode((WIDTH,HEIGTH))
pygame.display.set_caption("MAZE PATH FINDER")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,255,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUISE = (64,224,208)

class Spot:
    def __init__(self,row,col,width,heigth,totalRows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*heigth
        self.color = RED
        self.neighbors = []
        self.width = width
        self.heigth = heigth
        self.totalRows = totalRows

    def getPos(self):
        return self.row,self.col
    
    def isClose(self):
        return self.color == WHITE

    def isOpen(self):
        return self.color == BLUE

    def isBarrier(self):
        return self.color == BLACK

    def isStart(self):
        return self.color == PURPLE

    def isEnd(self):
        return self.color == GREEN

    def reset(self):
        self.color = RED

    def makeClose(self):
        self.color = WHITE

    def makeOpen(self):
        self.color = BLUE

    def makeBarrier(self):
        self.color == BLACK

    def makeStart(self):
        self.color = PURPLE

    def makeEnd(self):
        self.color = GREEN

    def makePath(self):
        self.color = TURQUISE

    def draw(self,WINDOW):
        pygame.draw.rect(WINDOW,self.color,(self.x,self.y,self.width,self.heigth))

    def updateNeifgbours(self,grid):
        self.neighbors = []
        if self.row < self.totalRows -1 and not grid[self.row + 1][self.col].isBarrier(): #down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].isBarrier(): #up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.totalRows -1 and not grid[self.row ][self.col+1].isBarrier(): #Rght
            self.neighbors.append(grid[self.row ][self.col+1])

        if self.col > 0 and not grid[self.row ][self.col-1].isBarrier(): #left
            self.neighbors.append(grid[self.row ][self.col-1])

    def __lt__(self,other):
        return False  


def reconstructPath(cameFrom,current,draw):
    while current in cameFrom:
        current = cameFrom[current]
        current.makePath()
        draw()


def h(p1,p2):
    x0 ,y0 = p1
    x1 ,y1 = p2
    p2 = (1,9)
    return abs(x0 - x1) + abs(y0 -y1)

def algorithm1(draw,grid,start,end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count,start))
    cameFrom = {}
    gScore = {spot:float("inf") for row in grid for spot in row}
    gScore[start] = 0
    fScore = {spot:float("inf") for row in grid for spot in row}
    fScore[start] = h(start.getPos(),end.getPos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end :
            reconstructPath(cameFrom, end,draw)
            end.makeEnd()
            start.makeStart()
            return True

        for neighbor in current.neighbors:
            temp_g_score = gScore[current] + 1
            
            if temp_g_score < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = temp_g_score
                fScore[neighbor] = temp_g_score + h(neighbor.getPos(),end.getPos())
                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((fScore[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    #neighbor.makeOpen()
        #draw()

       # if current != start:
         #   current.makeClose()

    return False

def algorithm(draw,grid,start,end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0,count,start))
    cameFrom = {}
    gScore = {spot:float("inf") for row in grid for spot in row}
    gScore[start] = 0
    fScore = {spot:float("inf") for row in grid for spot in row}
    fScore[start] = h(start.getPos(),end.getPos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end :
            reconstructPath(cameFrom, end,draw)
            end.makeEnd()
            start.makeStart()
            return True

        for neighbor in current.neighbors:
            temp_g_score = gScore[current] + 1
            
            if temp_g_score < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = temp_g_score
                fScore[neighbor] = temp_g_score + h(neighbor.getPos(),end.getPos())
                if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((fScore[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.makeOpen()
        draw()

        if current != start:
            current.makeClose()

    return False

def makeGrid(rows,width,col):
    grid = []
    gap1= width // rows
    gap2=HEIGTH // col
    for i in range(rows):
        grid.append([])
        for j in range(col):
            spot = Spot(i ,j ,gap1,gap2 ,rows)
            grid[i].append(spot)

    return grid

def drawGrid(WINDOW,rows,col,width):
    GAP1 = width // rows
    GAP2 = HEIGTH // col
    for i in range(rows):
        pygame.draw.line(WINDOW,GREY,(0,i*GAP1),(width,i*GAP2))
    for j in range(rows):
        pygame.draw.line(WINDOW,GREY,(j*GAP1,0),(j*GAP2,width))

def draw(WINDOW,grid,rows,col,width):
    WINDOW.fill(RED)
    for row in grid:
        for spot in row:
            spot.draw(WINDOW)

    drawGrid(WINDOW,rows,col,width)
    pygame.display.update()

def getClickedPosition(pos,rows,col,width):
    GAP1 = width // rows
    GAP2 = HEIGTH // col

    y,x = pos

    row = y // GAP1
    col = x // GAP2
    return row,col

def main(WINDOW,width):
    ROWS = 31
    COL = 28
    grid = makeGrid(COL,WIDTH,ROWS)

    start = None
    end = None

    run = True
    started = False

    while run :
        
        draw(WINDOW,grid,COL,ROWS,WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row,col = getClickedPosition(pos,ROWS,COL,width)
                spot = grid[int(row)][int(col)]
                spot.makeBarrier()
            if event.type == pygame.KEYDOWN:
                with open("walls.txt",'r') as file:
                        for yidx,line in enumerate(file):
                            for xidx,char in enumerate(line):
                                if char == "1":
                                    print(yidx,xidx)
                                    spot = grid[int(yidx)][int(xidx)]
                                    spot.makeBarrier()
                a=vec(1,1)
                b=vec(1,15)
                row,col = a.y,a.x
                spot = grid[int(row)][int(col)]
                start = spot
                row,col = b.y,b.x
                spot = grid[int(row)][int(col)]
                end = spot
                if event.key == pygame.K_l and start and end:
                    for row in grid:
                        for spot in row:
                            spot.updateNeifgbours(grid)
                            print(spot.neighbors)
                    algorithm1(lambda:draw(WINDOW,grid,ROWS,COL,WIDTH),grid,start,end)

                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.updateNeifgbours(grid)

                    algorithm(lambda:draw(WINDOW,grid,ROWS,COL,WIDTH),grid,start,end)

                if event.key == pygame.K_c:
                    start=None
                    end=None
                    grid = makeGrid(ROWS,WIDTH,COL)
    pygame.quit()

main(WINDOW,WIDTH)

