import math
import numpy as np

class Circle:

  render_x = 0
  render_y = 0
  render_direction = 0
  
  def __init__(
        self, 
        angle,      # in radians
        x,          # in pixels
        y,          # in pixels
        radius = 20,# in pixels
        ):
       
    self.radius = radius
    self.x = x
    self.y = y
    self.angle = angle
    self.speed = 0

    self.render_x = self.x
    self.render_y = self.y
    self.render_direction = self.angle
    
  def get_velocity_vector(self):
      vx = self.speed * math.cos(self.angle)
      vy = self.speed * math.sin(self.angle)
      velocity = np.array((vx, vy))
      return velocity
  
  def get_speed(self):
      return self.speed
  
  def update_position(self, elapsed_time):
      (vx, vy) = self.get_velocity_vector()
      self.x += vx * elapsed_time
      self.y += vy * elapsed_time

  def update(self, elapsed_time):
      self.update_position(elapsed_time)

      pos_factor = 0.6
      dir_factor = 0.85

      self.render_x = pos_factor * self.render_x + (1 - pos_factor) * self.x
      self.render_y = pos_factor * self.render_y + (1 - pos_factor) * self.y
      self.render_direction = dir_factor * self.render_direction + (1 - dir_factor) * self.angle

  def update_velocity(self, velocity):
      # calculate direction and speed based on velocity x and velocity y
      self.speed = math.sqrt(velocity[0]**2 + velocity[1]**2)
      self.angle = math.atan2(velocity[1], velocity[0])
   
  def calc_vectors(self):
      forward = np.array((self.radius * math.cos(self.render_direction),
                          self.radius * math.sin(self.render_direction)))
      
      sideward = np.array((self.radius * math.sin(self.render_direction),
                          -self.radius * math.cos(self.render_direction)))
                          
      return forward,sideward