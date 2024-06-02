from app import App
from app_components import clear_background
from events.input import Buttons, BUTTON_TYPES

import imu
import math
import time

class Ballcage(App):
  def __init__(self):
    self.button_states = Buttons(self)

    self.ball_pos = [0, 0]
    self.ball_vel = [0, 0]
    self.last_accel = imu.acc_read()
    self.speed_factor = 4
    self.ball_r = 50

  def update(self, delta):
    if self.button_states.get(BUTTON_TYPES["CANCEL"]):
        self.button_states.clear()
        self.minimise()
    #print("delta:", delta)

    start = time.ticks_us()
    new_accel = imu.acc_read()
    #print("imu took:", time.ticks_us() - start, start)
    #accel = [new + old / 2 for new, old in zip(new_accel, self.last_accel)]
    accel = new_accel
    self.last_accel = new_accel

    self.ball_vel[0] += accel[1] * delta * 0.001
    self.ball_vel[1] += accel[0] * delta * 0.001

    new_x = self.ball_pos[0] + self.ball_vel[0] * self.speed_factor
    new_y = self.ball_pos[1] + self.ball_vel[1] * self.speed_factor

    arg = math.sqrt(new_x ** 2 + new_y ** 2)

    if arg >= 118 - self.ball_r:
        angle = math.atan2(new_y, new_x)
        new_x = (118 - self.ball_r) * math.cos(angle)
        new_y = (118 - self.ball_r) * math.sin(angle)

        self.ball_vel = [0, 0]

    self.ball_pos = [new_x, new_y]



    #print(accel, self.ball_vel, (new_x, new_y), arg)



  def draw(self, ctx):
    #clear_background(ctx)
    start = time.ticks_us()
    ctx.rgb(1,1,1).rectangle(-120,-120,240,240).fill()
    ctx.rgb(0, 0, 0).arc(self.ball_pos[0], self.ball_pos[1], self.ball_r, 0, 2 * math.pi, True).fill()
    #print("draw took:", time.ticks_us() - start, start)

__app_export__ = Ballcage
