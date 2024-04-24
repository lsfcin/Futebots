import cv2
import math
import numpy as np

background_grey = 170
lines_gray = (240, 240, 240)

def create_map_image(map):
  height = map.height
  width = map.width
  margin = map.margin
  goal_size = map.goal_size

  image = np.ones((height + margin, width + margin, 3), dtype="uint8") * background_grey

  # draw the football field limit lines
  cv2.rectangle(image, (margin, margin), (width, height), lines_gray, 2)

  # draw the center circle
  cv2.circle(image, 
             (int((width + margin) / 2), int((height + margin) / 2)), 
             int(height/5), 
             lines_gray, 
             2)

  # draw the center line
  cv2.line(image, 
           (int((width + margin) / 2), margin), 
           (int((width + margin) / 2), height), 
           lines_gray, 
           2)

  cv2.rectangle(image, 
                (int(margin/2), int((height + margin) / 2) - int(goal_size/2)), 
                (margin,        int((height + margin) / 2) + int(goal_size/2)), 
                lines_gray, 
                2)
  
  cv2.rectangle(image, 
                (width,                 int((height + margin) / 2) - int(goal_size/2)), 
                (width + int(margin/2), int((height + margin) / 2) + int(goal_size/2)), 
                lines_gray, 
                2)

  return image

def paint_player(image, player):
    body_color = (255, 255, 255)
    head_color = (255, 255, 255)
    if player.team == 1:
        body_color = (100, 100, 240)
        head_color = (50, 50, 100)
    elif player.team == 2:
        body_color = (100, 240, 100)
        head_color = (50, 100, 50)

    # paint the player's position
    x = int(player.x)
    y = int(player.y)

    cv2.circle(image, 
               (x, y), 
               player.radius, 
               body_color, 
               -1)

    # paint the player's direction
    direction_x = x + int(player.radius * 0.4 * math.cos(player.direction))
    direction_y = y + int(player.radius * 0.4 * math.sin(player.direction))
    
    # draw a triangle based on the player's direction
    cv2.circle(image, 
             (direction_x, direction_y),
             (int)(player.radius / 1.5),
             head_color, 
             -1)

    return image