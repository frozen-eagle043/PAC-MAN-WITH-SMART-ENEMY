import pygame
from pygame.math import Vector2 as vec
from settings import *



class Player:
    def __init__(self,app,pos):
        
        self.app = app
        self.starting_pos = [pos[0],pos[1]]
        self.grid_pos = vec(pos[0],pos[1])
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1,0)
        self.stored_direction = None
        self.score = 0
        self.able_to_move = True
        self.speed = 2
        self.lives = 3


    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction*self.speed
        #keeping in boxes
        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        
                

        #setting grid in ref to pix
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BUFFER+self.app.cell_width//2)//self.app.cell_width +1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BUFFER+self.app.cell_heigth//2)//self.app.cell_heigth +1

        if self.on_coin():
            self.eat_coin()

    def draw(self):
        self.app.draw_text('CURRENT SCORE : '+str(self.score),self.app.WINDOW,[120,5],20,WHITE,START_FONT)
        self.app.draw_text('HIGH SCORE :'+str(self.score),self.app.WINDOW,[500,5],20,WHITE,START_FONT)
        pygame.draw.circle(self.app.WINDOW,YELLOW,self.pix_pos,self.app.cell_width//2-2)
        #drawing grid pos rect

        for x in range(self.lives):
            pygame.draw.circle(self.app.WINDOW,YELLOW,(35 + 25*x ,HEIGTH-15),self.app.cell_width//2-2)

        #pygame.draw.rect(self.app.WINDOW,RED,(self.grid_pos[0]*self.app.cell_width+TOP_BUFFER//2,self.grid_pos[1]*self.app.cell_heigth+TOP_BUFFER//2,self.app.cell_width,self.app.cell_heigth),1)
    
    
    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x + TOP_BUFFER //2 )% self.app.cell_width == 0:
                if self.direction == vec(1,0) or self.direction == vec(-1,0):
                    return True

            if int(self.pix_pos.y + TOP_BUFFER //2) % self.app.cell_heigth == 0:
                if self.direction == vec(0,1) or self.direction == vec(0,-1):
                    return True
        return False


    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.score += 2



    def move(self,direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.app.cell_width)+TOP_BUFFER//2+self.app.cell_width//2,
        (self.grid_pos.y*self.app.cell_heigth)+TOP_BUFFER//2+self.app.cell_heigth//2)
        print(self.grid_pos,self.pix_pos)

    def time_to_move(self):

        if int(self.pix_pos.x + TOP_BUFFER //2 )% self.app.cell_width == 0:
            if self.direction == vec(1,0) or self.direction == vec(-1,0) or self.direction == vec(0,0):
                return True

        if int(self.pix_pos.y + TOP_BUFFER //2) % self.app.cell_heigth == 0:
            if self.direction == vec(0,1) or self.direction == vec(0,-1) or self.direction == vec(0,0):
                return True

        return False

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos+self.direction)==wall:
                return False
        return True