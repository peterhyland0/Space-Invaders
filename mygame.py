import pygame, sys
from user import User
import cover
from alien import Alien
from random import choice
from missile import Missile

class MyGame:
    def __init__(self):
        user_sprite = User((screen_width/ 2, screen_height), screen_width, 5 )
        self.user = pygame.sprite.GroupSingle(user_sprite)

        self.lives = 3
        self.lives_amount = pygame.image.load('/Users/peter/Desktop/2nd_year/programming/space_invaders/images/ship.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.lives_amount.get_size()[0] * 2 + 20)

        self.shape = cover.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.cover_amount = 4
        self.cover_x_positions = [num * (screen_width / self.cover_amount) for num in range(self.cover_amount)]
        self.create_multiple_covers(*self.cover_x_positions,x_start = screen_width/15,y_start = 480)

        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows=6,cols=8)
        self.alien_direction = 1
        self.alien_missiles = pygame.sprite.Group()


    def create_cover(self, x_start, y_start,offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index,col in enumerate(row):
                 if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = cover.Block(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)

    def create_multiple_covers(self,*offset,x_start,y_start):
        for offset_x in offset:
            self.create_cover(x_start,y_start,offset_x,)

    def alien_setup(self,rows,cols,x_distance = 60, y_distance = 48, x_offset=70, y_offset=100):
        for row_index,row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                alien_sprite = Alien(x,y)    
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        distance = 1
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                if self.aliens:
                    for alien in self.aliens.sprites():
                        alien.rect.y += distance
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                if self.aliens:
                    for alien in self.aliens.sprites():
                        alien.rect.y += distance

    def alien_missile(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            missile_sprite = Missile(random_alien.rect.center,6,screen_height)
            self.alien_missiles.add(missile_sprite)

    def collision_checks(self):

        if self.user.sprite.missiles:
            for missile in self.user.sprite.missiles:
                if pygame.sprite.spritecollide(missile,self.blocks,True):
                    missile.kill()

                if pygame.sprite.spritecollide(missile,self.aliens,True):
                    missile.kill()

                if pygame.sprite.spritecollide(missile,self.alien_missiles,True):
                    missile.kill()

        if self.alien_missiles:
            for missile in self.alien_missiles:
                if pygame.sprite.spritecollide(missile,self.blocks,True):
                    missile.kill()

                if pygame.sprite.spritecollide(missile,self.user,False):
                    missile.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)

                if pygame.sprite.spritecollide(alien,self.user,False):
                    sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * self.lives_amount.get_size()[0] + 10)
            screen.blit(self.lives_amount,(x,8))
                    


    def run(self):
        self.user.update()
        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        
        self.alien_missiles.update()
        self.collision_checks()
        self.display_lives()

        self.user.sprite.missiles.draw(screen)
        self.user.draw(screen)

        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_missiles.draw(screen)
        


if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_height, screen_width))
    clock = pygame.time.Clock()
    mygame = MyGame()
    alienMissile = pygame.USEREVENT + 1
    pygame.time.set_timer(alienMissile, 750)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == alienMissile:
                mygame.alien_missile()

        screen.fill((30,30,30))
        mygame.run()
        
        pygame.display.flip()
        clock.tick(60)
      