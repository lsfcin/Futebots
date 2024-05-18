from enum import Enum

class Types(Enum):
  SIZE_X_ACCELERATION = 0  # -1 = max size, 1 = max acceleration
  KICK_X_POSSESSION = 1    # -1 = max kick strength, 1 = max possession time
  BALL_X_OWN_GOAL = 2      # -1 = moves always towards ball, 1 = moves always towards own goal
  PASS_X_SHOOT = 3         # -1 = always passes, 1 = always shoots

class Genes:
    min_size = 20
    max_size = 60
    min_acceleration = 20
    max_acceleration = 60
    min_kick_strength = 150
    max_kick_strength = 300
    min_possession_time = 20
    max_possession_time = 100
    min_move_to_ball = 0
    max_move_to_ball = 1
    min_move_to_goal = 0
    max_move_to_goal = 1
    min_prefer_pass = 0
    max_prefer_pass = 1
    min_prefer_shoot = 0
    max_prefer_shoot = 1

    def __init__(
          self, 
          genes):
        self.genes = list()
        self.genes.append(genes[0])
        self.genes.append(genes[1])
        self.genes.append(genes[2])
        self.genes.append(genes[3])

    # convert the value from the range -1 to 1 to the range min_value to max_value
    def convert(self, invert, value, min_value, max_value):
        # first, if invert is true, invert the value
        if invert:
            value = -value

        return int((value + 1) * (max_value - min_value) / 2 + min_value)     

    def get_acceleration(self):
        return self.convert(
            False, 
            self.genes[Types.SIZE_X_ACCELERATION.value], 
            Genes.min_acceleration, 
            Genes.max_acceleration)
    
    def get_size(self):
        return self.convert(
            True, 
            self.genes[Types.SIZE_X_ACCELERATION.value], 
            Genes.min_size, 
            Genes.max_size)
    
    def get_possession_time(self):
        return self.convert(
            False, 
            self.genes[Types.KICK_X_POSSESSION.value], 
            Genes.min_possession_time, 
            Genes.max_possession_time)
    
    def get_kick_strength(self):
        return self.convert(
            True, 
            self.genes[Types.KICK_X_POSSESSION.value], 
            Genes.min_kick_strength, 
            Genes.max_kick_strength)
    
    def get_move_to_goal(self):
        return self.convert(
            False, 
            self.genes[Types.BALL_X_OWN_GOAL.value], 
            Genes.min_move_to_goal, 
            Genes.max_move_to_goal)
    
    def get_move_to_ball(self):
        return self.convert(
            True, 
            self.genes[Types.BALL_X_OWN_GOAL.value], 
            Genes.min_move_to_ball, 
            Genes.max_move_to_ball)
    
    def get_prefer_shoot(self):
        return self.convert(
            False, 
            self.genes[Types.PASS_X_SHOOT.value], 
            Genes.min_prefer_shoot, 
            Genes.max_prefer_shoot)
    
    def get_prefer_pass(self):
        return self.convert(
            True, 
            self.genes[Types.PASS_X_SHOOT.value], 
            Genes.min_prefer_pass, 
            Genes.max_prefer_pass)