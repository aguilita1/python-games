#!/usr/bin/env python3
# by Seth Kenlon

# GPLv3
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pygame
import sys
import os

'''
Variables
'''

worldx = 960
worldy = 720
fps = 40
ani = 4
world = pygame.display.set_mode([worldx, worldy])

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
ALPHA = (0, 255, 0)

'''
Objects
'''


class Player(pygame.sprite.Sprite):
    """
    Spawn a player
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.health = 10
        self.images = []
        self.jump_speed = -15
        self.gravity = 1
        self.jump_active = False
        self.on_ground = True  # Assume player starts on ground
        self.ground_y = 600
        self.manual_offset = 0  # Tracks manual up/down movement from ground level

        for i in range(1, 8):
            img = pygame.image.load(os.path.join('assets','images', 'hero' + str(i) + '.png'))
            img.convert_alpha()
            img.set_colorkey(ALPHA)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = self.ground_y

    def control(self, x, y):
        """
        control player movement
        """
        self.movex += x

        if self.on_ground:
            if y < 0 and self.manual_offset > -40:
                self.movey += y
                self.manual_offset += y
            elif y > 0 and self.manual_offset < 40:
                self.movey += y
                self.manual_offset += y

    def jump(self):
        if self.on_ground:
            self.movey = self.jump_speed
            self.on_ground = False

    def update(self):
        """
        Update sprite position
        """
        # Gravity
        if not self.on_ground:
            self.movey += self.gravity

        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

        # Simulate ground collision
        if self.rect.bottom >= self.ground_y + self.manual_offset:
            self.rect.bottom = self.ground_y + self.manual_offset
            self.movey = 0
            self.on_ground = True

        # Reset movey after applying
        if self.on_ground:
            self.movey = 0

        # moving left
        if self.movex < 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame // ani], True, False)

        # moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = self.images[self.frame//ani]

        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in hit_list:
            self.health -= 1
            print(self.health)


class Enemy(pygame.sprite.Sprite):
    """
    Spawn an enemy
    """
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 6):  # Assuming enemy1.png to enemy4.png
            img = pygame.image.load(os.path.join('assets', 'images', 'enemy' + str(i) + '.png'))
            img.convert_alpha()
            img.set_colorkey(ALPHA)
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0
        self.frame = 0
        self.movex = 0
        self.movey = 0
        self.counter = 0        
        self.direction = 1  # 1 = right, -1 = left

    def update(self):
        """
        Enemy movement and animation
        """
        patrol_distance = 80
        speed = 8

        # Patrol logic using movex
        if self.counter <= patrol_distance:
            self.movex = speed
            self.direction = 1
        elif self.counter <= patrol_distance * 2:
            self.movex = -speed
            self.direction = -1
        else:
            self.counter = 0

        self.counter += 1

        self.rect.x += self.movex
        self.rect.y += self.movey

        # Animation logic
        self.frame += 1
        if self.frame >= ani * len(self.images):
            self.frame = 0

        frame_image = self.images[self.frame // ani]

        if self.direction == -1:
            flipped_image = pygame.transform.flip(frame_image, True, False)
            self.image = flipped_image
        else:
            self.image = frame_image

        # Keep the image rect aligned with position
        old_center = self.rect.center  # preserve position
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        """
        Enemy movement and animation
        """
        patrol_distance = 80
        speed = 8

        # Patrol logic using movex
        if self.counter <= patrol_distance:
            self.movex = speed
            self.direction = 1
        elif self.counter <= patrol_distance * 2:
            self.movex = -speed
            self.direction = -1
        else:
            self.counter = 0

        self.counter += 1

        self.rect.x += self.movex
        self.rect.y += self.movey

        # Animation logic (same as Player)
        self.frame += 1
        if self.frame >= ani * len(self.images):
            self.frame = 0

        image = self.images[self.frame // ani]
        if self.direction == -1:
            self.image = pygame.transform.flip(image, True, False)
        else:
            self.image = image

class Level():
    def bad(lvl, eloc):
        if lvl == 1:
            enemy = Enemy(eloc[0], eloc[1])
            enemy_list = pygame.sprite.Group()
            enemy_list.add(enemy)
        if lvl == 2:
            print("Level " + str(lvl) )

        return enemy_list


'''
Setup
'''

backdrop = pygame.image.load(os.path.join('assets','images', 'stage.png'))
clock = pygame.time.Clock()
pygame.init()
backdropbox = world.get_rect()
main = True

player = Player()  # spawn player
player.rect.x = 0  # go to x
player.rect.y = 600  # go to y

player_list = pygame.sprite.Group()
player_list.add(player)
steps = 10

eloc = []


eloc = [300, 505]
enemy_list = Level.bad(1, eloc )

'''
Main Loop
'''

while main:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                main = False

        if event.type == pygame.KEYDOWN:
            if event.key == ord('q') or event.key == pygame.K_ESCAPE:
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(steps, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                player.control(0, -steps*10)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player.control(0, steps*10)                
            if event.key == pygame.K_SPACE:
                print('jump')
                player.jump()           
               
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-steps, 0)
            if event.key == pygame.K_UP or event.key == ord('w'):
                player.control(0, steps*10)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                player.control(0, -steps*10)


    world.fill(BLACK)  # Clear screen
    world.blit(backdrop, backdropbox)
    player.update()
    player_list.draw(world)
    enemy_list.update()
    enemy_list.draw(world)
    pygame.display.flip()
    clock.tick(fps)