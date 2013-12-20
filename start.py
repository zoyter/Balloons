#!/usr/bin/python
#-*-coding:utf-8-*-
"""
Компьютерная игра "Balloons".
Игорку необходимо проколоть как можно больше шариков за отведенное время.
После удачного прокалывания шарика начисляются баллы, после того как шарик улетел у игрока отнимается попытка.
"""
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
        self.speed=15 #скокрость движения шариков
        #Оставаться в цикле, пока пользователь не нажмёт на кнопку закрытия окна
        self.menu=True
        self.earthquake=0 # Дрожжание экрана
        self.earthquake_time=0 #Время в течении которого экран дрожжит        

        # Используется для контроля частоты обновления экрана
        self.clock=pygame.time.Clock()   
        pygame.font.init()

        font = pygame.font.Font(None, 25) #для вывода игровой информации
        font2 = pygame.font.Font(None, 80) #для вывода крупных надписей
        #Прячем курсор
        pygame.mouse.set_visible(0)
        
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
            
#Добавить потом позиционирование окна по центру экрана
#
####################        
            self.screen=pygame.display.set_mode(self.size)
            pygame.display.set_caption(GAME_CAPTION)
            self.screen=pygame.display.get_surface() #Получаем объект-экран
            self.load_data()


##    #Создаем список с информацией о шариках
##    #координаты, картинка, скорость.
##       
##    #координаты, картинка, скорость.
##    #img,x,y,speed
##    balloons=[]
##    for i in range(count):
##        balloons.append([random.randint(1,6),
##                        random.randrange(size[0]-images['balloon1'].get_width()-30),
##                        random.randrange(size[1]),
##                        random.randint(speed//1.5,speed)]
##                        )
##        


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
            except pygame.error, message:
                print ERROR_LOADING_IMAGE, fullname
                raise SystemExit, message
            return image, image.get_rect()


    def load_data(self):
        '''
        Загрузка данных
        '''
        self.balloons_img=[]
        try:
            self.background=self.load_img("fon1.jpg")[0]
            self.balloons.append(self.load_img("balloon1.png"))
            self.balloons.append(self.load_img("balloon2.png"))
            self.balloons.append(self.load_img("balloon3.png"))
            self.balloons.append(self.load_img("balloon4.png"))
            self.balloons.append(self.load_img("balloon5.png"))
            self.cursor=self.load_img("cursor.png")
            self.paper=self.load_img("paper1.png")[0]
            self.paper.set_colorkey((0,0,0))
        except pygame.error, message:
            print ERROR_LOADING_IMAGE, fullname
            self.done=True
            raise SystemExit, message

        

        #Загружаем музыку
        print("трек Johaness Gilther - Subcarpathia (Original Mix)Album artwork")
        print("http://www.jamendo.com/en/track/1003419/johaness-gilther-subcarpathia-original-mix")

        try:
            pygame.mixer.music.load(self.path+'/snd/2Inventions_-_Johaness_Gilther_-_Subcarpathia__Original_Mix_.mp3')
            # Начинаем проигрывать музыку,
            pygame.mixer.music.play()
        except pygame.error, message:
            print ERROR_LOADING_SOUND, fullname
            self.done=True
            raise SystemExit, message

        #Загружаем взрыв
        print("Звуки взрывов откуда-то из интернета")
        try:
            self.soundBoom1=pygame.mixer.Sound(self.path+'/snd/gun1.wav')
            self.soundBoom1.set_volume(0.1)
            self.soundBoom2=pygame.mixer.Sound(self.path+'/snd/gun2.wav')
            self.soundBoom2.set_volume(0.3)
            self.soundLevel=pygame.mixer.Sound(self.path+'/snd/iron2.wav')
        except pygame.error, message:
            print ERROR_LOADING_SOUND, fullname
            self.done=True
            raise SystemExit, message

    def draw_npc(self):
        ''' Метод draw_npc обрабатывает события		для игровых объектов и выполняет их отрисовку на		холсте '''
        pass
    
    def draw_player(self):
        '''
        Метод draw_player обрабатывает события для игрока и выполняет его отрисовку на холсте
        '''		
        pass


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
