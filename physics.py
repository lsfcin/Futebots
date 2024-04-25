import math
import circle
import numpy as np

# check collision between two moving circles python
def simulate_circles_collision(c1, c2):    
    
    circle1_vel = c1.get_velocity_vector()
    circle2_vel = c2.get_velocity_vector()

    # calculate the distance between two circles
    distance = math.sqrt((c2.x - c1.x) ** 2 + (c2.y - c1.y) ** 2)

    # check if the distance is less than the sum of the radii
    if distance < c1.radius + c2.radius:

        # calculate the vector that connects the two circles
        collision_v = np.array((c2.x - c1.x, c2.y - c1.y))

        # normalize the vector
        length = math.sqrt(collision_v[0] ** 2 + collision_v[1] ** 2)
        collision_v[0] /= length
        collision_v[1] /= length

        # calculate the overlap distance
        overlap = (c1.radius + c2.radius) - distance

        # use the vector to calculate the new position of the first circle
        c1.x -= collision_v[0] * overlap
        c1.y -= collision_v[1] * overlap

        # and the second circle
        c2.x += collision_v[0] * overlap
        c2.y += collision_v[1] * overlap

        # calculate the perpendicular vector and projections of the velocities
        # using code from https://scipython.com/blog/two-dimensional-collisions/

        m1, m2 = c1.radius**2, c2.radius**2
        M = m1 + m2
        r1, r2 = np.array((c1.x, c1.y)), np.array((c2.x, c2.y))
        d = np.linalg.norm(r1 - r2)**2
        v1, v2 = circle1_vel, circle2_vel
        print("dot 1: ", np.dot(v1-v2, r1-r2))
        print("dot 2: ", np.dot(v1-v2, r1-r2))
        u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
        u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
        c1.update_velocity(u1)
        c2.update_velocity(u2)

# test and simulate collision between a moving circle and field limits
def simulate_field_collision(circle, field):
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

def simulate_players_collision(circle, players):
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

# move Circle
def move_circle(circle, field, players, delta_time):

    circle.update(delta_time)

    simulate_field_collision(circle, field)
    simulate_players_collision(circle, players)