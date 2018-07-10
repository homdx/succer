#!/usr/bin/python

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window

class SuccerPlayer(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class SuccerBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
spd = 30

class SuccerGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SuccerGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.player1.center_y += spd
        elif keycode[1] == 's':
            self.player1.center_y -= spd
        elif keycode[1] == 'd':
            self.player1.center_x += spd
        elif keycode[1] == 'a':
            self.player1.center_x -= spd
        elif keycode[1] == 'up':
            self.player2.center_y += spd
        elif keycode[1] == 'down':
            self.player2.center_y -= spd
        elif keycode[1] == 'right':
            self.player2.center_x += spd
        elif keycode[1] == 'left':
            self.player2.center_x -= spd
        return True

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        # went of to a side to score point?
        if self.ball.x < self.x:
            if (self.height*0.26 < self.ball.y) & (self.ball.y < self.height*0.74):
                self.player2.score += 1
                self.serve_ball(vel=(4, 0))
            else:
                self.ball.velocity_x *= -1
        if self.ball.x > self.width:
            if (self.height*0.26 < self.ball.y) & (self.ball.y < self.height*0.74):
                self.player1.score += 1
                self.serve_ball(vel=(4, 0))
            else:
                self.ball.velocity_x *= -1

    def on_touch_move(self, touch):
        if touch.x < self.width / 2.2:
            self.player1.center_y = touch.y
            self.player1.center_x = touch.x
        if touch.x > self.width - self.width / 2.2:
            self.player2.center_y = touch.y
            self.player2.center_x = touch.x


class SuccerApp(App):
    def build(self):
        game = SuccerGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    SuccerApp().run()
