#!/usr/bin/python
# -*- coding: utf-8 -*-

from pygame import Rect, Color, Surface

from pygame_gui import UIManager

from pygame_gui.elements import UIButton
from pygame_gui.windows import UIColourPickerDialog


class ColorPicker:
    _type_cube = tuple[int, int]
    __slots__ = ('ui_manager', 'cube_pos', 'adj_pos',
                 'colour_picker_button', 'colour_picker',
                 'current_colour', 'picked_colour_surface')

    def __init__(self, screen,
                 pos: _type_cube, size: _type_cube, adj_pos: _type_cube = (70, 15),
                 name: str = 'Pick', color: str = 'black'):
        self.ui_manager = UIManager(screen, 'theme_color_picker.json')

        self.cube_pos = pos
        self.adj_pos = adj_pos

        self.colour_picker_button = self.create_button(
            name, screen, self.ui_manager, size, self.cube_pos)

        self.colour_picker = None
        self.current_colour = Color(color)

        self.picked_colour_surface = Surface(size)
        self.picked_colour_surface.fill(self.current_colour)

    @staticmethod
    def create_button(name, screen, ui_manager, cube_size, cube_pos):
        return UIButton(
            relative_rect=Rect(-screen[0]+cube_pos[0], -screen[1]+cube_pos[1], cube_size[0], cube_size[1]),
            text=name, manager=ui_manager,
            anchors={'left': 'right',
                     'right': 'right',
                     'top': 'bottom',
                     'bottom': 'bottom'}
        )

    def events(self, event):
        colour_picker = self.colour_picker_button

        match event.type:
            case 32867:
                if event.ui_element == colour_picker:
                    x, y = self.cube_pos
                    adj_x, adj_y = self.adj_pos

                    self.colour_picker = UIColourPickerDialog(
                        Rect(x+adj_x, y-adj_y, 390, 390), self.ui_manager,
                        window_title="Change Colour...",
                        initial_colour=self.current_colour
                    )
                    colour_picker.disable()
            case 32884:
                self.picked_colour_surface.fill(self.current_colour)
            case 32880:
                colour_picker.enable()
                self.colour_picker = None

        self.ui_manager.process_events(event)

    def draw(self, screen, dt):
        ui = self.ui_manager

        ui.update(dt)
        screen.blit(self.picked_colour_surface, self.cube_pos)
        ui.draw_ui(screen)
