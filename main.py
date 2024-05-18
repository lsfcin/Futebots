import cv2
import map
import time
import random
import circle
import player
import painter
import physics
import genetics
import numpy as np

print('Futebots! Genetic algorithms for football agents.')

# globals
start = time.time()
end = time.time()
elapsed_time = 0.033        # just initializing the variable
target_elapsed_time = 0.033 # aiming at a target realtime fps (30fps)
exit = False

# create game components
# field
field = map.Map(1000, 700, 100, 250)

# skin colors in RGB from consult to 
# https://static.vecteezy.com/system/resources/previews/006/683/568/non_2x/skin-tones-palette-by-color-codes-different-types-human-skin-flat-icon-set-vector.jpg
def rand_skin():
    skin_colors = list()
    skin_colors.append((196, 223, 255))
    skin_colors.append((168, 203, 234))
    skin_colors.append((171, 226, 247))
    skin_colors.append((100, 139, 172))
    skin_colors.append((60 , 97 , 148))
    skin_colors.append((77 , 100, 153))
    skin_colors.append((30 , 40 , 63 )) 
    return skin_colors[int(random.random()*len(skin_colors))]

# hair colors in RGB
def rand_hair():
    hair_colors = list()
    hair_colors.append((30, 40, 45))
    hair_colors.append((60, 75, 80))
    hair_colors.append((80, 75, 60))
    hair_colors.append((10, 40, 50))
    hair_colors.append((5 , 10, 15))
    return hair_colors[int(random.random()*len(hair_colors))]

# genes
def rand_genes():
    genes_list = list()
    genes_list.append(random.random()*2-1)
    genes_list.append(random.random()*2-1)
    genes_list.append(random.random()*2-1)
    genes_list.append(random.random()*2-1)
    genes = genetics.Genes(genes_list)
    return genes

# circle, skin, hair, team, genes
# angle, x, y

# SIZE_X_ACCELERATION = 0  # -1 = max size, 1 = max acceleration
# KICK_X_POSSESSION = 1    # -1 = max kick strength, 1 = max possession time
# BALL_X_OWN_GOAL = 2      # -1 = moves always towards ball, 1 = moves always towards own goal
# PASS_X_SHOOT = 3         # -1 = always passes, 1 = always shoots

# define starting positions for the players
def reset_players():
    pos = list()
    pos.append(np.array((int(field.margin/2 + field.width * 0.2), int(field.margin/2 + field.height * 0.5))))
    pos.append(np.array((int(field.margin/2 + field.width * 0.3), int(field.margin/2 + field.height * 0.2))))
    pos.append(np.array((int(field.margin/2 + field.width * 0.3), int(field.margin/2 + field.height * 0.8))))
    pos.append(np.array((int(field.margin/2 + field.width * 0.8), int(field.margin/2 + field.height * 0.5))))
    pos.append(np.array((int(field.margin/2 + field.width * 0.7), int(field.margin/2 + field.height * 0.2))))
    pos.append(np.array((int(field.margin/2 + field.width * 0.7), int(field.margin/2 + field.height * 0.8))))
    
    p1 = player.Player(circle.Circle( 0.0, pos[0][0], pos[0][1]), rand_skin(), rand_hair(), 1, rand_genes())
    p2 = player.Player(circle.Circle( 0.4, pos[1][0], pos[1][1]), rand_skin(), rand_hair(), 1, rand_genes())
    p3 = player.Player(circle.Circle(-0.4, pos[2][0], pos[2][1]), rand_skin(), rand_hair(), 1, rand_genes())
    p4 = player.Player(circle.Circle( 3.2, pos[3][0], pos[3][1]), rand_skin(), rand_hair(), 2, rand_genes())
    p5 = player.Player(circle.Circle( 2.8, pos[4][0], pos[4][1]), rand_skin(), rand_hair(), 2, rand_genes())
    p6 = player.Player(circle.Circle( 3.6, pos[5][0], pos[5][1]), rand_skin(), rand_hair(), 2, rand_genes())
    players = [p1, p2, p3, p4, p5, p6]

    return players

players = reset_players()

def reset_ball():
    return circle.Circle(0, int((field.margin + field.width)/2), int((field.margin + field.height)/2), 15)

ball = reset_ball()
scored = 0
goals1 = 0
goals2 = 0
total_time = 0
freeze_time = 0

def simulate_physics(target_elapsed_time, field, players, ball):
    for p in players:
      physics.move_player(p, field, players, target_elapsed_time)

    goal = physics.move_ball(ball, field, players, target_elapsed_time)
    return goal

def paint(players, ball, image):
    painter.paint_ball(image, ball)
    for p in players:
      painter.paint_player(image, p)
    painter.paint_score(image, goals1, goals2, field, total_time)
    cv2.imshow('Futebots! Genetic algorithms for football agents.', image)

def update_score(scored, goals1, goals2):
    if(scored != 0):
      # if a goal was scored, reset the ball and the players
      players = reset_players()
      ball = reset_ball()

      if scored == 1:
        goals1 += 1
      elif scored == -1:
        goals2 += 1
    
      scored = 0

    return goals1, goals2

# start game loop    
while not exit:

  # create the image from the field
  image = painter.create_field_image(field)

  if freeze_time == 0:
    players = reset_players()
    ball = reset_ball()

  if freeze_time >= 1:
    
    #simulate the game components
    scored = simulate_physics(target_elapsed_time, field, players, ball)
    goals1, goals2 = update_score(scored, goals1, goals2)

    # paint the game components
    paint(players, ball, image)

  freeze_time += 1

  if scored != 0:
    scored = 0
    freeze_time = -60

  # time management
  end = time.time()
  elapsed_time = end - start
  time.sleep(max(0, target_elapsed_time - elapsed_time))
  if freeze_time >= 1:
    total_time += target_elapsed_time
  start = time.time()

  # capture key press
  if cv2.waitKey(1) == 27: # esc keys
    exit = True