#!/usr/bin/python
#-*-coding:utf-8-*-

# Copyright 2012 Oleg Lyash (aka Zoyter)
"""
 This file is part of Balloons.

    Balloons is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Balloons is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Balloons.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
Компьютерная игра "Balloons".
Игорку необходимо проколоть как можно больше шариков за отведенное время.
После удачного прокалывания шарика начисляются баллы, после того как шарик улетел у игрока отнимается попытка.
"""

#
VERSION = "0.5"

#
try:
    from lang import *
    import sys
    import os
    import pygame
    import random
    from pygame.locals import *
except ImportError(err):
    print (ERROR_LOADING_MODULES+" %s" % (err))
    sys.exit(2)


def load_img(name):
    '''
    Функция load_img загружает изображение
    Принимает name - имя файла
    Возвращает объект-изображение
    '''
    try:
        image = pygame.image.load(name)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error:
        print (ERROR_LOADING_IMAGE, name)
        raise SystemExit(message)
    return image, image.get_rect()

class Balloon(pygame.sprite.Sprite):
    '''
        Воздушный шарик, кторый движется снизу вверх
        Возвращает: объект Balloon
        Функции:
        Атрибуты:
    '''
    def __init__(self,path,name):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png(os.path.join(self.path+"/img/", name))
        self.screen = pygame.display.get_surface()
        self.alive=True
        self.X=0
        self.Y=0
        self.boom=False
    def renew(self):
        pass
    def move(self):
        pass
    def draw(self):
        pass
        self.screen


