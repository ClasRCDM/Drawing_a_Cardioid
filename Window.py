#!/usr/bin/python
# -*- coding: utf-8 -*-

from asyncio import create_task, run

from pygame import DOUBLEBUF, NOFRAME, K_ESCAPE, KEYDOWN, QUIT, display
from pygame import error as pg_error
from pygame import event as events
from pygame import font, init, quit, time

from scripts.Cardioid import Cardioid
from scripts.HUD import HUD

width, height = 1300, 680
WINDOW_SIZE = width, height


class WindowScreen:
    __slots__ = 'SCREEN', 'FPS', 'dt', 'FONT', 'cardioid', 'button', 'HUD'

    @classmethod
    def quit_game(cls) -> None:
        quit()
        exit()

    @staticmethod
    def class_name(_object) -> str:
        return _object.__class__.__name__

    def __init__(self) -> None:
        # !Init for Engine
        init()
        font.init()

        events.set_allowed((QUIT, KEYDOWN, K_ESCAPE))

        # !Screen
        flags = DOUBLEBUF | NOFRAME
        self.SCREEN = display.set_mode(WINDOW_SIZE, flags, 8)
        display.set_caption('Cardioid')

        assert 'Surface' in self.class_name(self.SCREEN)

        # !INIT!
        self.dt: float = 0.0
        run(self.init_cardioid())

    async def _fps(self):
        # !FPS
        self.FPS = time.Clock()

        assert 'Clock' in self.class_name(self.FPS)

    async def _font(self):
        # !Font
        self.FONT = font.Font('scripts/font.otf', 30)

        assert 'Font' in self.class_name(self.FONT)

    async def _hud(self):
        # * Cardioid | HUD
        self.cardioid = Cardioid(self)

        initial_colors = self.cardioid.get_colors
        self.HUD = HUD(WINDOW_SIZE, self.FONT, initial_colors)

    async def init_cardioid(self):
        __font = create_task(self._font())
        __fps = create_task(self._fps())
        __hud = create_task(self._hud())

        await __font, __fps, __hud

    def check_events(self):
        """Check events
        Check and activate the keyboard.
        """

        # !Check events keyboard
        for event in events.get():
            # !Checks the key to close the window
            try:
                if event.type in (QUIT, KEYDOWN) and event.key == K_ESCAPE:
                    self.quit_game()
            except (pg_error, AttributeError):
                self.quit_game()

            self.HUD.events(event)

        return self

    def render_fps(self) -> None:
        # * Draw text FPS
        self.SCREEN.blit(self.FONT.render(
            f'{self.FPS.get_fps() :.0f} FPS', True, 'Green', 'Black'), (35, 25))

    def draw(self):
        """Draw
        objects in the screen.
        """

        def __background():  # ! Background color
            yield self.SCREEN.fill('black')

        # * Draw lines of cardioid
        def __draw_ui():  # ! Update all screen
            self.HUD.draw(self.SCREEN, self.dt)
            self.cardioid.draw()

            yield display.update()

        def __fps_render():  # * Draw text FPS
            yield self.render_fps()

        yield from __background()
        yield from __fps_render()
        yield from __draw_ui()

    def run(self) -> None:
        """Run loop
            Main game actions
        """

        while 1:
            _ = *(self.draw()),
            self.check_events()

            # * Set the fps.
            self.dt = self.FPS.tick(0) * 0.001

            # * HUD
            (  # ?Update variables from cardioid
                self.cardioid.update_globals(self.HUD.get_activities)
                    .set_colors(self.HUD.get_colors)
            )
