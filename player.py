import math
import circle
import genetics

class Player:
    animation_stage = 0
    animation_direction = 1
    possession_count = 0
    has_ball = False
		
    def __init__( 
          self,
          circle,
          skin, 
          hair, 
          team, 
          genes):
        self.skin_color       = skin
        self.hair_color       = hair
        self.team             = team
        self.acceleration     = genes.get_acceleration()
        self.size             = genes.get_size()
        self.kick_strength    = genes.get_kick_strength()
        self.possession_time  = genes.get_possession_time()
        self.move_to_goal     = genes.get_move_to_goal()
        self.move_to_ball     = genes.get_move_to_ball()
        self.prefer_pass      = genes.get_prefer_pass()
        self.prefer_shoot     = genes.get_prefer_shoot()
        
        self.circle = circle
        self.circle.radius = self.size

        self.max_speed = 100
        self.angular_speed = 0.1

    def update(self, elapsed_time):
        dir_speed = self.circle.speed
        dir_speed = min(self.max_speed, dir_speed + self.acceleration * elapsed_time)
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
      if(self.possession_count < 0):
          self.possession_count += 1

    def update_direction(self, elapsed_time):
      self.circle.angle += self.angular_speed * elapsed_time
      if self.circle.angle > 2 * math.pi:
          self.circle.angle -= 2 * math.pi

    def get_animation_stage(self):
        return self.animation_stage
    
    def manage_ball(self, ball, collided, players):
      if(collided and self.possession_count == 0):
          # grab the ball
          self.has_ball = True

          # take the ball from the other players
          for p2 in players:
              if p2 != self:
                  p2.has_ball = False

      # now manage ball possession
      if(self.has_ball):

        # keep counting possession time
        self.possession_count += 1

        if(self.possession_count > self.possession_time):
            # reset possession
            self.possession_count = -30 # it will take N frames to grab the ball again
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
