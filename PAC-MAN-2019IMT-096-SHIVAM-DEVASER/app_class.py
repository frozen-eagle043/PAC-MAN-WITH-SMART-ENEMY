import pygame
from settings import *
from player_class import *
from enemy import *
import copy
pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.WINDOW = pygame.display.set_mode((WIDTH,HEIGTH))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH // 28
        self.cell_heigth = MAZE_HEIGTH // 30
        self.PLAYER_START_POS = None
        self.coins = []
        self.walls = []
        self.enemies = []
        self.e_pos = []
        self.load()
        self.player = Player(self,copy.copy(self.PLAYER_START_POS))
        self.make_enemies()

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'PLAY':
                self.PLAY_events()
                self.PLAY_update()
                self.PLAY_draw()
            elif self.state == 'GAME_OVER':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.running = False

            self.clock.tick(FPS)
            
        pygame.quit()

#helper
    def draw_text(self,Text,WINDOW,pos,size,color,font_name):
        font = pygame.font.SysFont(font_name,size)
        text = font.render(Text,False,color)
        text_size = text.get_size()
        pos[0] = pos[0]-text_size[0] // 2
        WINDOW.blit(text,pos)

    def load(self):
        self.background = pygame.image.load('background.png')
        self.background = pygame.transform.scale(self.background,(MAZE_WIDTH,MAZE_HEIGTH))
        #opening walls file 
        with open("walls.txt",'r') as file:
            for yidx,line in enumerate(file):
                for xidx,char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx,yidx))
                    elif char == "C":
                        self.coins.append(vec(xidx,yidx))
                    elif char == "P":
                        self.PLAYER_START_POS = [xidx,yidx]
                    elif char in ["6","5","4","3","2"]:
                        self.e_pos.append([xidx,yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background,BLACK,(xidx*self.cell_width,yidx*self.cell_heigth,self.cell_width,self.cell_heigth))

        #print(len(self.walls))

    def make_enemies(self):
        for idx,pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self,vec(pos),idx))

    def draw_grid(self):
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, GREY,(x*self.cell_width ,0),(x*self.cell_width ,HEIGTH))

        for x in range(HEIGTH // self.cell_heigth):
            pygame.draw.line(self.background, GREY,(0,x*self.cell_heigth),(WIDTH,x*self.cell_heigth ))

        
    def reset(self):
        self.player.lives = 3
        self.player.score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = "PLAY"

        
#start
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'PLAY'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()


    def start_update(self):
        pass

    def start_draw(self):
        self.WINDOW.fill(BLACK)
        self.draw_text('HIGH SCORE',self.WINDOW,[140,5],START_TEXT_SIZE,WHITE,START_FONT)
        self.draw_text('PUSH SPACE_BAR TO START',self.WINDOW,[WIDTH // 2,HEIGTH//2-50],START_TEXT_SIZE,ORANGE,START_FONT)
        self.draw_text('1 PLAYER ONLY',self.WINDOW,[WIDTH // 2,HEIGTH//2+20],START_TEXT_SIZE,TURQUISE,START_FONT)
        self.draw_text('MADE BY - ',self.WINDOW,[WIDTH // 2 - 235,HEIGTH//2 + 240],START_TEXT_SIZE-10,WHITE,START_FONT)
        self.draw_text('SHIVAM DEVASER 2019_IMT-096',self.WINDOW,[WIDTH // 2 - 90,HEIGTH//2 + 260],START_TEXT_SIZE-5,WHITE,START_FONT)
        pygame.display.update()
#play
    def PLAY_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1,0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1,0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0,-1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0,1))
            
    def PLAY_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        
        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def PLAY_draw(self):
        self.WINDOW.fill(BLACK)
        self.WINDOW.blit(self.background,(TOP_BUFFER // 2,TOP_BUFFER // 2))
        self.draw_coins()
        #self.draw_grid()

        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()
        #self.coins.pop()


    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "GAME_OVER"
        else:
            self.player.grid_pos=vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0



    def draw_coins(self):
        for coin in self.coins:
           pygame.draw.circle(self.WINDOW,YELLOW1,(int(coin.x*self.cell_width + self.cell_width // 2 + TOP_BUFFER//2),int(coin.y*self.cell_heigth + self.cell_heigth //2 + TOP_BUFFER//2)),5)
#game over
    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.WINDOW.fill(BLACK)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACE bar to PLAY AGAIN"
        self.draw_text("GAME OVER", self.WINDOW, [WIDTH//2, 100],  52, RED, "arial")
        self.draw_text(again_text, self.WINDOW, [
                       WIDTH//2, HEIGTH//2],  36, (190, 190, 190), "arial")
        self.draw_text(quit_text, self.WINDOW, [
                       WIDTH//2, HEIGTH//1.5],  36, (190, 190, 190), "arial")
        pygame.display.update()