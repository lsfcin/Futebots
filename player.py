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
