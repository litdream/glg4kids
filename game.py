#!/usr/bin/env python2

import sys
import pygame
import random
import time

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
RED  = ( 255,0,0)
GREEN = (0, 255,0)

#
# Resizing image: (with ImageMagic)
#   convert image.jpg -resize 50% image_new.jpg
#
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        if sys.version[0] == '2':
            pygame.sprite.Sprite.__init__(self)
        else:
            super().__init__()
        self.image = pygame.image.load("galaga-ship.jpg").convert()
        self.rect = self.image.get_rect()
        self.rect.x = 400/2
        self.rect.y = 600 - 100

        self.move_left = False
        self.move_right = False

    def update(self):
        speed = 0
        if self.move_left:
            speed -= 3
        if self.move_right:
            speed += 3
        self.rect.x += speed

        if self.rect.x < 10:
            self.rect.x = 10
        if self.rect.x > 370:
            self.rect.x = 370


        
class Bee(pygame.sprite.Sprite):
    def __init__(self, badbull, x,y, gif="galaga-bee.gif"):
        if sys.version[0] == '2':
            pygame.sprite.Sprite.__init__(self)
        else:
            super().__init__()
        self.image = pygame.image.load(gif).convert()
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move = 0

        self.badbull = badbull
        self.shoot = random.randint(50,300)
        
    def update(self):
        if self.move == 0:
            self.move = 40
            if random.randint(0,1) == 0:
                self.move = -40

        if self.move > 0:
            self.rect.x += 1
            self.move -= 1
        else:
            self.rect.x -= 1
            self.move += 1

        if self.rect.x < 10:
            self.rect.x = 10
        if self.rect.x > 370:
            self.rect.x = 370

        self.shoot -= 1
        if self.shoot < 0:
            self.shoot = random.randint(50,300)
            b = BadBullet(self.badbull, self.rect.x, self.rect.y)
            self.badbull.add(b)

class BossGalaga(Bee):
    def __init__(self, badbull, x,y):
        if sys.version[0] == '2':
            Bee.__init__(self, badbull, x,y, "boss_galaga.gif")
        else:
            super().__init__(badbull, x,y, "boss_galaga.gif")

class ButterFly(Bee):
    def __init__(self, badbull, x,y):
        if sys.version[0] == '2':
            Bee.__init__(self, badbull, x,y, "galaga-butter-fly.png")
        else:
            super().__init__(badbull, x,y, "boss_galaga.gif")            

        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullets, x):
        if sys.version[0] == '2':
            pygame.sprite.Sprite.__init__(self)
        else:
            super().__init__()
        self.bulletGroup = bullets
        
        self.image = pygame.Surface([4, 10])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x+20
        self.rect.y = 550
        
        self.bulletGroup.add(self)
        
    def update(self):
        self.rect.y -= 10
        if self.rect.y < 0:
            self.bulletGroup.remove(self)

class BadBullet(pygame.sprite.Sprite):
    def __init__(self, bullets, x,y):
        if sys.version[0] == '2':
            pygame.sprite.Sprite.__init__(self)
        else:
            super().__init__()
        self.bulletGroup = bullets
        
        self.image = pygame.Surface([4, 10])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = x+20
        self.rect.y = y

        self.bulletGroup.add(self)
        
    def update(self):
        self.rect.y += 3
        if self.rect.y > 600:
            self.bulletGroup.remove(self)            

            
class BowlingBall(pygame.sprite.Sprite):
    def __init__(self, bullets, x, offset=3, bowl_w=200, bowl_h=200):
        if sys.version[0] == '2':
            pygame.sprite.Sprite.__init__(self)
        else:
            super().__init__()
        self.bulletGroup = bullets
        self._add_bowl(bowl_w, bowl_h, offset)

    def _add_bowl(self, bowl_width, bowl_height, offset):    
        size = (bowl_width, bowl_height)
        self.offset= offset
        self.image = pygame.Surface(size)
        self.image.fill(WHITE)
        self.image = pygame.image.load("red-bowl.jpg").convert()
        pygame.draw.circle(self.image, WHITE, (x,550),50)
        self.rect = self.image.get_rect()

        self.rect.x = x+20
        self.rect.y = 550
        self.bulletGroup.add(self)
        
    def update(self):
        self.rect.y -= self.offset
        if self.rect.y < 0:
            self.bulletGroup.remove(self)

class FastBowlingBall(BowlingBall):
    def __init__(self, bullets, x, offset=30):
        if sys.version[0] == '2':
            BowlingBall.__init__(self, bullets, x, offset)
        else:
            super().__init__(bullets, x, offset)

class VerySlowBowlingBall(BowlingBall):
    def __init__(self, bullets, x, offset=2 ):
        if sys.version[0] == '2':
            BowlingBall.__init__(self, bullets, x, offset, 500,200)
        else:
            super().__init__(bullets, x, offset, 500,200)

            
