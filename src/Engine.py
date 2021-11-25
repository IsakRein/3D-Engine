from math import degrees
from typing import Sized
import pygame, sys
from pygame import Surface, Vector2
from pygame import color
from pygame.locals import *
import math

class Renderer():
    def __init__(self, size, camera, center):
        pygame.init()
        
        self.renderObjects = []

        # Display
        self.surface = pygame.display.set_mode(size, 0, 32)
        self.surface.fill((230, 230, 230))

        # Camera
        self.camera = camera
        self.center = center
        self.light = Vector(21,-11,11)
        
    def clear(self):
        self.surface.fill((230, 230, 230))
        self.renderObjects.clear()

    def update(self):
        self.renderObjects.sort(key=lambda x: x.distance, reverse=True)
        for obj in self.renderObjects:
            obj.render()
            
        pygame.display.update()
    
    def draw_axis(self):
        axis = [
            (Vector(0, 0, 0), Vector(500, 0, 0), (255, 0, 0)),
            (Vector(0, 0, 0), Vector(0, 500, 0), (0, 255, 0)),
            (Vector(0, 0, 0), Vector(0, 0, 500), (0, 0, 255))
            ]    

        self.draw_lines(axis)

    def draw_lines(self, lines):
        for line in lines:
            start = line[0]
            end = line[1]
            if (len(line)>2): 
                color = line[2]
            else:
                color = (50, 50, 50)

            line = RenderLine(self, color, start, end, 3)
            self.renderObjects.append(line)

class RenderObject:
    def __init__(self, renderer, color):
        self.renderer = renderer
        self.color = color

class RenderLine(RenderObject):
    def __init__(self, renderer, color, point1, point2, width):
        super(RenderLine, self).__init__(renderer, color)
        self.point1 = point1
        self.point2 = point2
        self.width = width 

        average_x = (point1.x + point2.x) / 2 
        average_y = (point1.y + point2.y) / 2 
        average_z = (point1.z + point2.z) / 2 
        
        self.distance = math.sqrt(
                (renderer.camera.x - average_x)**2 +
                (renderer.camera.y - average_y)**2 +
                (renderer.camera.z - average_z)**2)

    
    def render(self):
        a = self.renderer.camera.x
        b = self.renderer.camera.y
        c = self.renderer.camera.z
        d = a**2 + b**2 + c**2
        intersection_y = d/b

        base_y = (Vector(0, intersection_y, 0) - self.renderer.camera)/(intersection_y-self.renderer.camera.y)
        base_x = Vector(1, 0, (-self.renderer.camera.x)/self.renderer.camera.z)

        projection_camera_start = project(self.point1, self.renderer.camera)
        projection_start = self.point1 - projection_camera_start

        result_vector = self.point2-self.point1

        projection_camera_normal = project(result_vector, self.renderer.camera)
        projection_end = result_vector - projection_camera_normal

        start = defineWithBases(projection_start, base_x, base_y)
        end = defineWithBases(projection_end, base_x, base_y)

        start_pos = (start[0] + self.renderer.center[0], start[1] + self.renderer.center[1])
        end_pos = (start_pos[0] + end[0], start_pos[1] + end[1])

        pygame.draw.line(self.renderer.surface, self.color, start_pos, end_pos, self.width)

class RenderPolygon(RenderObject):
    def __init__(self, renderer, color, points, outline_color, outline_width):
        super(RenderPolygon, self).__init__(renderer, color)
        self.points = points

        self.average_x, self.average_y, self.average_z = 0, 0, 0

        for i in points:
            self.average_x += i.x
            self.average_y += i.y
            self.average_z += i.z     

        self.average_x /= len(points)   
        self.average_y /= len(points)   
        self.average_z /= len(points)   

        self.distance = math.sqrt(
            (self.renderer.camera.x - self.average_x)**2 + 
            (self.renderer.camera.y - self.average_y)**2 +
            (self.renderer.camera.z - self.average_z)**2)

        self.outline_color = outline_color
        self.outline_width = outline_width


    def render(self):
        a = self.renderer.camera.x
        b = self.renderer.camera.y
        c = self.renderer.camera.z
        d = a**2 + b**2 + c**2
        intersection_y = d/b

        base_y = (Vector(0, intersection_y, 0) - self.renderer.camera)/(intersection_y-self.renderer.camera.y)
        base_x = Vector(1, 0, (-self.renderer.camera.x)/self.renderer.camera.z)

        projection_camera_start = project(self.points[0], self.renderer.camera)
        projection_start = self.points[0] - projection_camera_start
        
        start = defineWithBases(projection_start, base_x, base_y)
        point1 = start[0] + self.renderer.center[0], start[1] + self.renderer.center[1]

        points2D = [point1]

        for point in self.points[1:]:
            result_vector = point-self.points[0]
            projection_camera_normal = project(
                result_vector, self.renderer.camera)
            projection_end = result_vector - projection_camera_normal
            end = defineWithBases(projection_end, base_x, base_y)

            point2D = (point1[0] + end[0], point1[1] + end[1])
            points2D.append(point2D)

        if self.color != 0:
            pygame.draw.polygon(self.renderer.surface, self.color, points2D, 0)
        self.draw_outline()

    def draw_outline(self):
        for index in range(len(self.points)):
            line = RenderLine(self.renderer, self.outline_color, self.points[index % len(
                self.points)], self.points[(index + 1) % len(self.points)], self.outline_width)
            line.render()

