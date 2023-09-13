import pygame
from missile import Missile


class User(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load('/Users/peter/Desktop/2nd_year/programming/space_invaders/images/ship.png')
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.x_constraint = constraint
        self.ready = True
        self.missile_time = 0
        self.missile_cooldown = 600

        self.missiles = pygame.sprite.Group()
        

    
    def get_key(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_missile() 
            self.ready = False
            self.missile_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.missile_time >= self.missile_cooldown:
                self.ready = True

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.x_constraint:
            self.rect.right = self.x_constraint

    def shoot_missile(self):
        self.missiles.add(Missile(self.rect.center,-8,self.rect.bottom))
    

    def update(self):
        self.get_key()
        self.constraint()
        self.recharge()
        self.missiles.update()