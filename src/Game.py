from random import randint
import pygame, sys
from pygame.locals import *
import Engine 
import math
import Main

class Piece:
    def __init__(self, game, y_pos, color, outline_color, positions):
        self.game = game
        self.y_pos = y_pos
        self.color = color
        self.outline_color = outline_color
        self.cubes = []
        self.positions = positions
        self.realPositions = []
        for pos in positions:
            self.realPositions.append(Engine.Vector((pos.x*70)-70, (pos.y*30), (pos.z*70)-70))
        for realPos in self.realPositions:
            self.cubes.append(Engine.Cube(
                realPos, 0, 50, 25, color, outline_color, 3))

        self.floating = True

    def draw(self, renderer):
        for i in range(len(self.cubes)):
            self.cubes[i].position = self.realPositions[i] + \
                Engine.Vector(0, self.y_pos, 0)
            self.cubes[i].draw(renderer)

    def checkFloating(self):
        for index in range(len(self.positions)):
            pos = self.positions[index]
            realPos = self.realPositions[index]

            top = self.game.topPositions[int(pos.x)][int(pos.z)]
            bottom = realPos.y - 15 + self.y_pos

            if (bottom <= top):
                self.floating = False
                return False
        return True

    def moveDown(self):
        self.checkFloating()
        
        if self.floating:
            self.y_pos -= 5

        else:
            for index in range(len(self.positions)):
                pos = self.positions[index]
                realPos = self.realPositions[index]

                newTop = realPos.y + 15 + self.y_pos

                layer = int(((realPos.y + 15 + self.y_pos) // 30)-1)
                
                while (len(self.game.layers) < layer + 1):
                    self.game.layers.append(0)
                
                self.game.layers[layer] += 1

                if (self.game.topPositions[int(pos.x)][int(pos.z)] < newTop):
                    self.game.topPositions[int(pos.x)][int(pos.z)] = newTop
        
            for i in self.cubes:
                self.game.finishedPieces.append(i)
            # self.game.finishedPieces.append(self)
            self.game.newPiece()

    def rotate(self, degrees):
        for cube in self.cubes:
            cube.rotate(degrees)

class Game:
    def start(self, renderer, ui):
        self.renderer = renderer
        self.ui = ui

        self.platform = []
        self.topPositions = []

        self.generatePlatform()        

        self.gameActive = True
        self.layers = []

        self.available_pieces = [

            ((77, 120, 220), [
                Engine.Vector(0, 0, 0),
                Engine.Vector(0, 1, 0),
                Engine.Vector(0, 2, 0),
            ]),
            ((77, 120, 220), [
                Engine.Vector(0, 0, 0),
                Engine.Vector(0, 0, 1),
                Engine.Vector(0, 0, 2),
            ]),
            ((66, 135, 245), [
                Engine.Vector(0, 0, 0),
                Engine.Vector(0, 0, 1),
                Engine.Vector(0, 1, 1),
            ]),
            ((55, 200, 2), [
                Engine.Vector(0, 0, 0),
                Engine.Vector(0, 0, 1),
                Engine.Vector(1, 0, 0),
                Engine.Vector(1, 0, 1),
                Engine.Vector(0, 1, 0),
                Engine.Vector(0, 1, 1),
                Engine.Vector(1, 1, 0),
                Engine.Vector(1, 1, 1),
            ]),
            ((66, 245, 209), [
                Engine.Vector(0, 0, 0),
                Engine.Vector(0, 0, 1),
                Engine.Vector(0, 0, 2),
                Engine.Vector(1, 0, 2),
            ]),
            ((245, 66, 126), [
                Engine.Vector(0, 0, 0),
                Engine.Vector(0, 0, 1),
                Engine.Vector(0, 0, 2),
                Engine.Vector(0, 1, 2),
            ]),
            ((245, 66, 66), [
                Engine.Vector(1, 0, 1),
                Engine.Vector(1, 1, 1),
                Engine.Vector(1, 2, 1),
                Engine.Vector(1, 2, 2)
            ])
        ]

        self.score = 0

        self.newPiece()
        self.finishedPieces = []

    def newPiece(self):
        self.score += 1
        index = randint(0,len(self.available_pieces)-1)
        color = self.available_pieces[index][0]
        points = self.available_pieces[index][1]

        self.currentPiece = Piece(self, 500, color, (100, 100, 100), points)      

    def generatePlatform(self):
        for i in range(9):
            cube = Engine.Cube(Engine.Vector(
                ((i % 3)-1)*70, 0, ((math.floor(i/3)+1)-2)*70), 0, 50, 1, (180, 180, 180), (40, 40, 40), 0)
            bottom = Engine.Cube(Engine.Vector(
                ((i % 3)-1)*70, -150, ((math.floor(i/3)+1)-2)*70), 0, 100, 300, (200, 200, 200), (40, 40, 40), 0)
            self.platform.append(cube)
            self.platform.append(bottom)
        
        for i in range(3):
            row = []
            for j in range(3*i, (3*i)+3):
                row.append(0)
            self.topPositions.append(row)

    def update(self):
        self.renderer.clear()        
        self.currentPiece.moveDown()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.topPositions = self.rotateMatrix(
                        self.topPositions, -90)
                    for cube in self.platform:
                        cube.rotate(-90)
                    for piece in self.finishedPieces:
                        piece.rotate(-90)

                if event.key == pygame.K_RIGHT:
                    self.topPositions = self.rotateMatrix(
                        self.topPositions, 90)
                    for cube in self.platform:
                        cube.rotate(90)
                    for piece in self.finishedPieces:
                        piece.rotate(90)

                if event.key == pygame.K_SPACE:
                    #while self.currentPiece.floating
                    while self.currentPiece.checkFloating():
                        self.currentPiece.moveDown()

        self.checkCleared()
        self.checkWon()

        self.currentPiece.draw(self.renderer)
        self.ui.renderText("score", "Roboto",
            100, (100, 100, 100), "center", (600, 150))
        self.ui.renderText(str(self.score), "Roboto",
            200, (100, 100, 100), "center", (600, 300))
        self.ui.renderText("previous highscores", "Roboto",
                           50, (100, 100, 100), "center", (600, 450))
        for i in range(5):
            self.ui.renderText(
                self.ui.highScores[i][0], "Roboto-Light", 30, (100, 100, 100), "right", (575, 500+i*40))
            self.ui.renderText("-", "Roboto-Light", 30,
                               (100, 100, 100), "center", (600, 500+i*40))
            self.ui.renderText(str(
                self.ui.highScores[i][1]), "Roboto-Light", 30, (100, 100, 100), "left", (625, 500+i*40))
        self.draw()

    def draw(self):
        for piece in self.finishedPieces:
            piece.draw(self.renderer)

        for cube in self.platform:
            cube.draw(self.renderer)

        self.renderer.update()
        pygame.time.wait(15)       

    def checkCleared(self):       
        while 9 in self.layers:
            index = self.layers.index(9)
            piecesToMove = []

            i = 0
            while i < len(self.finishedPieces):
                layer_pos = int(index*30+15)
                obj = self.finishedPieces[i]
                
                if (int(obj.position.y) == layer_pos):
                    self.finishedPieces.remove(obj)
                    del obj
                else:
                    i += 1
            
            for obj in self.finishedPieces:
                layer_pos = int(index*30+15)
                if (int(obj.position.y) > layer_pos):
                    piecesToMove.append(obj)

            for i in range(len(self.topPositions)):
                for j in range(len(self.topPositions[i])):
                    self.topPositions[i][j] -= 30  

            # Animate
            for i in range(6):
                self.renderer.clear()
                for i in piecesToMove:
                    i.position -= Engine.Vector(0,5,0)
                self.draw()
            self.layers.pop(index)

    def checkWon(self):
        if len(self.layers) > 10:
            self.gameActive = False

    def rotateMatrix(self, matrix, degrees):
        newMatrix = []

        if degrees == 90:
            for i in range(len(matrix)):
                row = []
                for j in range(len(matrix[0])-1, -1, -1):
                    row.append(matrix[j][i])
                newMatrix.append(row)
        elif degrees == -90:
            for i in range(len(matrix)-1, -1, -1):
                row = []
                for j in range(len(matrix[0])):
                    row.append(matrix[j][i])
                newMatrix.append(row)


        return newMatrix
        