class LittleStar(pygame.sprite.Sprite):
    def __init__(self, x,y):
        if sys.version[0] == '2':
            pygame.sprite.Sprite.__init__(self)
        else:
            super().__init__()
        self.image = pygame.Surface((2,2))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += 1
        if self.rect.y > 600:
            self.rect.y = 0
            
def shoot(bullets, ship):
    if len(bullets) < 5:
        newBullet = Bullet(bullets, ship.rect.x)
        pygame.mixer.music.load('laser1.ogg')
        pygame.mixer.music.play()

def bowl(bullets, ship):
    if len(bullets) < 2:
        newBullet = BowlingBall(bullets, ship.rect.x)
        #newBullet = FastBowlingBall(bullets, ship.rect.x)
        #newBullet = VerySlowBowlingBall(bullets, ship.rect.x)

        #pygame.mixer.music.load('laser1.ogg')
        pygame.mixer.music.load('bowl.ogg')
        pygame.mixer.music.play()

def buldozer(bullets, ship):
    if len(bullets) < 1:
        newBullet = VerySlowBowlingBall(bullets, ship.rect.x)

        pygame.mixer.music.load('bowl.ogg')
        pygame.mixer.music.play()

        
if __name__ == '__main__':
    FULL_SOUND = True
    WIN = False
    mode = "bullet"
    try:
        mode = sys.argv[1]
        FULL_SOUND = False
    except:
        pass
    
    pygame.init()

    screen = pygame.display.set_mode((400,600))

    allSprites = pygame.sprite.Group()
    goodGuys = pygame.sprite.Group()
    badGuys  = pygame.sprite.Group()
    bullets  = pygame.sprite.Group()
    badBullets = pygame.sprite.Group()

    ship = Ship()
    allSprites.add(ship)
    goodGuys.add(ship)

    for i in range(0,4):
        boss = BossGalaga(badBullets,
            random.randint(50,350), 
            random.randint(1,4)*50 + 10)
        allSprites.add(boss)
        badGuys.add(boss)
        
    for i in range(0,7):
        bee = Bee( badBullets,
                  random.randint(50,350),
                   random.randint(1,4)*50 + 10)
        allSprites.add(bee)
        badGuys.add(bee)

    for i in range(0,3):
        butfly = ButterFly(badBullets,
                  random.randint(50,350),
                   random.randint(1,4)*50 + 10)
        allSprites.add(butfly)
        badGuys.add(butfly)
            
    for i in range(0,50):
        x = random.randint(0,400)
        y = random.randint(0,600)
        star = LittleStar(x,y)
        allSprites.add(star)


    allSprites.update()
    allSprites.draw(screen)
    bullets.draw(screen)

    if FULL_SOUND:
        pygame.mixer.music.load('opening.ogg')
        pygame.mixer.music.play()
        time.sleep(7)
    
    clock = pygame.time.Clock()
    done = False

    while not done:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    ship.move_left = True
                if event.key == pygame.K_RIGHT:
                    ship.move_right = True
                if event.key == pygame.K_SPACE:
                    if mode == "bullet":
                        shoot(bullets, ship)
                    elif mode == "bowl":
                        bowl(bullets, ship)
                    elif mode == "buldozer":
                        buldozer(bullets, ship)
                        
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    ship.move_left = False
                if event.key == pygame.K_RIGHT:
                    ship.move_right = False
                    
        allSprites.update()
        bullets.update()
        badBullets.update()
        
        # detect shoot hit.
        for bullet in bullets:
            blocks_hit_list = pygame.sprite.spritecollide(bullet, badGuys, True)
            for bee in blocks_hit_list:
                pygame.mixer.music.load('hit.ogg')
                pygame.mixer.music.play()
                if mode not in ( "bowl", "buldozer" ):
                    bullets.remove(bullet)

        # detect player hit
        for bul in badBullets:
            bulHit = pygame.sprite.spritecollide(bul, goodGuys, True)

            if bulHit:
                pygame.mixer.music.load('atari_boom5.ogg')
                pygame.mixer.music.play()
                time.sleep(2)
                print('''\
***************************************************************************
YOU LOST!!
***************************************************************************\n''')
                done = True
                
        if len(badGuys) == 0:
            
            print('''\
===========================================================================
YOU WON!!
===========================================================================\n''')
            done = True
            WIN = True
            
        allSprites.draw(screen)
        bullets.draw(screen)
        badBullets.draw(screen)
        
        clock.tick(60)
        pygame.display.flip()

    if FULL_SOUND and WIN:
        pygame.mixer.music.load('applause.ogg')
        pygame.mixer.music.play()
        time.sleep(5)
    pygame.quit()
