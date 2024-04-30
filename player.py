import math
import circle

class Player:
    animation_stage = 0
    animation_direction = 1

    def __init__(self, circle, team, acceleration, top_speed):
        self.circle = circle
        self.team = team
        self.acceleration = acceleration
        self.top_speed = top_speed

    def update_animation_stage(self):
      animation_factor = 0.3
      self.animation_stage = self.animation_stage + animation_factor * (self.circle.directional_speed * self.animation_direction)
      
      if self.animation_stage > 100:
          self.animation_direction = -1

      elif self.animation_stage < -100:
          self.animation_direction = 1

    def get_animation_stage(self):
        return self.animation_stage