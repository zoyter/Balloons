#!/usr/bin/python
#-*-coding:utf-8-*-
"""
Компьютерная игра "Balloons".
Игорку необходимо проколоть как можно больше шариков за отведенное время.
После удачного прокалывания шарика начисляются баллы, после того как шарик улетел у игрока отнимается попытка.
"""
# (c) Oleg Lyash (aka Zoyter) 2012
#
VERSION = "0.5"

try:
    from lang import *
    import sys
    import os
    import pygame
    import random
    from pygame.locals import *
except ImportError, err:
    print ERROR_LOADING_MODULES+" %s" % (err)
    sys.exit(2)

pygame.init()

class Balloon(pygame.sprite.Sprite):
    """  Шарик
    летит снизу вверх и может взрываться
    """
    def __init__(self, screen, img_filename,speed):        
        self._display_surf=screen
        self.image=self.load_png(img_filename)        
        self.pos=[None,None]
        self.speed=None
        self.alive=None
        
        self.boom=None
        self.boom_ttl_max=30
        self.boom_ttl=self.boom_ttl_max
        self.boom_img=pygame.image.load("data/img/boom.gif").convert_alpha()
        
        self.make_alive(speed)

    def make_alive(self,speed):
        '''Воскрешаем
        '''
        self.pos[0]=random.randrange(self._display_surf.get_bounding_rect()[2] - self.image.get_width() )        
        self.pos[1]=100 #self._display_surf.get_bounding_rect()[3]
        self.speed=random.randint(speed//1.5,speed)
        self.alive=True
        
    def load_png(self,filename):
        '''Загрузка изображения
        '''
        try:
            image = pygame.image.load(filename)
            if image.get_alpha is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except pygame.error, message:
            print ERROR_LOADING_IMAGE, filename
            raise SystemExit, message
        return image

        
    def update(self, time_passed,cursor_pos):
        l_edge=cursor_pos[0]>self.pos[0]
        r_edge=cursor_pos[0]<self.pos[0]+self.image.get_width()
        t_edge=cursor_pos[1]>self.pos[1]
        b_edge=cursor_pos[1]<self.pos[1]+self.image.get_height()
        if (l_edge and r_edge and t_edge and b_edge):
            self.boom=True
            
        
        if self.boom==False:
            #self.pos[1]-=self.speed
            if self.pos[1]<0-self.image.get_height():
                self.alive=False
                self.pos[1]=self._display_surf.get_bounding_rect()[3]
        else:
            self.boom_ttl-=1
            if self.boom_ttl<=0:
                self.boom_ttl=self.boom_ttl_max
                self.boom=False
                self.make_alive(5)


    def draw(self):
        if (self.alive==True and self.boom==False):
            self._display_surf.blit(self.image,self.pos)
        if (self.boom==True):
            self._display_surf.blit(self.boom_img,self.pos)
        
            
        
    def boom(self):
        '''Взрыв
        '''
        pass
    
 
class App:
    def __init__(self):        
        self._running = True
        self._display_surf = None  
        self.path='data/'
        self.path_img='img/'
        self.path_snd='snd/'
        self.speed=5
        self.life=10
        self.miss=0
        self.ballons_count=6
        self.pos=None
  
    def on_init(self,Fullscreen):
        pygame.init()
        
        self.fullscreen=Fullscreen
        
        if self.fullscreen:
            print("полноэкранный режим")
            self.size = self.width, self.height = pygame.display.list_modes()[0][0] , pygame.display.list_modes()[0][1]
            #self.size=[pygame.display.list_modes()[0][0],pygame.display.list_modes()[0][1]]                                 
            self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
        else:
            print("оконный режим")
            self.size = self.width, self.height = 800,600
            #Получаем размеры экрана
            scr_width=pygame.display.Info().current_w
            scr_height=pygame.display.Info().current_h
            #Позиционирование окна по центру экрана
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (scr_width//2-self.size[0]//2,scr_height//2-self.size[1]//2)
            self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
            
        pygame.display.set_caption(GAME_CAPTION)    

        #Фоновое изображение
        self.bg=pygame.image.load(self.path+self.path_img+'fon1.jpg')
        #Массив с шариками
        self.Balloons=[]
        for i in range(1,self.ballons_count+1):
            self.Balloons.append(Balloon(self._display_surf,self.path+self.path_img+'balloon'+str(i)+'.png',self.speed))
        

        
        self.pos=pygame.mouse.get_pos()

        self._running = True

    def draw_bg(self):
        '''Выводим фоновую картинку на холст
        '''
        self._display_surf.blit(self.bg,[0,0])
        
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            print("Пока")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Пока")
                self._running = False
            if event.key == pygame.K_SPACE:
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.pos=pygame.mouse.get_pos()
            print(self.pos)

    def on_mouse(self):
        if (pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]) :
            print('бабах ')
    
    def on_loop(self):
        for i in self.Balloons:
            i.update(10,self.pos)
            if i.alive==False:
                self.miss+=1
                i.make_alive(self.speed)
                
        
                
                
    def on_render(self):
        '''рендерим все и вся
        '''
        #Рисуем фон
        self.draw_bg()
        #рисуем шарик        
        for i in self.Balloons:
            i.draw()               
               
        
        #отображаем все на экране
        pygame.display.flip()
        
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init(False) == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
