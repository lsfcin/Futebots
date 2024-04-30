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
    
    # speed = player.circle.get_speed()
    # player.animation_stage = player.animation_stage + (speed * player.animation_direction)
    
    # if player.animation_stage > 100:
    #     player.animation_direction = -1

    # elif player.animation_stage < -100:
    #     player.animation_direction = 1

    animation_offset = -20
    
    # defining colors
    body_color = (255, 255, 255)
    head_color = (255, 255, 255)
    if player.team == 1:
        body_color = (100, 100, 240)
        head_color = (50, 50, 100)
    elif player.team == 2:
        body_color = (100, 240, 100)
        head_color = (50, 100, 50)

    # defining auxiliar coordinates
    circle = player.circle
    x = int(circle.render_x)
    y = int(circle.render_y)
    
    forward = np.array((circle.radius * math.cos(circle.render_direction),
                        circle.radius * math.sin(circle.render_direction)))
    
    sideward = np.array((circle.radius * math.sin(circle.render_direction),
                        -circle.radius * math.cos(circle.render_direction)))

    degrees = circle.render_direction * 180 / math.pi

    # paint player's arms
    arm_x = int(x + forward[0] * 0.3 + sideward[0] * 0.85)
    arm_y = int(y + forward[1] * 0.3 + sideward[1] * 0.85)

    cv2.ellipse(
        image,
        (arm_x, arm_y),
        (int(circle.radius / 4), int(circle.radius / 2)),
        degrees - 90 + animation_offset,
        0, 360,
        head_color,
        -1)
    
    # draw an ellipse based on a circle and a direction
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

    # paint the player's head
    head_x = int(x + forward[0] * 0.1)
    head_y = int(y + forward[1] * 0.1)

    cv2.circle(image, (head_x, head_y), int(circle.radius / 2), head_color, -1)

    return image


def paint_ball(image, ball):

    cv2.circle(image, (int(ball.x), int(ball.y)), ball.radius, (245, 245, 245), -1)

    cv2.circle(image, (int(ball.x), int(ball.y)), ball.radius, (10, 10, 10), 2)

    return image
