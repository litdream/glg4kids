#!/usr/bin/env python2

import sys
import pygame
import random
import time

BOWL = False

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
    def __init__(self, badbull, x,y):
        if sys.version[0] == '2':
            pygame.sprite.Sprite.__init__(self)
        else:
            super().__init__()
        self.image = pygame.image.load("galaga-bee.gif").convert()
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
    def __init__(self, bullets, x):
        if sys.version[0] == '2':
            pygame.sprite.Sprite.__init__(self)
        else:
            super().__init__()
        self.bulletGroup = bullets
        size = (200,200)
        self.image = pygame.Surface(size)
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, WHITE, (x,550),50)
        self.rect = self.image.get_rect()

        self.rect.x = x+20
        self.rect.y = 550
        self.bulletGroup.add(self)
        
    def update(self):
        self.rect.y -= 3
        if self.rect.y < 0:
            self.bulletGroup.remove(self)

class FastBowlingBall(pygame.sprite.Sprite):
    def __init__(self, bullets, x):
        if sys.version[0] == '2':
            pygame.sprite.Sprite.__init__(self)
        else:
            super().__init__()
        self.bulletGroup = bullets
        size = (400,200)
        self.image = pygame.Surface(size)
        #self.image.fill(RED)
        self.image.fill(GREEN)
        pygame.draw.circle(self.image, WHITE, (x,550),50)
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 550
        self.bulletGroup.add(self)
        
    def update(self):
        self.rect.y -= 30
        if self.rect.y < 0:
            self.bulletGroup.remove(self)

            
class VerySlowBowlingBall(pygame.sprite.Sprite):
    def __init__(self, bullets, x):
        if sys.version[0] == '2':
            pygame.sprite.Sprite.__init__(self)
        else:
            super().__init__()
        self.bulletGroup = bullets
        size = (400,200)
        self.image = pygame.image.load("red-bowl.jpg").convert()
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = 350
        self.bulletGroup.add(self)
        self.slower = 3
        
    def update(self):
        self.slower -= 1
        if self.slower == 0:
            self.rect.y -= 1
            self.slower = 3
            
        if self.rect.y < 0:
            self.bulletGroup.remove(self)

            
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
        #newBullet = BowlingBall(bullets, ship.rect.x)
        #newBullet = FastBowlingBall(bullets, ship.rect.x)
        newBullet = VerySlowBowlingBall(bullets, ship.rect.x)

        #pygame.mixer.music.load('laser1.ogg')
        pygame.mixer.music.load('bowl.ogg')
        pygame.mixer.music.play()

if __name__ == '__main__':
    FULL_SOUND = True
    WIN = False
    try:
        s = sys.argv[1]
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

    for i in range(0,10):
        bee = Bee( badBullets,
                  random.randint(50,350),
                  random.randint(0,4)*50)
        allSprites.add(bee)
        badGuys.add(bee)

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
                    if BOWL:
                        bowl(bullets, ship)
                    else:
                        shoot(bullets, ship)

                    
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
                if not BOWL:
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
