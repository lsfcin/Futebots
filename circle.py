import math
import numpy as np

class Circle:
  def __init__(
        self, 
        radius,            # in pixels
        x,                 # in pixels
        y,                 # in pixels
        angular_direction, # in radians
        directional_speed, # in pixels per second
        angular_speed):    # in radians per second
        
    self.x = x
    self.y = y
    self.direction = angular_direction
    self.directional_speed = directional_speed
    self.angular_speed = angular_speed
    self.radius = radius
      
  def get_velocity_vector(self):
      vx = self.directional_speed * math.cos(self.direction)
      vy = self.directional_speed * math.sin(self.direction)
      velocity = np.array((vx, vy))
      return velocity
  
  def update_position(self, elapsed_time):
      (vx, vy) = self.get_velocity_vector()
      self.x += vx * elapsed_time
      self.y += vy * elapsed_time

  def updated_direction(self, elapsed_time):
      self.direction += self.angular_speed * elapsed_time
      if self.direction > 2 * math.pi:
          self.direction -= 2 * math.pi

  def update(self, elapsed_time):
      self.updated_direction(elapsed_time)
      self.update_position(elapsed_time)

  def update_velocity(self, velocity):
      # calculate direction and speed based on velocity x and velocity y
      self.directional_speed = math.sqrt(velocity[0]**2 + velocity[1]**2)
      self.direction = math.atan2(velocity[1], velocity[0])