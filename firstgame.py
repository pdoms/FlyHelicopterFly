import pygame
import random
import os
import pygame.freetype
import pandas as pd
import datetime

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE,
    K_RETURN,
    K_BACKSPACE
)





p = os.getcwd()



def logHighscore(username, score):
    with open('highscores.csv', 'a') as f:
        t = str(datetime.datetime.now().isoformat())
        f.write(f'{t},{username},{score}\n')

def getHighScore():
    df = pd.read_csv('highscores.csv')
    score = df['score']
    max = score.max()
    by = df.iloc[df['score'].argmax()]['name']
    return str(max), str(by)

import random



balloon_red = os.path.join("sprites","balloon_red.png")
balloon_yellow = os.path.join("sprites","balloon_yellow.png")
balloon_purple = os.path.join("sprites","balloon_purple.png")
cloud = os.path.join("sprites","cloud.png")
cloud_2 = os.path.join("sprites","cloud_2.png")
cloud_3= os.path.join("sprites","cloud_3.png")



def random_sprite(type):
    r = random.randint(1,3)
    if type == 'balloon':
        if r == 1:
            return balloon_red
        elif r == 2:
            return balloon_yellow
        else:
            return balloon_purple
    elif type == 'cloud':
        if r == 1:
            return cloud
        elif r == 2:
            return cloud_2
        else:
            return cloud_3
    


print('GAME IS STARTING')

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super(Player, self).__init__()
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"sprites","helicopter.png")
        self.surf = pygame.image.load(path).convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()


    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-7)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,7)
        if pressed_keys[K_LEFT]: 
            self.rect.move_ip(-7,0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(7,0)


        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super(Enemy, self).__init__()
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"sprites","bird.png")
        self.surf = pygame.image.load(path).convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH+100), random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(10,25)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Balloon(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super(Balloon, self).__init__()
        path = random_sprite('balloon')
        self.surf = pygame.image.load(path).convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH+100), random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5,20)
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super(Cloud, self).__init__()
        path = random_sprite('cloud')
        self.surf = pygame.image.load(path).convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH+100), random.randint(40, SCREEN_HEIGHT)
            )
        )
    
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

score = 0
current_level = 10
ticks = 20


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

ADDENEMY = pygame.USEREVENT + 1
ADDBALLOON = pygame.USEREVENT + 2
ADDCLOUD = pygame.USEREVENT + 3
pygame.time.set_timer(ADDENEMY, 700)
pygame.time.set_timer(ADDBALLOON, 500)
pygame.time.set_timer(ADDCLOUD, 1000)
player = Player()


enemies = pygame.sprite.Group()
balloons = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"font","LuckiestGuy-Regular.ttf")
score_font = pygame.freetype.Font(font_path)

def keepScore(board):
    score_font.render_to(board, (3,3), "Score: "+str(score), bgcolor=((42, 203, 235)), size=20)

def write(text, dims, pos, size):
    surface = pygame.Surface(dims)
    surface.fill((42, 203, 235))
    score_font.render_to(surface, (3,3), str(text), bgcolor=((42, 203, 235)), size=size)
    return screen.blit(surface, pos)
    

running = False
intro = True

def gamepaused():
    pygame.mixer.music.stop()
    collisionsound.stop()
    write('PAUSE', (300, 80), ((SCREEN_WIDTH/2)-120, 100), 80)
    write('Hit Space to continue', (500, 50), ((SCREEN_WIDTH/2)-205, 250), 40)
    paused = True
    exit = False
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                paused = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit = True
                    paused = False                    
                if event.key == K_SPACE:
                    pygame.mixer.music.play(loops=-1)
                    screen.fill((0,0,0))
                    paused = False
        pygame.display.update()
        clock.tick(60)
    return exit

username = ''
highscore = 0


while intro:
    for event in pygame.event.get(): 
        if event.type == QUIT:
            intro = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
            elif event.key == K_SPACE:
                intro = False
                running = True
            elif event.key == K_BACKSPACE:
                username = username[:len(username) -1]
            else:
                if event.key < 255:
                    username += chr(event.key)
    highscore, by = getHighScore()
    screen.fill((42, 203, 235))
    write('Type your name', (500, 50), ((SCREEN_WIDTH/2)-250, 150), 60)
    write(username, (500, 50), ((SCREEN_WIDTH/2)-100, 300), 60)
    write('HIGHSCORE: ' + highscore + ' by ' + by, (500, 50), ((SCREEN_WIDTH/2)-250, 400), 40)
    pygame.display.flip()   
    clock.tick(30)

pygame.mixer.music.load('sound/helicoptersound.mp3') 
pygame.mixer.music.play(loops=-1)
collisionsound = pygame.mixer.Sound("sound/Blop.mp3")

def post_crash():
    write('GAME OVER', (320, 100), ((SCREEN_WIDTH/2)-140, (SCREEN_HEIGHT/2) - 50), 60)
    postcrash = True
    return_to_game = False
    while postcrash:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                elif event.key == K_SPACE:
                    return_to_game = True
                    postcrash = False
                elif event.key == K_RETURN:
                    return_to_game = True
                    postcrash = False
        for entity in all_sprites:
            entity.kill()
        pygame.display.update()  
        clock.tick(30)
    return return_to_game



while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                collisionsound.stop()
                pygame.mixer.music.stop()
                pygame.quit()
            elif event.key == K_SPACE:
            
                if gamepaused() == True:
                    running = False
        elif event.type == QUIT:
            collisionsound.stop()
            pygame.mixer.music.stop()
            pygame.quot()
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDBALLOON:
            new_balloon = Balloon()
            balloons.add(new_balloon)
            all_sprites.add(new_balloon)
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
        

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    enemies.update()
    balloons.update()
    clouds.update()


    screen.fill((42, 203, 235))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    if pygame.sprite.spritecollideany(player, enemies):
        pygame.mixer.music.stop()
        logHighscore(username, score)
        score = 0
        current_level = 10
        ticks = 20
        if post_crash() == False:
            running = False
        else:
            pygame.mixer.music.play(loops=-1)
            player = Player()
            all_sprites.add(player)


    
    collected = pygame.sprite.spritecollide(player, balloons, True)
    for _ in collected:
        collisionsound.play() 
        score += 1
        if score == current_level:
            current_level = current_level * 2.5
            ticks = ticks * 1.2

    s_surf = pygame.Surface((300,50))
    s_surf.fill((42, 203, 235))

    keepScore(s_surf)
    screen.blit(s_surf, (SCREEN_WIDTH-100, 0))

    pygame.display.flip()
    clock.tick(ticks)







