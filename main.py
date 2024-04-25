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
field = map.Map(800, 600, 50, 250)
p1 = player.Player(circle.Circle(100, 200, 200, 1.6,  50, -0.001 ), 1, 0.1, 2)
p2 = player.Player(circle.Circle(25, 100, 200, 1.9, 100,  0.001 ), 1, 0.1, 2)
p3 = player.Player(circle.Circle(15, 200, 100, 1.0, 100,  0.0001), 1, 0.1, 2)
p4 = player.Player(circle.Circle(30, 400, 400, 0.6, 100,  0.002 ), 2, 0.1, 2)
p5 = player.Player(circle.Circle(25, 450, 450, 0.1, 100, -0.0001), 2, 0.1, 2)
p6 = player.Player(circle.Circle(20, 400, 200, 2.6, 150,  0.0005), 2, 0.1, 2)
players = [p1, p2, p3, p4, p5, p6]

# start game loop
while not exit:

  # paint the game components
  image = painter.create_field_image(field)
  
  for p in players:
    physics.move_circle(p.circle, field, players, target_elapsed_time)
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