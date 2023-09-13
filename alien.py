import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('/Users/peter/Desktop/2nd_year/programming/space_invaders/images/alien.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))

    def update(self, direction):
        self.rect.x += direction

        