class Player:
  def __init__(
        self, 
        x, 
        y,
        direction,
        current_speed,
        team, 
        radius, 
        acceleration,
        top_speed,
        angular_speed,):
    self.x = x
    self.y = y
    self.direction = direction
    self.current_speed = current_speed
    self.team = team
    self.radius = radius
    self.acceleration = acceleration
    self.top_speed = top_speed
    self.angular_speed = angular_speed

      