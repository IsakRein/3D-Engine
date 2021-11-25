import Engine
import Game

from random import randint
import pygame
import sys
from pygame.locals import *
import math

class UI:
    def __init__(self):
        while True:
            self.startGame()
            self.game = Game.Game()
            self.game.start(self.renderer, self)
            while self.game.gameActive:
                self.game.update()

            self.gameOver()

    def startGame(self):
        self.renderer = Engine.Renderer(
            (800, 800), Engine.Vector(1500, 400, 1000), (200, 600))

        self.readHighScores()

        self.renderText("tretris", "Roboto-Light", 150, (60, 60, 60), "center", (400, 200))

        self.renderText("press enter to start", "Roboto-Light", 50,
                        (60, 60, 60), "center", (400, 325))

        self.renderText("previous high scores:", "Roboto",
                        50, (100, 100, 100), "center", (400, 450))

        for i in range(5):
            self.renderText(
                self.highScores[i][0], "Roboto-Light", 30, (100, 100, 100), "right", (375, 500+i*40))
            self.renderText("-", "Roboto-Light", 30,
                            (100, 100, 100), "center", (400, 500+i*40))
            self.renderText(str(self.highScores[i][1]), "Roboto-Light", 30, (100, 100, 100), "left", (425, 500+i*40))

        self.renderer.update()

        game_started = False
        while not game_started:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_started = True
    
    def gameOver(self):
        done = False
        name = ""

        self.readHighScores()

        while not done: 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_RETURN:
                        done = True
                    else:
                        name += event.unicode
                        if len(name) >= 5:
                            done = True
            self.renderer.clear()
            self.renderText("game over", "Roboto-Light", 100, (60, 60, 60), "center", (400, 150))
            
            if (self.highScores[4][1] < self.game.score):
                self.renderText("type your name: " + name, "Roboto",
                    50, (100, 100, 100), "center", (400, 325))
                self.renderText("score: " + str(self.game.score), "Roboto",
                    50, (100, 100, 100), "center", (400, 375))
            else:
                self.renderText("not a high score. press enter to go back.", "Roboto",
                    50, (100, 100, 100), "center", (400, 325))
                self.renderText("score: " + str(self.game.score), "Roboto",
                    50, (100, 100, 100), "center", (400, 375))

            self.renderText("previous highscores", "Roboto",
                50, (100, 100, 100), "center", (400, 500))
            for i in range(5):
                self.renderText(
                    self.highScores[i][0], "Roboto-Light", 30, (100, 100, 100), "right", (375, 550+i*40))
                self.renderText("-", "Roboto-Light", 30,
                                (100, 100, 100), "center", (400, 550+i*40))
                self.renderText(str(
                    self.highScores[i][1]), "Roboto-Light", 30, (100, 100, 100), "left", (425, 550+i*40))
            
            self.renderer.update()
        
        self.reportScore(name, self.game.score)
        self.writeHighScores()
        
    def renderText(self, message, font, size, color, align, position):
        myfont = pygame.font.SysFont(font, size)
        textsurface = myfont.render(message, True, color)
        textRect = textsurface.get_rect()
        
        if align == "center":
            textRect.center = position
        elif align == "left":
            textRect.center = position
            textRect.left = position[0]
        elif align == "right":
            textRect.center = position
            textRect.right = position[0]

        self.renderer.surface.blit(textsurface, textRect)

    def readHighScores(self):
        file = open('HighScores.txt', 'r')
        lines = file.readlines()
        self.highScores = []
        for line in lines: 
            line = line.strip()
            split_line = line.split(';')
            self.highScores.append([split_line[0], int(split_line[1])])

    def reportScore(self, name, score):
        self.highScores.append([name, score])
        self.highScores.sort(key=lambda x: x[1], reverse=True)
        self.highScores = self.highScores[:5]

    def writeHighScores(self):
        with open('HighScores.txt', 'w') as filetowrite:
            for i in range(5):
                filetowrite.write(
                    self.highScores[i][0] + ";" + str(self.highScores[i][1]) + "\n")

def main():
    ui = UI()

if __name__ == '__main__':
    main()
