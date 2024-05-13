import time
import math

import os
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"


import pygame
import pygame.gfxdraw
from pygame.locals import *

pygame.init()

width, height = 800,420
screen = pygame.display.set_mode((width, height))

joystick = pygame.joystick.Joystick(0)

button_map = {
'a': 0,
'b': 1,
'x': 2,
'y': 3,
'rb': 5,
'lb': 4,
'select': 6,
'start': 7,
'xbox': 8,
'l3': 9,
'r3': 10,
}

axis_map = {
'lx': 0,
'ly': 1,
'lt': 2,
'rx': 3,
'ry': 4,
'rt': 5,
}

button_positions = {
'y': (0,-1),
'b': (1,0),
'x': (-1,0),
'a': (0,1),
}
button_radius = 50
button_offset = (width*3/4,height/2)
button_positions = {
    k: (v[0]*button_radius*2+button_offset[0], v[1]*button_radius*2+button_offset[1])
    for k,v in button_positions.items()
}


button_colors = {
'y': (255,255,0),
'b': (255,0,0),
'x': (0,0,255),
'a': (0,255,0),
}

stick_center = (width*1/4,height/2)
stick_radius = button_radius*3

stick_points = []

draw_stick_path = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    screen.fill((0,0,0))

#    for i in range(11):
#        print(f'{i} {joystick.get_button(i)}')
#    for i in range(6):
#        print(f'{i} {joystick.get_axis(i)}')



    #buttons
    for btn, pos in button_positions.items():
        color = (128,128,128)
        if joystick.get_button(button_map[btn]):
            color = button_colors[btn]

        pygame.draw.circle(screen, (7,7,7), button_positions[btn], button_radius+4, width = 4)

        pygame.draw.circle(screen, color, button_positions[btn], button_radius)

    #rt
    """
    color = (128,128,128)
    if joystick.get_axis(axis_map['rt']) > 0:
        color = (255,255,255)

    screen.fill(
        (7,7,7),
        pygame.Rect(
            width*3/4+button_radius-4,
            height/2-button_radius*3-50-4,
            108, 58
            ),
        )

    screen.fill(
        color,
        pygame.Rect(
            width*3/4+button_radius,
            height/2-button_radius*3-50,
            100, 50
            ),
        )
"""
####
    color = (128,128,128)
    if joystick.get_axis(axis_map['rt']) > 0:
        color = (255,255,255)

    screen.fill(
        (7,7,7),
        pygame.Rect(
            width*3/4+button_radius-4+50,
            height/2-button_radius*3-50-4+29,
            58, 58
            ),
        )

    screen.fill(
        color,
        pygame.Rect(
            width*3/4+button_radius+50,
            height/2-button_radius*3-50+29,
            50, 50
            ),
        )
####
    color = (128,128,128)
    if joystick.get_button(button_map['rb']):
        color = (255,255,255)

    screen.fill(
        (7,7,7),
        pygame.Rect(
            width*3/4+button_radius-4,
            height/2-button_radius*3-50-4,
            108, 29
            ),
        )

    screen.fill(
        color,
        pygame.Rect(
            width*3/4+button_radius,
            height/2-button_radius*3-50,
            100, 25
            ),
        )
####
    color = (128,128,128)
    if joystick.get_button(button_map['lb']) > 0:
        color = (255,255,255)

    screen.fill(
        (7,7,7),
        pygame.Rect(
            width*3/4-button_radius-100-4,
            height/2-button_radius*3-50-4,
            108, 29
            ),
        )

    screen.fill(
        color,
        pygame.Rect(
            width*3/4-button_radius-100,
            height/2-button_radius*3-50,
            100, 25
            ),
        )

    color = (128,128,128)
    if joystick.get_axis(axis_map['lt']) > 0:
        color = (255,255,255)

    screen.fill(
        (7,7,7),
        pygame.Rect(
            width*3/4-button_radius-100-4,
            height/2-button_radius*3-50-4+25+4,
            58, 58
            ),
        )

    screen.fill(
        color,
        pygame.Rect(
            width*3/4-button_radius-100,
            height/2-button_radius*3-50+25+4,
            50, 50
            ),
        )



    #lb
    """
    color = (128,128,128)
    if joystick.get_button(button_map['lb']) > 0:
        color = (255,255,255)

    screen.fill(
        (7,7,7),
        pygame.Rect(
            width*3/4-button_radius-100-4,
            height/2-button_radius*3-50-4,
            108, 58
            ),
        )

    screen.fill(
        color,
        pygame.Rect(
            width*3/4-button_radius-100,
            height/2-button_radius*3-50,
            100, 50
            ),
        )
"""

    #left stick
    xpos = joystick.get_axis(axis_map['lx'])
    ypos = joystick.get_axis(axis_map['ly'])
    angle = math.atan2(ypos, xpos)
    if draw_stick_path:
        stick_points.append((
            int(stick_center[0] + xpos*stick_radius),
            int(stick_center[0] + ypos*stick_radius)))

    rad = max(abs(xpos), abs(ypos))
    if rad > 0.33:
        rad = 1
    else:
        rad = 0

    xpos = rad*math.cos(angle)
    ypos = rad*math.sin(angle)

    #background
    color = (7,7,7)
    pygame.draw.circle(screen, color, stick_center, stick_radius)

    #wedge
    if rad > 0:
        angle = round(4*angle/math.pi)*math.pi/4
        points = [[0,0]]

        N = 8
        for n in range(N+1):
            a = angle - math.pi/8 + (math.pi/4)*n/N
            points.append([stick_radius*math.cos(a), stick_radius*math.sin(a)])

        points = [[int(x+stick_center[0]), int(y+stick_center[1])] for x,y in points]

        pygame.gfxdraw.filled_polygon(
            screen, points, (128,128,128)
            )

    #border
    color = (192,192,192)
    pygame.draw.circle(screen, color, stick_center, stick_radius, width = 4)

    #direction
    if rad > 0:
        color = (255,255,255)
    pygame.draw.circle(screen, color,
        (stick_center[0]+xpos*stick_radius,
         stick_center[1]+ypos*stick_radius), 20)

    if draw_stick_path:
        for x,y in stick_points:
            screen.set_at((x,y), (255,0,0))
        if len(stick_points) > 2:
            pygame.draw.lines(screen, (255,0,255), False, stick_points)
        pygame.draw.circle(screen, (255,0,255), stick_points[-1], 4)



    pygame.display.update()
    time.sleep(0.05)

