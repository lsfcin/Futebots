from enum import Enum

class GeneTypes(Enum):
  SIZE_X_ACCELERATION = 0  # -1 = max size, 1 = max acceleration
  KICK_X_POSSESSION = 1    # -1 = max kick strength, 1 = max possession time
  BALL_X_OWN_GOAL = 2      # -1 = moves always towards ball, 1 = moves always towards own goal
  PASS_X_SHOOT = 3         # -1 = always passes, 1 = always shoots

class PlayerGenes:
    def __init__(
          self, 
          genes):
        self.genes = list()
        self.genes.append(genes[0])
        self.genes.append(genes[1])
        self.genes.append(genes[2])
        self.genes.append(genes[3])