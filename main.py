import os
import pygame
import math
from pygame.locals import * # import pygame.locals for easier access to key coordinates
from sys import exit
import random
import time
import neat
import pickle
import numpy as np
from pygame import Surface
import cv2

pygame.init()
clock = pygame.time.Clock()
bgimg = pygame.image.load('ProgrammeerimiseProjekt/assets/road.jpg') #loads in the background image
screen_width = bgimg.get_width() 
screen_height = bgimg.get_height()
blackplayer = cv2.imread("ProgrammeerimiseProjekt/assets/playercar.png", cv2.IMREAD_UNCHANGED)
ret, mask = cv2.threshold(blackplayer[:, :, 3], 0, 255, cv2.THRESH_BINARY)
cv2.imwrite('ProgrammeerimiseProjekt/assets/black-and-white.png', mask) 
blackplayer = pygame.image.load('ProgrammeerimiseProjekt/assets/black-and-white.png')
blackplayer = pygame.transform.rotate(blackplayer, 90)
blackplayer = pygame.transform.scale(blackplayer, (55, 105))
blackimg = pygame.image.load('ProgrammeerimiseProjekt/assets/road.jpg')


screen = pygame.display.set_mode((screen_width, screen_height)) #sets the screen size
pygame.display.set_caption("Racer Game") #sets the name of the opened window

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ProgrammeerimiseProjekt/assets/playercar.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale(self.image, (60, 105))
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width/2, screen_height-100)
        self.mask = pygame.mask.from_surface(self.image)
        self.points = 0
        self.radars = [[(0, 0), 0, (-math.pi)], [(0, 0), 0, 3 * (-math.pi) / 4], [(0, 0), 0, (-math.pi) / 2],
                       [(0, 0), 0, (-math.pi) / 4], [(0, 0), 0, 0]]
        self.distances = []
        for distance in self.radars:
            position, dist, angle = distance
            self.distances.append(dist)

    def checkRadars(self, radars, bgimg, resolution):
        i = 0
        for radar in radars:
            pos, dist, angle = radar
            len = 0
            x = int(self.rect.center[0] + math.cos(2 * math.pi + angle) * len)
            y = int(self.rect.center[1] + math.sin(2 * math.pi + angle) * len)
            while x > 0 and x < screen_width and y > 0 and y < screen_height and not bgimg.get_at((x, y)) == (255, 255, 255) and len < 500:
                len += 1
                x = int(self.rect.center[0] + math.cos(2 * math.pi + angle) * len)
                y = int(self.rect.center[1] + math.sin(2 * math.pi + angle) * len)

            dist = math.sqrt(math.pow(x - self.rect.center[0], 2) + math.pow(y - self.rect.center[1], 2))
            self.radars[i] = ([(x, y), dist, angle])
            i += 1

    def update(self, dir = 0, gamemode = 1, black = blackimg):
        # move the sprite based on the key pressed
        if gamemode == 1:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_LEFT] or pressed_keys[K_a]:
                self.rect.move_ip(-5, 0)
            if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
                self.rect.move_ip(5, 0)
        else:
            if dir == -1:
                self.rect.move_ip(-5, 0)
            if dir == 1:
                self.rect.move_ip(5, 0)

        # keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width

        self.checkRadars(self.radars, black, (screen_width, screen_height))
        self.distances = []
        for distance in self.radars:
            position, dist, angle = distance
            self.distances.append(dist)
    
    def draw(self, surface):
        # blit yourself at your current position
        surface.blit(self.image, self.rect)
        for radar in self.radars:
            pos, dist, angle = radar
            pygame.draw.line(screen, (255, 0, 0), self.rect.center, pos, 1)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ProgrammeerimiseProjekt/assets/playercar.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (320, 240)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # move enemy down the screen
        self.rect.move_ip(0, 1)
        # if image is off screen, kill it
        if self.rect.top > screen_height:
            self.kill()
            return True
        return False
        
    
    def draw(self, surface):
        # blit yourself at your current position
        surface.blit(self.image, self.rect)

enemy_locations = [64, 148, 240, 330, 420] # define enemy spawn locations


def create_enemies(enemies):
    newenemies = []
    for e in range(random.randint(1,4)):
        if not newenemies:
            newenemies.append(Enemy())
            spawnpoint = random.choice(enemy_locations)
            newenemies[0].rect.center = (spawnpoint, 0-newenemies[0].rect.height/2)
        else:
            enemy = Enemy()
            enemy.rect.center = (random.choice(enemy_locations), 0-enemy.rect.height/2)
            checked = False
            while not checked:
                j = False   
                for i in newenemies:
                    if not pygame.sprite.collide_mask(enemy, i) and enemy.rect.center[0] != i.rect.center[0] and enemy.rect.center[0] != i.rect.center[0]+1 and enemy.rect.center[0] != i.rect.center[0]-1:
                        j = True
                    else:
                        j = False
                        break
                if j:
                    newenemies.append(enemy)
                    checked = True
                else:
                    pass
                if not checked:
                    enemy.rect.center = (random.choice(enemy_locations), 0-enemy.rect.height/2)
                else:
                    break
    
    return newenemies

