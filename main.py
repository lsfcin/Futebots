import cv2
import map
import time
import player
import painter
import physics
import numpy as np

# globals
map = map.Map(800, 600, 50, 250)

start = time.time()
end = time.time()
target_elapsed_time = 0.033 # 30fps

i = 50
exit = False

p1 = player.Player(200, 200, 1.6, 100, 1, 30, 0.1, 2, 0.1)
p2 = player.Player(400, 200, 1.6, 150, 2, 20, 0.1, 2, 0.1)

while not exit:
  image = painter.create_map_image(map)
  p1.direction = physics.change_direction(p1.direction, -0.01)  
  p2.direction = physics.change_direction(p2.direction, 0.02)
  physics.move_player(p1, map, target_elapsed_time)
  physics.move_player(p2, map, target_elapsed_time)
  painter.paint_player(image, p1)
  painter.paint_player(image, p2)

  # sleep to keep the desired frame rate and then show the frame
  end = time.time()
  delta = end - start
  time.sleep(target_elapsed_time - delta)
  cv2.imshow('frame', image)
  start = time.time()

  if cv2.waitKey(1) == 27: # esc keys
    exit = True