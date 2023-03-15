#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from math import cos, pi, sin
from typing import Final, Self

from pygame import Color, draw, time, Surface


def calc(theta, radius: int, translate: tuple) -> tuple:
    return int(radius * cos(theta)) + translate[0], int(
        radius * sin(theta)) + translate[1]


@dataclass(slots=True)
class Cardioid:
    program: Surface = None
    type_numbers = int | float

    # * If it will be built from scratch
    anim: bool = True
    pulse: bool = True
    draw_aalines: bool = True

    # ? Size | Lines
    radius: type_numbers = 0
    num_lines: Final[int] = 0
    tuple_lines: Final[tuple] = 0

    # ? Pos 1 | 2 > Lines
    x1: type_numbers = 0
    y1: type_numbers = 0
    x2: type_numbers = 0
    y2: type_numbers = 0

    translate: tuple[float, float] = None

    color_primary: str = None
    color_secondary: str = None

    counter: type_numbers = 0
    inc: float = 0.01

    __time: int = 0
    factor: type_numbers = 0

    radius_size = 300.0, 0.001, 0
    behavior, peaks = 4, 1

    speed, max_pulse = 0.0004, 300

    def __init__(self, screen) -> None:
        self.program = screen
        assert 'WindowScreen' in self.program.class_name(self.program)

        self.anim = self.pulse = self.draw_aalines = True
        self.radius, self.num_lines = 0, 150  # ? Size | Lines
        self.tuple_lines = *(range(150)),

        self.x1 = self.y1 = 0  # ? Pos 1 | 2 > Lines
        self.x2 = self.y2 = 0  # ? Pos 1 | 2 > Lines

        self.color_primary, self.color_secondary = 'purple', 'orange'

        # * Cardioid position
        self.translate: tuple[float, float] = self.program.SCREEN.get_width() // 2 + 180, \
            self.program.SCREEN.get_height() // 2

        self.counter, self.inc = 0, 0.01

    @property
    def __get_color(self) -> Color:
        """Get color

        Defines color between multiple lines

        Returns:
            Color: line color
        """

        # ! Change color gradually
        if self.anim:
            self.counter += self.inc
            self.counter, self.inc = (
                self.counter, self.inc) if 0 < self.counter < 1 else (
                max(min(self.counter, 1), 0), -self.inc
            )

        color1, color2 = self.get_colors
        yield Color(color1).lerp(color2, self.counter)

    @property
    def get_colors(self) -> tuple[str, str]:
        return self.color_primary, self.color_secondary

    def set_colors(self, colors) -> None:
        self.color_primary, self.color_secondary = colors

    def update_globals(self, _globals: tuple[bool]) -> Self:
        self.anim, self.pulse, self.draw_aalines = _globals

        return self

    def cardioid(self, factor, num_lines, i) -> None:
        """Cardioid

        Calculated positions and behavior, Draw lines

        Args:
            factor (_type_): _description_
            num_lines (_type_): _description_
            i (_type_): _description_
        """

        # * line behavior
        theta = (self.behavior * pi / num_lines) * i

        # ! Get pos to lines
        self.x1, self.y1 = calc(theta, self.radius, self.translate)
        self.x2, self.y2 = calc(factor * theta, self.radius, self.translate)

        if self.draw_aalines:
            draw.aaline(  # * Draw line
                self.program.SCREEN, next(self.__get_color),
                (self.x2, self.y2), (self.x1, self.y1))

    def draw(self) -> None:
        if self.anim:
            # * Set to radius
            self.__time = time.get_ticks()

            if self.pulse:  # -
                self.radius = self.radius_size[0] * abs(
                    sin(self.__time * self.radius_size[1]) - self.radius_size[2])
            else:
                self.radius = self.max_pulse

            # * Number of peaks
            self.factor = self.peaks + self.speed * self.__time

        # ! Draw cardioid.
        tuple(self.cardioid(self.factor, self.num_lines, i) for i in self.tuple_lines)
