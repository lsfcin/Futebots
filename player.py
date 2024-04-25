import math
import circle

class Player:
    def __init__(self, circle, team, acceleration, top_speed):
        self.circle = circle
        self.team = team
        self.acceleration = acceleration
        self.top_speed = top_speed
