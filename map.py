import circle

class Map:
  def __init__(
        self, 
        width, 
        height,
        margin,
        goal_size):
    self.width = width
    self.height = height
    self.margin = margin
    self.goal_size = goal_size

    self.postL1 = circle.Circle(5, margin, int((height + margin) / 2 - goal_size/2), 0, 0)
    self.postL2 = circle.Circle(5, margin, int((height + margin) / 2 + goal_size/2), 0, 0)
    self.postR1 = circle.Circle(5, width,  int((height + margin) / 2 - goal_size/2), 0, 0)
    self.postR2 = circle.Circle(5, width,  int((height + margin) / 2 + goal_size/2), 0, 0)
    