class Vector:
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

    def __add__(self, other):
        if isinstance(other, tuple):
            result = (self.x + other[0], self.y + other[1])
            return result
        else:
            result = Vector(self.x + other.x, self.y + other.y, self.z + other.z)
            return result

    def __sub__(self, other):
        result = Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        return result

    def __mul__(self, other):
        result = Vector(self.x * other, self.y * other, self.z * other)
        return result

    def __truediv__(self, other):
        result = Vector(self.x / other, self.y / other, self.z / other)
        return result

    def flip_y(self):
        self.y *= -1;

    def magnitude(self):
        return math.sqrt(self.x**2+self.y**2+self.z**2)

class Cube():
    def __init__(self, position, rotation, width, height, color, outline_color, outline_width):
        self.position = position
        self.rotation = rotation
        self.target_rotation = rotation
        self.width = width
        self.height = height
        self.color = color
        self.outline_color = outline_color
        self.outline_width = outline_width

    def draw(self, renderer):
        if self.rotation != self.target_rotation:
            self.rotation += (self.target_rotation-self.rotation)/5;
            if (abs(self.rotation-self.target_rotation) < 1):
                self.rotation = self.target_rotation;
        
        vector1 = Vector(self.position.x - self.width/2,
                         self.position.y - self.height/2,
                         self.position.z - self.width/2)
        vector2 = Vector(self.position.x + self.width/2,
                         self.position.y + self.height/2,
                         self.position.z + self.width/2)


        rotated_V1 = rotateAroundY(vector1, math.radians(self.rotation))
        rotated_V2 = rotateAroundY(vector2, math.radians(self.rotation))
        
        x1 = rotated_V1.x
        y1 = rotated_V1.y
        z1 = rotated_V1.z
        x2 = rotated_V2.x
        y2 = rotated_V2.y
        z2 = rotated_V2.z

        bottom_vector2 = Vector(rotated_V2.x, rotated_V1.y, rotated_V2.z)

        middle = (bottom_vector2-rotated_V1)/2
        middle_pos = middle + rotated_V1

        x3 = (rotateAroundY(middle, math.pi/2) + middle_pos).x
        z3 = (rotateAroundY(middle, math.pi/2) + middle_pos).z
        x4 = (rotateAroundY(middle, -math.pi/2) + middle_pos).x
        z4 = (rotateAroundY(middle, -math.pi/2) + middle_pos).z

        corners = [
            Vector(x1, y1, z1),
            Vector(x3, y1, z3),
            Vector(x2, y1, z2),
            Vector(x4, y1, z4),
            Vector(x1, y2, z1),
            Vector(x3, y2, z3),
            Vector(x2, y2, z2),
            Vector(x4, y2, z4)
        ]

        sides = [
            # Top and bottom
            (corners[0], corners[1], corners[2], corners[3]),
            (corners[4], corners[5], corners[6], corners[7]),

            # Sides
            (corners[0], corners[1], corners[5], corners[4]),
            (corners[1], corners[2], corners[6], corners[5]),
            (corners[2], corners[3], corners[7], corners[6]),
            (corners[3], corners[0], corners[4], corners[7]),
        ]

        for side in sides:
            pol = RenderPolygon(renderer, self.color, side,
                                self.outline_color, self.outline_width)
            renderer.renderObjects.append(pol)

    def rotate(self, degrees):
        self.target_rotation += degrees

class Axis():
    def __init__(self):
        self.axis = [(Vector(0, 0, 0), Vector(500, 0, 0), (255, 0, 0)),
                     (Vector(0, 0, 0), Vector(0, 500, 0), (0, 255, 0)),
                     (Vector(0, 0, 0), Vector(0, 0, 500), (0, 0, 255))]

    def draw(self, renderer):
        renderer.draw_lines(self.axis)

def easeInOut(x):
    return ((math.sin(math.pi*(x-0.5)))+1)*0.5

def rotateAroundY(vector, radians):
    newX = vector.x*math.cos(radians) + vector.z*math.sin(radians)
    newZ = -vector.x * \
        math.sin(radians) + vector.z*math.cos(radians)
    
    rotatedVector = Vector(newX,vector.y,newZ)
    return rotatedVector

def project(vector1, vector2):
    dot_prod =  vector1.x*vector2.x +vector1.y*vector2.y+vector1.z*vector2.z
    
    length = vector2.x**2 + vector2.y**2 + vector2.z**2
    coef = dot_prod/length

    projection = Vector(coef*vector2.x, coef*vector2.y, coef*vector2.z)

    return projection

def planeIntersectionBetweenPoints(vector, camera, eye):
    a = camera.x
    b = camera.y
    c = camera.z
    d = a**2 + b**2 + c**2

    difference = eye - vector

    numer = d - a*vector.x - b*vector.y - c*vector.z
    denum = a * difference.x + b * difference.y + c * difference.z

    delta = numer / denum

    return vector + difference * delta

def defineWithBases(vector, baseX, baseY):
    l = vector.y / baseY.y
    k = vector.x - ((baseY * l).x/baseX.x)
    return (k, -l)
