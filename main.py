import cv2
import map
import time
import random
import circle
import player
import painter
import physics
import numpy as np

# globals
start = time.time()
end = time.time()
elapsed_time = 0.033        # just initializing the variable
target_elapsed_time = 0.033 # aiming at a target realtime fps (30fps)
exit = False

# create game components
# skin colors in RGB from consult to 
# https://static.vecteezy.com/system/resources/previews/006/683/568/non_2x/skin-tones-palette-by-color-codes-different-types-human-skin-flat-icon-set-vector.jpg
skin_colors = list()
skin_colors.append((196, 223, 255))
skin_colors.append((168, 203, 234))
skin_colors.append((171, 226, 247))
skin_colors.append((100, 139, 172))
skin_colors.append((60 , 97 , 148))
skin_colors.append((77 , 100, 153))
skin_colors.append((30 , 40 , 63 )) 

def sort_skin(skin_colors):
    return skin_colors[int(random.random()*len(skin_colors))]

# hair colors in RGB
hair_colors = list()
hair_colors.append((30, 40, 45))
hair_colors.append((60, 75, 80))
hair_colors.append((80, 75, 60))
hair_colors.append((10, 40, 50))
hair_colors.append((5 , 10, 15))

def sort_hair(hair_colors):
    return hair_colors[int(random.random()*len(hair_colors))]	

field = map.Map(1000, 700, 100, 250)

p1 = player.Player(circle.Circle(100, 200, 200, 1.6, -0.001 ), 1, sort_skin(skin_colors), sort_hair(hair_colors), 50,  50, 60, 350)
p2 = player.Player(circle.Circle(35,  100, 200, 1.9,  0.001 ), 1, sort_skin(skin_colors), sort_hair(hair_colors), 50, 100, 60, 350)
p3 = player.Player(circle.Circle(25,  200, 100, 1.0,  0.0001), 1, sort_skin(skin_colors), sort_hair(hair_colors), 50, 100, 60, 350)
p4 = player.Player(circle.Circle(30,  400, 400, 0.6,  0.002 ), 2, sort_skin(skin_colors), sort_hair(hair_colors), 50, 100, 60, 350)
p5 = player.Player(circle.Circle(25,  450, 450, 0.1, -0.0001), 2, sort_skin(skin_colors), sort_hair(hair_colors), 50, 100, 60, 350)
p6 = player.Player(circle.Circle(20,  400, 200, 2.6,  0.0005), 2, sort_skin(skin_colors), sort_hair(hair_colors), 50, 150, 60, 350)
players = [p1, p2, p3, p4, p5, p6]
ball = circle.Circle(15, int((field.margin + field.width)/2), int((field.margin + field.height)/2), 0, 0)

# start game loop
while not exit:

  # create the image from the field
  image = painter.create_field_image(field)
  
  #simulate the game components
  for p in players:
    physics.move_player(p, field, players, target_elapsed_time)

  physics.move_ball(ball, field, players, target_elapsed_time)
  
  # paint the game components
  painter.paint_ball(image, ball)
  for p in players:
    painter.paint_player(image, p)

  cv2.imshow('Futebots! Genetic algorithms for football agents.', image)

  # time management
  end = time.time()
  elapsed_time = end - start
  time.sleep(max(0, target_elapsed_time - elapsed_time))
  start = time.time()

  # capture key press
  if cv2.waitKey(1) == 27: # esc keys
    exit = True