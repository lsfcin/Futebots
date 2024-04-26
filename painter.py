import cv2
import math
import numpy as np

background_grey = 170
lines_gray = (240, 240, 240)

def create_field_image(field):
  height = field.height
  width = field.width
  margin = field.margin
  goal_size = field.goal_size

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
    circle = player.circle
    x = int(circle.render_x)
    y = int(circle.render_y)

    cv2.circle(image, 
               (x, y), 
               circle.radius, 
               body_color, 
               -1)

    # paint the player's direction
    direction_x = x + int(circle.radius * 0.5 * math.cos(circle.render_direction))
    direction_y = y + int(circle.radius * 0.5 * math.sin(circle.render_direction))
    
    # draw a triangle based on the player's direction
    cv2.circle(image, 
             (direction_x, direction_y),
             (int)(circle.radius / 3),
             head_color, 
             -1)

    return image

def paint_ball(image, ball):
   
    cv2.circle(image, 
              (int(ball.x), int(ball.y)), 
              ball.radius, 
              (245, 245, 245), 
              -1)
    
    cv2.circle(image, 
              (int(ball.x), int(ball.y)), 
              ball.radius, 
              (10, 10, 10), 
              2)

    return image