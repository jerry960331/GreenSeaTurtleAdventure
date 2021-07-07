import pygame
import os, sys
import model
import random
from eventmanager import *
import src
import configparser
import os.path
from models import TurtleMC
from models import Straw
from models import Heart


BACKGROUND_BLUE = (93, 189, 245)
WHITE = (255, 255, 255)
WINDOW_HEIGHT = None
WINDOW_WIDTH = None

class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """

    def __init__(self, evManager, model):
        """
        evManager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.

        Attributes:
        isinitialized (bool): pygame is ready to draw.
        screen (pygame.Surface): the screen surface.
        clock (pygame.time.Clock): keeps the fps constant.
        smallfont (pygame.Font): a small font.
        """
        #pygame.init()
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model
        self.isinitialized = False
        self.screen = None
        self.clock = None
        self.smallfont = None

        self.turtleCounter = 0
        self.intro_text_alpha = 255



    def notify(self, event):
        """
        Receive events posted to the message queue.
        """

        if isinstance(event, InitializeEvent):
            self.initialize()

            self.background_image = pygame.image.load("src/background.png").convert_alpha()

            # add turtle object
            self.creature = TurtleMC.TurtleMC(1/5, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

            # 生成吸管
            self.straws = pygame.sprite.Group()
            strawNum = 20
            for i in range(strawNum):
                self.straws.add(Straw.Straw(self.WINDOW_WIDTH, random.randint(self.WINDOW_WIDTH, self.WINDOW_WIDTH*2), (self.WINDOW_HEIGHT/strawNum)*i+10))

            # 生成心臟
            self.hearts = pygame.sprite.Group()
            heartNum = 2
            heartSize = 52
            for i in range(heartNum):
                self.hearts.add(Heart.Heart(0 + i * heartSize, self.WINDOW_HEIGHT - heartSize, heartSize))

        elif isinstance(event, QuitEvent):
            # shut down the pygame graphics
            self.isinitialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
            if not self.isinitialized:
                return
            currentstate = self.model.state.peek()
            if currentstate == model.STATE_INTRO:
                self.renderintro()
            if currentstate == model.STATE_MENU:
                self.rendermenu()
            if currentstate == model.STATE_PLAY:
                self.renderplay()
            if currentstate == model.STATE_HELP:
                self.renderhelp()

            # 鍵盤上下左右的狀態
            if currentstate == model.STATE_RIGHT:
                self.renderRight()
            if currentstate == model.STATE_LEFT:
                self.renderLeft()
            if currentstate == model.STATE_UP:
                self.renderUp()
            if currentstate == model.STATE_DOWN:
                self.renderDown()


            # 設定 60 FPS
            self.clock.tick(60)

    def renderintro(self):
        self.screen.fill(WHITE)
        text = self.smallfont.render(
                    'Game intro. Press space to start.',
                    True, (0, 0, 0))

        # 讓 intro text 有呼吸效果
        self.intro_text_alpha = self.intro_text_alpha - 4 if self.intro_text_alpha > -255 else 255
        text.set_alpha(abs(self.intro_text_alpha))

        # 計算文字位置，水平置中、垂直0.8
        text_rect = text.get_rect(center = (self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT * 0.8))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def rendermenu(self):
        """
        Render the game menu.
        """

        """
        todo:
        1. 繼續遊戲
        2. 新遊戲
        3. 設定
        4. 幫助

        """
        self.screen.fill(BACKGROUND_BLUE)

        image = pygame.image.load("src/background.png")
        self.screen.blit(image, (0, 0))

        select = []

        # self.smallfont.render(text, antialias, color, background=None) -> Surface
        titleText = self.smallfont.render(
                    'You are in the Menu. Space to play. Esc exits.',
                    True, (0, 0, 0))
        self.screen.blit(titleText, (0, 0))
        displaySettingText = self.smallfont.render(
                    'Resolution:',
                    True, (0, 0, 0))
        displaySettingText2 = self.smallfont.render(
                    '1920x1080',
                    True, (0, 0, 0))
        displaySettingText3 = self.smallfont.render(
                    '1366x768',
                    True, (0, 0, 0))
        displaySettingText4 = self.smallfont.render(
                    '3840x2160',
                    True, (0, 0, 0))
        self.screen.blit(displaySettingText, (0, 40))
        self.screen.blit(displaySettingText2, (40, 80))
        self.screen.blit(displaySettingText3, (40, 120))
        self.screen.blit(displaySettingText4, (40, 160))

        pygame.display.flip()

    def renderplay(self):
        """
        Render the game play.
        """
        self.refresh()

    def renderhelp(self):
        """
        Render the help screen.
        """

        self.screen.fill(BACKGROUND_BLUE)
        somewords = self.smallfont.render(
                    'Help is here. space, escape or return. 中文字測試',
                    True, (0, 0, 0))
        self.screen.blit(somewords, (0, 0))
        pygame.display.flip()

    def renderRight(self):
        """
        角色向右移動
        """
        self.creature.move("right")
        self.refresh()

    def renderLeft(self):
        """
        角色向左移動
        """
        self.creature.move("left")
        self.refresh()

    def renderUp(self):
        """
        角色向上移動
        """
        self.creature.move("up")
        self.refresh()

    def renderDown(self):
        """
        角色向下移動
        """
        self.creature.move("down")
        self.refresh()

    def refresh(self):
        """
        刷新畫面上顯示的內容
        """
        self.screen.fill(BACKGROUND_BLUE)

        self.screen.blit(self.background_image, (0, 0))

        somewords = self.smallfont.render('You are Playing the game. F1 for help.', True, (0, 0, 0))
        self.screen.blit(somewords, (0, 0))
        self.screen.blit(self.creature.image, self.creature.rect)
        self.straws.update()
        self.straws.draw(self.screen)
        self.hearts.update()
        self.hearts.draw(self.screen)
        pygame.display.flip()

    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """

        if not os.path.isfile('config.ini'):
            resolutionWidth = 1280
            resolutionHeight = 720
            screenFlags = pygame.SCALED
            display_index = 0
            vsync = 1
            self.generateConfig()
        else:
            resolutionWidth, resolutionHeight, screenFlags, display_index, vsync = self.applyConfig()

        result = pygame.init()
        pygame.init()
        pygame.font.init()
        #pygame.display.init()
        pygame.display.set_caption('Green Sea Turtle Adventure')
        self.screen = pygame.display.set_mode((resolutionWidth, resolutionHeight),
                                                screenFlags,
                                                display = display_index,
                                                vsync = vsync)
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.smallfont = pygame.font.Font("src/jf-openhuninn-1.1.ttf", 40)
        self.isinitialized = True

    def generateConfig(self):
        config = configparser.ConfigParser(allow_no_value=True)
        config['SCREEN'] = {'RESOLUTION_WIDTH' : '1280',
                            'RESOLUTION_HEIGHT' : '720',
                            '# 將全螢幕設為TRUE可能會造成系統解析度的問題' : None,
                            '# Set fullscreen to TRUE may cause some problem on system resolution.' : None,
                            'FULLSCREEN' : 'FALSE',
                            'SCALED' : 'TRUE',
                            'NOFRAME' : 'FALSE',
                            'OPENGL' : 'FALSE',
                            'display_index' : '0',
                            '# 需要開啟OPENGL或SCALED使VSYNC有效' : None,
                            '# VSYNC only works with the OPENGL or SCALED flags set TRUE' : None,
                            'vsync' : '1'}

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def applyConfig(self):
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')

            screen = config['SCREEN']

            resolutionWidth = int(screen['resolution_width'])
            resolutionHeight = int(screen['resolution_height'])
            screenFlags = 0
            if screen.getboolean('fullscreen'):
                screenFlags = pygame.FULLSCREEN
            if screen.getboolean('scaled'):
                screenFlags = screenFlags | pygame.SCALED
            if screen.getboolean('noframe'):
                screenFlags = screenFlags | pygame.NOFRAME
            if screen.getboolean('opengl'):
                screenFlags = screenFlags | pygame.OPENGL
            display_index = int(screen['display_index'])
            vsync = int(screen['vsync'])
            return resolutionWidth, resolutionHeight, screenFlags, display_index, vsync
        except:
            self.generateConfig()
            return 1280, 720, pygame.SCALED, 0, 1
