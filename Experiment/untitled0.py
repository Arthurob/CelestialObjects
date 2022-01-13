# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 22:55:29 2021

@author: Arthur
"""

import pygame_widgets
import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

pygame.init()
win = pygame.display.set_mode((1000, 1000))

slider = Slider(win, 100, 100, 500, 40, min=0, max=99, step=1)
output = TextBox(win, 475, 200, 50, 50, fontSize=30)

output.disable()  # Act as label instead of textbox

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    win.fill((255, 255, 255))

    output.setText(slider.getValue())

    pygame_widgets.update(events)
    pygame.display.update()