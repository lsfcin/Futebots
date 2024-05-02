import math
import circle

class Player:
    animation_stage = 0
    animation_direction = 1
    hold_count = 0
    has_ball = False

    def __init__(
          self, 
          circle, 
          team, 
          skin, 
          hair, 
          accel, 
          top_speed,
          top_hold_count,
          kick_strength):
        self.circle = circle
        self.team = team
        self.skin_color = skin
        self.hair_color = hair
        self.accel = accel
        self.top_speed = top_speed
        self.top_hold_count = top_hold_count
        self.kick_strength = kick_strength

    def update(self, elapsed_time):
        dir_speed = self.circle.speed
        dir_speed = min(self.top_speed, dir_speed + self.accel * elapsed_time)
        self.circle.speed = dir_speed
        self.circle.update(elapsed_time)
        

    def update_animation_stage(self):
      animation_factor = 0.3
      self.animation_stage = self.animation_stage + animation_factor * (self.circle.speed * self.animation_direction)
      
      if self.animation_stage > 100:
          self.animation_direction = -1

      elif self.animation_stage < -100:
          self.animation_direction = 1

      # after a kick, skip some frames to enable the player to grab the ball again
      if(self.hold_count < 0):
          self.hold_count += 1

    def get_animation_stage(self):
        return self.animation_stage
    
    def manage_ball(self, ball, collided, players):
      if(collided and self.hold_count == 0):
          # grab the ball
          self.has_ball = True

          # take the ball from the other players
          for p2 in players:
              if p2 != self:
                  p2.has_ball = False

      # now manage ball possession
      if(self.has_ball):

        # keep counting possession time
        self.hold_count += 1

        if(self.hold_count > self.top_hold_count):
            # reset possession
            self.hold_count = -30 # it will take N frames to grab the ball again
            self.has_ball = False
            
            # kick the ball
            ball.angle = self.circle.angle
            ball.speed = self.kick_strength

        else:
            # move the ball with the player
            forward, sideward = self.circle.calc_vectors()
            possession_x = int(self.circle.x + forward[0] * 0.8 - sideward[0] * (self.animation_stage * 0.004))
            possession_y = int(self.circle.y + forward[1] * 0.8 - sideward[1] * (self.animation_stage * 0.004))
            ball.x = ball.x * 0.7 + possession_x * 0.3
            ball.y = ball.y * 0.7 + possession_y * 0.3
            ball.angle = self.circle.angle
            ball.speed = 0
