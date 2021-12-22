import os.path
import random
import pygame
from random import randrange
from dot import Dot
from slider_bar import SliderBar
from chief import Chief

BLACK = (0, 0, 0)
RED = (255, 0, 0)

PAN_COLOR = '#FFAD7E'



class Slider:

    def __init__(self, win):
        self.combo = 0
        self.lives = 3
        self.score = 0
        self.combo_clear = 0
        self.window = win
        self.mode = 'game'

        self.hit_sound = pygame.mixer.Sound(os.path.join('assets', 'sound', 'hit.mp3'))
        self.miss_sound = pygame.mixer.Sound(os.path.join('assets', 'sound', 'miss.mp3'))
        #self.bgm = pygame.mixer.Sound(os.path.join('assets', 'sound', 'bgm_120.mp3'))
        #self.bgm.set_volume(0.1)
        self.hit_sound.set_volume(0.1)
        self.miss_sound.set_volume(0.1)

        self.bg_picture = pygame.image.load(os.path.join('assets', 'slider_bg.png')).convert()
        self.bar_picture = pygame.image.load(os.path.join('assets', 'bar.png')).convert_alpha()
        self.bar_rect = self.bar_picture.get_rect(midtop=(self.window.get_width()/2, 139))

        self.font = pygame.font.SysFont('Roboto', 40)
        self.lives_text = self.font.render(f'{self.lives}', 1, BLACK)

        self.list_of_buttons = []

        self.chief = pygame.sprite.Group()
        self.chief_pointer = Chief()
        self.chief.add(self.chief_pointer)

        self.dot_group = pygame.sprite.Group()

        self.slider_bar = pygame.sprite.GroupSingle()
        self.slider_bar_ref = SliderBar(self.bar_rect, self.bar_rect.x, self.bar_rect.y)
        self.slider_bar.add(self.slider_bar_ref)

    '''
    def generate_dot(self):
        difficulty = 25
        y = self.bar_rect.y + 5
        x = random.randint(self.bar_rect.x, self.bar_rect.x + self.bar_rect.width - difficulty)
        self.dots_list.append(pygame.Rect(10, 10, 10, 10))
    '''

    def generate_slider(self):
        size = 5
        y = self.bar_rect.y
        x = self.bar_rect.x
        return pygame.Rect(x, y, size, self.bar_rect.height)


    def slider_edge_check(self):
        if self.slider_bar_ref.rect.x == self.bar_rect.x:
            self.dot_group.empty()
            if self.combo == 3:
                self.combo_clear = 0
                self.combo = 0
            else:
                self.combo_clear += 1
                if self.combo_clear == 3:
                    self.lives -= 1
                    self.combo_clear = 0
                    self.check_lives()
                self.combo = 0
            coords_for_bars = []
            while len(coords_for_bars) < 3:
                coord = (randrange(self.bar_rect.x + int(self.bar_rect.width / 8),
                          self.bar_rect.x + self.bar_rect.width - int(self.bar_rect.width / 8),
                          int(self.bar_rect.width / 8)))
                if coord not in coords_for_bars:
                    coords_for_bars.append(coord)
            for x_pos in coords_for_bars:
                self.dot_group.add(Dot(x_pos, self.bar_rect.y + 6))

    def check_lives(self):
        if self.lives <= 0:
            self.mode = 'retry_screen'

    def hit_check(self):
        if pygame.sprite.spritecollide(self.slider_bar.sprite, self.dot_group, True):
            self.hit_sound.play()
            self.combo += 1
        else:
            self.miss_sound.play()
            self.lives -= 1
            self.check_lives()
        if self.combo == 3:
            self.chief_pointer.flip_anim_counter += 60
            self.score += 1



    def update_lives_text(self):
        self.lives_text = self.font.render(f'{self.lives}', 1, BLACK)

    def make_screenshot(self):
        self.window.blit(self.bg_picture, (0, 0))
        score_text = self.font.render(f'{self.score}', 1, BLACK)
        self.window.blit(self.lives_text, (154, 63))
        self.window.blit(self.bar_picture, self.bar_rect)
        self.window.blit(score_text, (929, 63))
        self.chief.draw(self.window)
        self.dot_group.draw(self.window)
        self.slider_bar.draw(self.window)

        rect = self.window.get_rect()
        sub = self.window.subsurface(rect)
        self.sub = sub.copy()
        self.sub = pygame.transform.smoothscale(pygame.transform.smoothscale(self.sub, (self.window.get_width()/25, self.window.get_height()//25)), (self.window.get_width(), self.window.get_height()))





    '''
    def hit_check_3(self):
        for dot in self.dots_list:
            if dot.colliderect(self.slider):
                self.dots_list.remove(dot)
                return True
            else:
                self.lives -= 1
                self.update_lives_text()
                return []

    def hit_check_2(self):
        for dot in self.dots_list:
            if dot.colliderect(self.slider):
                self.dots_list.remove(dot)
                return True
            else:
                self.lives -= 1
                self.update_lives_text()
    '''

    def main_loop(self):
        if self.mode == 'game':
            self.slider_edge_check()
            self.window.blit(self.bg_picture, (0, 0))
            score_text = self.font.render(f'{self.score}', 1, BLACK)
            self.update_lives_text()
            self.window.blit(self.lives_text, (154, 63))

            self.window.blit(self.bar_picture, self.bar_rect)
            self.window.blit(score_text, (929, 63))

            self.chief.update()

            self.chief.draw(self.window)

            #if len(self.dot_group) <= 0:
            #    for _ in range(3):
            #        self.dot_group.add(Dot(randrange(self.bar_rect.x + int(self.bar_rect.width / 8) , self.bar_rect.x + self.bar_rect.width - int(self.bar_rect.width / 8), int(self.bar_rect.width / 8)), self.bar_rect.y+6))

            self.dot_group.draw(self.window)
            self.slider_bar.draw(self.window)
            self.slider_bar.update(int(self.bar_rect.width/2/120))
            self.bars_draw()
            return True

        elif self.mode == 'retry_screen':
            self.make_screenshot()
            return False


    def bars_draw(self):
            pygame.draw.line(self.window, 'red', self.bar_rect.midtop, self.bar_rect.midbottom)
            pygame.draw.line(self.window, 'red', self.bar_rect.topleft, self.bar_rect.bottomleft)
            pygame.draw.line(self.window, 'red', self.bar_rect.topright, self.bar_rect.bottomright)


