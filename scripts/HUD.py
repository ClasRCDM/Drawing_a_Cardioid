#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Final
from color_picker import ColorPicker

from pygame import Surface, image, mouse, transform


def get_part(sheet, width, height, colour, x=0) -> Surface:
    _image = Surface((width, height)).convert_alpha()
    _image.blit(sheet, (0, 0), (0, x, width, height))
    _image.set_colorkey(colour)

    return _image


class Sprite:
    _scale_type = int | float
    _pos_type = int

    __slots__ = 'image', 'rect', 'x', 'y', 'scale', 'path_img'

    @staticmethod
    def get_wh(img) -> tuple:
        return img.get_width(), img.get_height()

    def __init__(self, img, x: _pos_type, y: _pos_type, scale: _scale_type) -> None:
        self.rect = None
        self.scale: int | float = scale

        self.path_img = image.load(img).convert_alpha()
        self.image = self.create(self.path_img, (x, y))

    def scale_sprite(self, _img, wh):
        return transform.scale(
            _img, (self._pos_type(wh[0] * self.scale), self._pos_type(wh[1] * self.scale)))

    def set_image(self, img, __return: bool = True):
        if __return:
            return self.scale_sprite(img, (self.get_wh(img)))

        self.image = self.scale_sprite(img, (self.get_wh(img)))

    def create(self, img, pos):
        __img = self.set_image(img)
        self.set_rect(pos, __img)

        return __img

    def set_rect(self, pos, _img=None):
        get_rect = lambda img: img.get_rect()

        if _img is None: self.rect = get_rect(self.image)
        else: self.rect = get_rect(_img)

        self.rect.topleft = pos[0], pos[1]

        assert 'Rect' in class_name(self.rect)

    def draw(self, surface) -> None:
        # Draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))


class TextBox(Sprite):
    _img = 'sprites/box_text.png'

    def __init__(self, pos, scale):
        super().__init__(self._img, pos[0], pos[1], scale)


class Button(Sprite):
    _img = 'sprites/check_buttons.png'
    __slots__ = 'clicked'

    def __init__(self, x: int, y: int, scale: float | int) -> None:
        super().__init__(self._img, x, y, scale)
        self.clicked = False

    def check_clicked(self) -> bool:
        action = False

        # Get mouse position
        pos = mouse.get_pos()

        # Check mouseover and clicked conditions
        mouse_pressed = mouse.get_pressed()[0]
        if self.rect.collidepoint(pos):
            if mouse_pressed == 1 and not self.clicked:
                self.clicked = action = True

        if mouse_pressed == 0:
            self.clicked = False

        return action


class CheckButton(Button):
    __slots__ = 'button', 'activated', 'text_box', 'txt_box', 'text'

    def __init__(self, pos: tuple[int, int],
                 scale: float | int, txt_box: bool,
                 txt: tuple = None) -> None:

        super().__init__(pos[0], pos[1], scale)

        sprite_size, dimension = 18, 36
        self.button: Final[dict] = {'activated': get_part(self.path_img, sprite_size, sprite_size, (0, 0, 0)),
                                    'disabled': get_part(self.path_img, sprite_size, dimension, (0, 0, 0), sprite_size)}
        self.activated: bool = True

        self.state_button(self.activated)
        self.set_rect(pos)

        self.txt_box = txt_box
        if txt_box:
            self.text_box, self.text = self.__create_text_box(pos, scale, txt)

    @staticmethod
    def __create_text_box(pos, scale, _txt) -> tuple[TextBox, tuple]:
        adj_x, adj_y = 248, 13  # Fitting fit.
        __txt = _txt[1].render(_txt[0]['text'], True, 'white')

        return TextBox((pos[0] - adj_x, pos[1] + adj_y), scale), __txt

    def set_activated(self, activity: bool):
        self.activated = activity
        self.state_button(self.activated)

    def state_button(self, activated) -> None:
        button = self.button
        self.set_image(button['activated'] if activated else button['disabled'], False)

    @property
    def action(self) -> bool:
        if self.check_clicked():
            self.activated = True if not self.activated else False
            self.state_button(self.activated)

        return self.activated

    def draw(self, surface) -> None:
        super().draw(surface)

        if self.txt_box:
            self.text_box.draw(surface)
            adj_sptx, adj_spty = 140, 23

            surface.blit(self.text, (self.rect.x - adj_sptx, self.rect.y + adj_spty))


"""
! __________________
!        HUD
"""


class HUD:
    def __init__(self, size_screen: tuple[int, int], font, colors) -> None:
        self.FONT = font
        assert 'Font' in class_name(self.FONT)

        settings = {'mov': {'text': 'Movement', 'pos': (50, 100)},
                    'rad': {'text': 'Pulse', 'pos': (50, 170)},
                    'dra': {'text': 'Draw', 'pos': (50, 240)}}

        adj_sptx, adj_spty, scale = 140, 22, 4  # Adjust sprite framing with text | Sprite scale.
        _create_button = lambda name: CheckButton(
            (settings[name]['pos'][0] + adj_sptx,
             settings[name]['pos'][1] - adj_spty), scale, txt_box=True, txt=(settings[name], font)
        )

        # * Buttons Check!
        __button = lambda name: settings[name]['text']
        self.check_buttons = {__button((_txt := button)): _create_button(_txt)
                              for button in settings}

        # * Color Pickers!
        self.colors_pickers = {'Color_1': ColorPicker(size_screen, (60, 300), (80, 35),
                                                      name='Color 1', color=colors[0], adj_pos=(160, 15)),
                               'Color_2': ColorPicker(size_screen, (150, 300), (80, 35),
                                                      name='Color 2', color=colors[1])}

    @staticmethod
    def __create_tuple_comprehension(__object, mode, *scope):
        _comprehension = lambda _object: __object[_object]
        if mode == 'event': tuple(_comprehension(_object).events(*scope)
                                  for _object in __object)
        elif mode == 'draw': tuple(_comprehension(_object).draw(*scope)
                                   for _object in __object)

    def events(self, event) -> None:
        # --
        self.__create_tuple_comprehension(self.colors_pickers, 'event', event)

    def draw(self, screen, dt) -> None:
        __buttons = self.check_buttons
        if not __buttons['Movement'].action:
            __buttons['Pulse'].set_activated(False)

        # --
        self.__create_tuple_comprehension(__buttons, 'draw', screen)
        self.__create_tuple_comprehension(self.colors_pickers, 'draw', screen, dt)

    @property
    def get_colors(self):
        for _object in (color_picker := self.colors_pickers): yield color_picker[_object].current_colour

    @property
    def get_activities(self):
        for _object in (button := self.check_buttons): yield button[_object].action


def class_name(_object) -> str:
    return _object.__class__.__name__