def check_and_remove_enemies(enemies):
    for i in range(len(enemies)):
        # check if current enemy has the same coordinates as any other enemies in the list
        for j in range(i+1, len(enemies)):
            if enemies[i].rect.center == enemies[j].rect.center:
                # if they have the same coordinates, remove one of the enemies
                enemies.remove(enemies[j])
                



def game(genomes, config):
    nets = []
    ge = []
    players = [] # create player
    enemies = [] # create enemy list
    enemies = create_enemies(enemies)
    enemy_positions = []
    for i in range(30):
        enemy_positions.append(0)
    


    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        players.append(Player())
        g.fitness = 0
        ge.append(g)

    font = pygame.font.SysFont("opensans", 50)
    enemy_timer = time.perf_counter()
    enemy_random_timer = 300
    loop_counter = 0
    scroll = 0
    tiles = math.ceil(screen_height / bgimg.get_height()) + 1 
    loops = 0
    speed = 400
    
    run = True
    while run:
        blackimg.fill((0,0,0))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        screen.fill((0,0,0)) #clear the screen before drawing on it 

        clock.tick(speed) 
        if loops % 100 == 0 and speed < 100:
            speed += 5
        if speed > 100:
            speed = 100

        #scroll background 
        scroll = (scroll + 1) % bgimg.get_height()
        for y in range(tiles):
            screen.blit(bgimg, (0, (y-1) * bgimg.get_height() + scroll))

        # update player position
        for player in players:
            player.draw(screen)
        # update enemy position
        
        if loop_counter == enemy_random_timer:
            enemies.extend(create_enemies(enemies))
            enemy_random_timer = random.randint(300, 400)
            loop_counter = 0
        check_and_remove_enemies(enemies)

        enemy_positions = []
        for i in range(30):
            enemy_positions.append(0)
        temp = []
        temp.append([0,0,0,0,0,0,0,0,0,0])
        temp.append([0,0,0,0,0,0,0,0,0,0])
        temp.append([0,0,0,0,0,0,0,0,0,0])
        temp.append([0,0,0,0,0,0,0,0,0,0])
        temp.append([0,0,0,0,0,0,0,0,0,0])
        ycords = []
        for e in enemies:
            blackimg.blit(blackplayer, e.rect)
            if e.rect.center[1] not in ycords:
                ycords.append(e.rect.center[1])
        
        


        for e in enemies:
            if e.update():
                enemies.remove(e)
            else:
                e.draw(screen)
            for i in range(len(ycords)):
                if e.rect.center[1] == ycords[i]+1:
                    temp[i].append(e.rect.center[0])
                    temp[i].pop(0)
                    temp[i].append(e.rect.center[1])
                    temp[i].pop(0)
            enemy_positions = []
            enemy_positions.extend(temp[0])
            enemy_positions.extend(temp[1])
        #print(ycords)
        #print(enemy_positions)
        

        # check for collisions
        for e in enemies:
            for x, player in enumerate(players):
                if pygame.sprite.collide_mask(player, e):
                    pygame.display.update()
                    ge[x].fitness -= 100
                    players.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    '''
                    while True:
                        screen.blit(font.render("Game Over", 1, (255, 255, 255)), (screen_width/2-100, screen_height/2-100))
                        screen.blit(font.render("Points: " + str(points), 1, (255, 255, 255)), (screen_width/2-100, screen_height/2-50))
                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                exit()'''

        # draw enemies
            

        text = font.render("Points: " + str(loops), True, (0 , 255, 0))
        screen.blit(text, (100, 10))

        pygame.display.update()
        loop_counter += 1
        if len(players) > 0:
            for x,player in enumerate(players):
                player.update(gamemode = 0, black = blackimg)
                tmp = enemy_positions.copy()
                tmp.append(player.rect.center[0])
                tmp.append(player.rect.center[1])
                for i in player.distances:
                    tmp.append(i)
                output = nets[x].activate(tuple(tmp))
                if output[0] < 0.4:
                    player.update(dir = -1, gamemode = 0, black = blackimg)
                elif output[0] > 0.6:
                    player.update(dir = 1, gamemode = 0, black = blackimg)
                else:
                    player.update(dir = 0, gamemode = 0, black = blackimg)
                    ge[x].fitness += 5
                player.draw(screen)
        else:
            run = False
            break
        for x, player in enumerate(players):
            if player.rect.x < 1:
                ge[x].fitness -= 50
                players.pop(x)
                nets.pop(x)
                ge.pop(x)
            elif player.rect.x + player.rect.width > screen_width-1:
                ge[x].fitness -= 50
                players.pop(x)
                nets.pop(x)
                ge.pop(x)
            else:
                ge[x].fitness += 5
        loops += 1
        
    return loops

def run(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(game, 500)
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
    f.close()

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)