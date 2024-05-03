import math
import circle
import numpy as np

# check collision between two circles
def check_collision(c1, c2, r1_factor=1.0):
    distance = math.sqrt((c2.x - c1.x) ** 2 + (c2.y - c1.y) ** 2)
    collided = distance < c1.radius * r1_factor + c2.radius
    return collided, distance

# check collision between two moving circles python
def simulate_circles_collision(c1, c2, move_c1=True, move_c2=True):    
    
    circle1_vel = c1.get_velocity_vector()
    circle2_vel = c2.get_velocity_vector()

    # if there is a collision, simulate
    collided, distance = check_collision(c1, c2)
    if collided:

        # calculate the vector that connects the two circles
        collision_v = np.array((c2.x - c1.x, c2.y - c1.y))

        # normalize the vector
        length = math.sqrt(collision_v[0] ** 2 + collision_v[1] ** 2)
        collision_v[0] /= length
        collision_v[1] /= length

        # calculate the overlap distance
        overlap = (c1.radius + c2.radius) - distance

        # use the vector to calculate the new position of the first circle
        if(move_c1): c1.x -= collision_v[0] * overlap
        if(move_c1): c1.y -= collision_v[1] * overlap

        # and the second circle
        if(move_c2): c2.x += collision_v[0] * overlap
        if(move_c2): c2.y += collision_v[1] * overlap

        # calculate the perpendicular vector and projections of the velocities
        # using code from https://scipython.com/blog/two-dimensional-collisions/

        m1, m2 = c1.radius**2, c2.radius**2
        M = m1 + m2
        r1, r2 = np.array((c1.x, c1.y)), np.array((c2.x, c2.y))
        d = np.linalg.norm(r1 - r2)**2
        v1, v2 = circle1_vel, circle2_vel
        u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
        u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
        if(move_c1): c1.update_velocity(u1)
        if(move_c2): c2.update_velocity(u2)

# test and simulate collision between a moving circle and field limits
def simulate_player_field_collision(circle, field):
    velocity = circle.get_velocity_vector()

    # check if the circle is going to collide with the left wall
    if circle.x - circle.radius < field.margin:
        circle.x = circle.radius + field.margin
        velocity[0] = -velocity[0]
    # check if the circle is going to collide with the right wall
    if circle.x + circle.radius > field.width:
        circle.x = field.width - circle.radius
        velocity[0] = -velocity[0]
    # check if the circle is going to collide with the top wall
    if circle.y - circle.radius < field.margin:
        circle.y = circle.radius + field.margin
        velocity[1] = -velocity[1]
    # check if the circle is going to collide with the bottom wall
    if circle.y + circle.radius > field.height:
        circle.y = field.height - circle.radius
        velocity[1] = -velocity[1]
    
    circle.update_velocity(velocity)

def simulate_ball_field_collision(ball, field):
    velocity = ball.get_velocity_vector()

    # check if the circle is going to collide with the top wall
    if ball.y - ball.radius < field.margin:
        ball.y = ball.radius + field.margin
        velocity[1] = -velocity[1]
  
    # check if the circle is going to collide with the bottom wall
    if ball.y + ball.radius > field.height:
        ball.y = field.height - ball.radius
        velocity[1] = -velocity[1]

    # check if the circle is going to collide with the left wall
    if ball.x - ball.radius < field.margin:        
        
        # if so, check if the circle is entering the goal
        if ball.y > field.height/2 - field.goal_size/2 and ball.y < field.height/2 + field.goal_size/2:
            simulate_circles_collision(field.postL1, ball, False)
            simulate_circles_collision(field.postL2, ball, False)

            # if the ball crossed the goal line, return results to the main loop
            if ball.x + ball.radius < field.margin:
                velocity[0] = 0
                velocity[1] = 0
        else:
          ball.x = ball.radius + field.margin
          velocity[0] = -velocity[0]
 
    # check if the circle is going to collide with the right wall
    if ball.x + ball.radius > field.width:
        
        # if so, check if the circle is entering the goal
        if ball.y > field.height/2 - field.goal_size/2 and ball.y < field.height/2 + field.goal_size/2:
            simulate_circles_collision(field.postR1, ball, False)
            simulate_circles_collision(field.postR2, ball, False)

            # if the ball crossed the goal line, return results to the main loop
            if ball.x - ball.radius > field.width:
                velocity[0] = 0
                velocity[1] = 0

        else:
          ball.x = field.width - ball.radius
          velocity[0] = -velocity[0]
    
    ball.update_velocity(velocity)

def simulate_player_players_collision(circle, players):
    for p2 in players:
        circle1 = circle
        circle2 = p2.circle
        if circle2 != circle1:
            simulate_circles_collision(circle1, circle2)            

# calculate the new speed based on the current speed and acceleration
def change_speed(current_speed, acceleration, top_speed):
    current_speed += acceleration
    if current_speed > top_speed:
        current_speed = top_speed
    return current_speed

# move player
def move_player(player, field, players, elapsed_time):

    player.update(elapsed_time)

    simulate_player_field_collision(player.circle, field)
    simulate_player_players_collision(player.circle, players)

# move ball
def move_ball(ball, field, players, elapsed_time):

    # if the ball is not with a player, move the ball
    friction = 50     # speed reduction in pixels per second
    ball.speed = max(0, ball.speed - friction * elapsed_time)
    ball.update(elapsed_time)

    simulate_ball_field_collision(ball, field)
    simulate_players_with_ball(ball, players)

def simulate_players_with_ball(ball, players):
    # if a player has the ball, move the ball with the player
    for p in players:
        collided = check_collision(ball, p.circle)[0]
        p.manage_ball(ball, collided, players)