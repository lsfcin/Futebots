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

    image = (
        np.ones((height + margin, width + margin, 3), dtype="uint8") * background_grey
    )

    # draw the football field limit lines
    cv2.rectangle(image, (margin, margin), (width, height), lines_gray, 2)

    # draw the center circle
    cv2.circle(
        image,
        (int((width + margin) / 2), int((height + margin) / 2)),
        int(height / 5),
        lines_gray,
        2,
    )

    # draw the center line
    cv2.line(
        image,
        (int((width + margin) / 2), margin),
        (int((width + margin) / 2), height),
        lines_gray,
        2,
    )

    cv2.rectangle(
        image,
        (int(margin / 2), int((height + margin) / 2) - int(goal_size / 2)),
        (margin, int((height + margin) / 2) + int(goal_size / 2)),
        lines_gray,
        2,
    )

    cv2.rectangle(
        image,
        (width, int((height + margin) / 2) - int(goal_size / 2)),
        (width + int(margin / 2), int((height + margin) / 2) + int(goal_size / 2)),
        lines_gray,
        2,
    )

    return image


def paint_player(image, player):
    
    player.update_animation_stage()
    animation_stage = player.get_animation_stage()
    
    # defining colors
    body_color, skin_color, hair_color, feet_color = get_painting_colors(player)

    # defining auxiliar coordinates
    circle, x, y, forward, sideward, angle = calc_painting_vars(player)

    # paint player's feet
    paint_feet(image, animation_stage, feet_color, circle, x, y, forward, sideward, angle)

    # paint player's arms
    paint_arms(image, animation_stage, skin_color, circle, x, y, forward, sideward, angle)
    
    # paint_body
    paint_body(image, body_color, circle, x, y, angle)

    # paint the player's head
    paint_head(image, animation_stage, skin_color, hair_color, circle, x, y, forward, sideward, angle)

    return image

def get_painting_colors(player):
    body_color = (255, 255, 255)
    skin_color = player.skin_color
    hair_color = player.hair_color
    feet_color = (80, 80, 80)
    if player.team == 1:
        body_color = (100, 100, 240)
    elif player.team == 2:
        body_color = (100, 240, 100)
    return body_color,skin_color,hair_color,feet_color

def calc_painting_vars(player):
    circle = player.circle
    x = int(circle.render_x)
    y = int(circle.render_y)
    
    forward, sideward = circle.calc_vectors()

    degrees = circle.render_direction * 180 / math.pi
    return circle,x,y,forward,sideward,degrees

def paint_head(image, animation_stage, skin_color, hair_color, circle, x, y, forward, sideward, angle):

    # head
    head_x = int(x + forward[0] * 0.1 - sideward[0] * (animation_stage * 0.0005))
    head_y = int(y + forward[1] * 0.1 - sideward[1] * (animation_stage * 0.0005))
    cv2.circle(image, (head_x, head_y), int(circle.radius / 2), skin_color, -1)
    
    # hair
    hair_x = int(head_x - forward[0] * 0.045)
    hair_y = int(head_y - forward[1] * 0.045)
    cv2.ellipse(
        image, 
        (hair_x, hair_y), 
        (int(circle.radius / 2.20), 
         int(circle.radius / 2)), 
         angle + (animation_stage * 0.1), 0, 360, hair_color, -1)

def paint_body(image, body_color, circle, x, y, degrees):
    cv2.ellipse(
        image,
        (x, y),
        (int(circle.radius / 2), circle.radius),
        degrees,
        0,
        360,
        body_color,
        -1,
    )

def paint_arms(image, animation_stage, head_color, circle, x, y, forward, sideward, degrees):
    left_arm_x  = int(x + forward[0] * 0.2 + sideward[0] * (0.8 - (animation_stage * 0.0005)))
    left_arm_y  = int(y + forward[1] * 0.2 + sideward[1] * (0.8 - (animation_stage * 0.0005)))
    right_arm_x = int(x + forward[0] * 0.2 - sideward[0] * (0.8 + (animation_stage * 0.0005)))
    right_arm_y = int(y + forward[1] * 0.2 - sideward[1] * (0.8 + (animation_stage * 0.0005)))

    cv2.ellipse(
        image,
        (left_arm_x, left_arm_y),
        (int(circle.radius / 5), int(circle.radius / (2 + (max(animation_stage,0) * 0.01)))),
        degrees - 100 + (animation_stage * 0.15),
        0, 360,
        head_color,
        -1)
    
    cv2.ellipse(
        image,
        (right_arm_x, right_arm_y),
        (int(circle.radius / 5), int(circle.radius / (2 + (max(-animation_stage,0) * 0.01)))),
        degrees - 80 + (animation_stage * 0.15),
        0, 360,
        head_color,
        -1)

def paint_feet(image, animation_stage, feet_color, circle, x, y, forward, sideward, degrees):
    left_foot_x  = int(x + forward[0] * (-0.03 - (animation_stage * 0.002)) + sideward[0] * (0.3))
    left_foot_y  = int(y + forward[1] * (-0.03 - (animation_stage * 0.002)) + sideward[1] * (0.3))
    right_foot_x = int(x + forward[0] * (-0.03 + (animation_stage * 0.002)) - sideward[0] * (0.3))
    right_foot_y = int(y + forward[1] * (-0.03 + (animation_stage * 0.002)) - sideward[1] * (0.3))

    cv2.ellipse(
        image,
        (left_foot_x, left_foot_y),
        (int(circle.radius / 5), int(circle.radius / 2.5)),
        degrees - 90,
        0, 360,
        feet_color,
        -1)
    
    cv2.ellipse(
        image,
        (right_foot_x, right_foot_y),
        (int(circle.radius / 5), int(circle.radius / 2.5)),
        degrees - 90,
        0, 360,
        feet_color,
        -1)    
    
def paint_ball(image, ball):

    cv2.circle(image, (int(ball.x), int(ball.y)), ball.radius, (140, 140, 140), -1)
    cv2.circle(image, (int(ball.x-1), int(ball.y-1)), ball.radius-2, (200, 200, 200), -1)
    cv2.circle(image, (int(ball.x-2), int(ball.y-2)), ball.radius-4, (245, 245, 245), -1)

    #cv2.circle(image, (int(ball.x), int(ball.y)), ball.radius, (10, 10, 10), 2)

    return image
