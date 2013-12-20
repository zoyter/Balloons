#!/usr/bin/python
#-*-coding:utf-8-*-
'''
Компьютерная игра "Balloons".
Игорку необходимо проколоть как можно больше шариков за отведенное время.
После удачного прокалывания шарика начисляются баллы, после того как шарик улетел у игрока отнимается попытка.
'''
# (c) Oleg Lyash
#
VERSION = "0.5"

#
try:
    from lang import *
    import sys
    import os
    import pygame
    from pygame.locals import *
except ImportError, err:
    print ERROR_LOADING_MODULES+" %s" % (err)
    sys.exit(2)

def load_png(name):
        ''' Загружает изображение
        возвращает объект-изображение '''
        fullname = os.path.join('data', name)
        try:
            image = pygame.image.load(fullname)
            if image.get_alpha is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except pygame.error, message:
            print ERROR_LOADING_IMAGE, fullname
            raise SystemExit, message
        return image, image.get_rect()
    
##class Balloon(pygame.sprite.Sprite):
##    ''' Воздушный шарик, кторый движется снизу вверх
##        Возвращает: объект Balloon
##        Функции: update, calcnewpos
##        Атрибуты: area, vector'''
##    def __init__(self, (xy), vector):
##        pygame.sprite.Sprite.__init__(self)
##        self.image, self.rect = load_png('balloon01.png')
##        screen = pygame.display.get_surface()
##        self.area = screen.get_rect()
##        self.vector = vector
##        self.hit = 0    
        
class Game():
    ''' Базовый класс игры
    '''
    def __init__(self,Fullscreen):
        '''Инициализация игры
        '''
        print(CREATE_GAME_CLASS)
        self.path="data"
        self.done=False
        self.pause=False
        pygame.init()
        if Fullscreen:
            print(FULLSCREEN_ENABLE)
            self.size=[pygame.display.list_modes()[0][0],pygame.display.list_modes()[0][1]]
            self.screen=pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        else:
            print(FULLSCREEN_DISABLE)
            self.size=[800,600]
            self.screen=pygame.display.set_mode(self.size)
            pygame.display.set_caption(GAME_CAPTION)
            self.screen=pygame.display.get_surface() #Получаем объект-экран
            self.load_data()
            self.main_loop()

    def load_data(self):
        '''Загрузка данных
        '''
        self.background=pygame.image.load(self.path+"/img/fon1.jpg").convert()

    def draw_npc(self):
        pass

    def draw_player(self):
        pass


    def draw_scene(self):
        '''Отрисовка сцены
        '''
        self.screen.blit(self.background,[0,0])
        self.draw_npc()
        self.draw_player()

    def events(self):
        '''Обработка событий
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If user clicked close
                print(GOOD_BY)
                self.done=True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print(GOOD_BY)
                    self.done=True
                if event.key == pygame.K_SPACE:
                    self.pause=not(self.pause)
                    print(PAUSE_ENABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print('Нажали на кнопку мыши')

    def main_loop(self):
        '''Основной цикл игры
        '''
        while self.done==False:
            #Обработка событий
            self.events()
            #Отрисовка сцены
            self.draw_scene()
            #Вывод на экран
            pygame.display.flip()
        #Выход из программы
        pygame.quit()
		
		
		
		

def main():
    #True - enable Fullscreen
    BallonsGame = Game(False)	
	
	
main()
