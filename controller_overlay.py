import time
import math

import os
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"


import pygame
import pygame.gfxdraw
from pygame.locals import *

pygame.init()

width, height = 800,420
#width, height = 215,112
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
#button_radius = 13.3
button_offset = (width*3/4,height/2)
button_positions = {
    k: (v[0]*button_radius*2+button_offset[0], v[1]*button_radius*2+button_offset[1])
    for k,v in button_positions.items()
}

border_width = 4
#background_color = (255,0,255)
background_color = (0,0,0)
outline_color = (7,7,7)
button_gray = (128,128,128)
button_white = (255,255,255)

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

def bordered_circle(screen, position, radius, linewidth, linecolor, fillcolor):
        pygame.draw.circle(screen, linecolor, position, radius+linewidth)
        pygame.draw.circle(screen, fillcolor, position, radius)

def bordered_rect(screen, left, top, width, height, linewidth, linecolor, fillcolor):

    screen.fill(
        linecolor,
        pygame.Rect(
            left-linewidth,
            top-linewidth,
            width+2*linewidth, height+2*linewidth
            ),
        )

    screen.fill(color,
        pygame.Rect(left, top, width, height),
        )

def draw_stick(screen, xpos, ypos, center, radius, pip_radius,linewidth, linecolor, fillcolor, wedgecolor, pipcolor, button=False):
    angle = math.atan2(ypos, xpos)

    rad = max(abs(xpos), abs(ypos))
    if rad > 0.33:
        rad = 1
    else:
        rad = 0

    xpos = rad*math.cos(angle)
    ypos = rad*math.sin(angle)

    #background
    color = fillcolor
    if button:
        color = pipcolor
    pygame.draw.circle(screen, color, center, radius)

    #wedge
    if rad > 0:
        angle = round(4*angle/math.pi)*math.pi/4
        points = [[0,0]]

        N = 8
        for n in range(N+1):
            a = angle - math.pi/8 + (math.pi/4)*n/N
            points.append([radius*math.cos(a), radius*math.sin(a)])

        points = [[int(x+center[0]), int(y+center[1])] for x,y in points]

        pygame.gfxdraw.filled_polygon(
            screen, points, wedgecolor
            )

    #border
    pygame.draw.circle(screen, linecolor, center, radius, width = linewidth)

    #direction
    color = linecolor
    if rad > 0:
        color = pipcolor
    pygame.draw.circle(screen, color,
        (center[0]+xpos*radius,
         center[1]+ypos*radius), pip_radius)



while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()


    if False:
        for i in range(joystick.get_numbuttons()):
            print(f'b{i} {joystick.get_button(i)}')
        for i in range(joystick.get_numaxes()):
            print(f'a{i} {joystick.get_axis(i)}')
        for i in range(joystick.get_numhats()):
            print(f'h{i} {joystick.get_hat(i)}')

    dpad = joystick.get_hat(0)
    dup = dpad[1] == 1
    ddown = dpad[1] == -1
    dleft = dpad[0] == -1
    dright = dpad[0] == 1

    screen.fill(background_color)

    #buttons
    for btn, pos in button_positions.items():
        color = button_gray
        if joystick.get_button(button_map[btn]):
            color = button_colors[btn]

        bordered_circle(screen, button_positions[btn], button_radius, border_width, outline_color, color)

#### left bumper
    color = button_gray
    if joystick.get_button(button_map['lb']) > 0:
        color = button_white

    bordered_rect(screen,
            button_offset[0]-button_radius-100,
            button_offset[1]-button_radius*3-50,
            100,25, border_width,
            outline_color, color
            )

#### left trigger
    color = button_gray
    if joystick.get_axis(axis_map['lt']) > 0:
        color = button_white

    bordered_rect(screen,
            button_offset[0]-button_radius-100,
            button_offset[1]-button_radius*3-50+29,
            40,50, border_width,
            outline_color, color
            )

#### right trigger
    color = button_gray
    if joystick.get_axis(axis_map['rt']) > 0:
        color = button_white

    bordered_rect(screen,
            button_offset[0]+button_radius+50+10,
            button_offset[1]-button_radius*3-50+29,
            40,50, border_width,
            outline_color, color
            )

#### right bumper
    color = button_gray
    if joystick.get_button(button_map['rb']):
        color = button_white

    bordered_rect(screen,
            button_offset[0]+button_radius,
            button_offset[1]-button_radius*3-50,
            100,25, border_width,
            outline_color, color
            )

### dpad

    dcenter = (
        button_offset[0]-button_radius*2.5,
        button_offset[1]+button_radius*2.5,
        )
    dwidth = 20
    dheight = 15
    doffset = dheight-2

    color = button_gray
    if dleft:
        color = button_white

    bordered_rect(screen,
        dcenter[0]-doffset-dwidth,
        dcenter[1]-dheight/2,
        dwidth, dheight, border_width,
        outline_color, color
        )

    color = button_gray
    if dright:
        color = button_white

    bordered_rect(screen,
        dcenter[0]+doffset,
        dcenter[1]-dheight/2,
        dwidth, dheight, border_width,
        outline_color, color
        )

    color = button_gray
    if dup:
        color = button_white

    bordered_rect(screen,
        dcenter[0]-dheight/2,
        dcenter[1]-doffset-dwidth,
        dheight, dwidth, border_width,
        outline_color, color
        )

    color = button_gray
    if ddown:
        color = button_white

    bordered_rect(screen,
        dcenter[0]-dheight/2,
        dcenter[1]+doffset,
        dheight, dwidth, border_width,
        outline_color, color
        )



    #left stick
    xpos = joystick.get_axis(axis_map['lx'])
    ypos = joystick.get_axis(axis_map['ly'])

    if draw_stick_path:
        stick_points.append((
            int(stick_center[0] + xpos*stick_radius),
            int(stick_center[0] + ypos*stick_radius)))

    draw_stick(screen, xpos, ypos, stick_center, stick_radius, 20, border_width, (192,192,192), outline_color, (128,128,128), (255,255,255))

    if draw_stick_path:
        for x,y in stick_points:
            screen.set_at((x,y), (255,0,0))
        if len(stick_points) > 2:
            pygame.draw.lines(screen, (255,0,255), False, stick_points)
        pygame.draw.circle(screen, (255,0,255), stick_points[-1], 4)

    #right stick
    xpos = joystick.get_axis(axis_map['rx'])
    ypos = joystick.get_axis(axis_map['ry'])

    draw_stick(screen, xpos, ypos,
               (button_offset[0]+button_radius*2.5,
                button_offset[1]+button_radius*2.5),
                button_radius*3/4, 4, 1, (192,192,192), outline_color, (128,128,128), (255,255,255),
                button = joystick.get_button(button_map['r3'])>0 )

    pygame.display.update()
    time.sleep(0.05)