class Game():
    '''
    Класс Game формирует игру
    Метод _init_ принимает на вход логическую переменную, которая задает режим отображения (полноэкранный или оконный)
    '''
    def __init__(self,Fullscreen):
        '''
        Инициализация игры
        '''
        pygame.init()

        print(CREATE_GAME_CLASS)
        self.path="data"
        self.done=False
        self.pause=False
        #Задаем стартовые параметры игровым переменным
        self.level=1 #Уровень
        self.level_change=False #Флаг, показывающий смену уровня
        self.level_change_time=0 #Счетчик для задержки надписи о смене уровня на экране
        self.score_cur=0 #текущие очки
        self.score_add=10 #сколько добавлять за подбитый шарик
        self.score_next=100 #сколько очков надо заработать для перехода на следующий уровень
        self.score_step_next=100 #на сколько следует увеличить планку перехода на следующий уровень
        self.life=5 #кол-во жизней
        self.count=3 #кол-во шариков, которые видны на экране
        self.speed=5 #скокрость движения шариков
        #Оставаться в цикле, пока пользователь не нажмёт на кнопку закрытия окна
        self.menu=True
        self.earthquake=0 # Дрожжание экрана
        self.earthquake_time=0 #Время в течении которого экран дрожжит
        self.cursorX=0
        self.cursorY=0

        # Используется для контроля частоты обновления экрана
        self.clock=pygame.time.Clock()
        pygame.font.init()

        font = pygame.font.Font(None, 25) #для вывода игровой информации
        font2 = pygame.font.Font(None, 80) #для вывода крупных надписей
        #Прячем курсор
        #pygame.mouse.set_visible(0)

        if Fullscreen:
            print(FULLSCREEN_ENABLE)
            self.size=[pygame.display.list_modes()[0][0],pygame.display.list_modes()[0][1]]
            self.screen=pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        else:
            print(FULLSCREEN_DISABLE)
            self.size=[800,600]

            #Получаем размеры экрана
            scr_width=pygame.display.Info().current_w
            scr_height=pygame.display.Info().current_h

            #Позиционирование окна по центру экрана
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (scr_width//2-self.size[0]//2,scr_height//2-self.size[1]//2)

            self.screen=pygame.display.set_mode(self.size)
            pygame.display.set_caption(GAME_CAPTION)
            #Получаем объект-экран
            self.screen=pygame.display.get_surface()
            self.load_data()


        #Создаем список с информацией о шариках
        #координаты, картинка, скорость.
        #координаты, картинка, скорость.
        #img,x,y,speed
        self.balloons=[]
        for i in range(self.count):
            self.balloons.append([random.randint(1,6),
                            random.randrange(self.size[0]-self.balloons_img[0][0].get_width()-30),
                            random.randrange(self.size[1]),
                            random.randint(self.speed//1.5,self.speed)]
                            )



        self.main_loop()

    def load_img(self,name):
            '''
            Функция load_img загружает изображение
            Принимает name - имя файла
            Возвращает объект-изображение
            '''
            fullname = os.path.join(self.path+"/img/", name)
            try:
                image = pygame.image.load(fullname)
                if image.get_alpha is None:
                    image = image.convert()
                else:
                    image = image.convert_alpha()
            except pygame.error(message):
                print (ERROR_LOADING_IMAGE, fullname)
                raise SystemExit(message)
            return image, image.get_rect()


    def load_data(self):
        '''
        Загрузка данных
        '''
        self.balloons_img=[]
        try:
            self.background=self.load_img("fon1.jpg")[0]
            self.balloons_img.append(self.load_img("balloon1.png"))
            self.balloons_img.append(self.load_img("balloon2.png"))
            self.balloons_img.append(self.load_img("balloon3.png"))
            self.balloons_img.append(self.load_img("balloon4.png"))
            self.balloons_img.append(self.load_img("balloon5.png"))
            self.cursor=self.load_img("cursor.png")
            self.paper=self.load_img("paper1.png")[0]
            self.paper.set_colorkey((0,0,0))
        except pygame.error(message):
            print (ERROR_LOADING_IMAGE, fullname)
            self.done=True
            raise SystemExit(message)



        #Загружаем музыку
        print("трек Johaness Gilther - Subcarpathia (Original Mix)Album artwork")
        print("http://www.jamendo.com/en/track/1003419/johaness-gilther-subcarpathia-original-mix")

        try:
            pygame.mixer.music.load(self.path+'/snd/2Inventions_-_Johaness_Gilther_-_Subcarpathia__Original_Mix_.mp3')
            # Начинаем проигрывать музыку,
            pygame.mixer.music.play()
        except pygame.error(message):
            print (ERROR_LOADING_SOUND, fullname)
            self.done=True
            raise SystemExit(message)

        #Загружаем взрыв
        print("Звуки взрывов откуда-то из интернета")
        try:
            self.soundBoom1=pygame.mixer.Sound(self.path+'/snd/gun1.wav')
            self.soundBoom1.set_volume(0.1)
            self.soundBoom2=pygame.mixer.Sound(self.path+'/snd/gun2.wav')
            self.soundBoom2.set_volume(0.3)
            self.soundLevel=pygame.mixer.Sound(self.path+'/snd/iron2.wav')
        except pygame.error( message):
            print (ERROR_LOADING_SOUND, fullname)
            self.done=True
            raise SystemExit( message)

    def draw_npc(self):
        ''' Метод draw_npc обрабатывает события     для игровых объектов и выполняет их отрисовку на        холсте '''
        for i in self.balloons:
            i[2]-=i[3]
            if i[2]<0:
                i[2]=self.size[1]
            self.screen.blit(self.balloons_img[i[0]][0],[i[1],i[2]])

    def draw_player(self):
        '''
        Метод draw_player обрабатывает события для игрока и выполняет его отрисовку на холсте
        '''
        self.screen.blit(self.cursor[0],[self.cursorX,self.cursorY])


    def draw_scene(self):
        '''
        Отрисовка сцены
        '''
        self.screen.blit(self.background,[0,0])
        self.draw_npc()
        self.draw_player()

    def events(self):
        '''Обработка событий
        '''
        pos = pygame.mouse.get_pos()
        self.cursorX=pos[0]
        self.cursorY=pos[1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Если пользователь нажал кнопку закрытия окна
                print(GOOD_BY)
                # Выставить флаг завершения игры
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
                    print('Нажали на левую кнопку мыши')
                if event.button == 3:
                    print('Нажали на правую кнопку мыши')

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
    #True - включить полноэкранный режим
    #False - выключить полноэкранный режим
    BallonsGame = Game(False)

main()
