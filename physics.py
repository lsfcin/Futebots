import math
import circle

# check collision between two moving circles python
def check_circles_collision(c1, c2):    
    
    (vx1, vy1) = c1.get_velocity_vector()
    (vx2, vy2) = c2.get_velocity_vector()

    # calculate the distance between two circles
    distance = math.sqrt((c2.x - c1.x) ** 2 + (c2.y - c1.y) ** 2)

    # check if the distance is less than the sum of the radii
    if distance < c1.radius + c2.radius:

        # calculate the vector that connects the two circles
        collision_vector = [c2.x - c1.x, c2.y - c1.y]

        # normalize the vector
        length = math.sqrt(collision_vector[0] ** 2 + collision_vector[1] ** 2)
        collision_vector[0] /= length
        collision_vector[1] /= length

        # calculate the overlap distance
        overlap = (c1.radius + c2.radius) - distance

        # use the vector to calculate the new position of the first circle
        c1.x -= collision_vector[0] * overlap
        c1.y -= collision_vector[1] * overlap

        # and the second circle
        c2.x += collision_vector[0] * overlap
        c2.y += collision_vector[1] * overlap

        # calculate the perpendicular vector
        perpendicular_vector = [collision_vector[1], -collision_vector[0]]

        # project v1 onto the vector
        dot1 = vx1 * collision_vector[0] + vy1 * collision_vector[1]

        # calculate the projection of v1 onto the collision vector
        proj1_collision = [dot1 * collision_vector[0], dot1 * collision_vector[1]]

        # calculate the projection of v1 onto the perpendicular vector
        proj1_perpendicular = [dot1 * perpendicular_vector[0], dot1 * perpendicular_vector[1]]

        # use the norm of the previous velocity vector
        norm1 = math.sqrt(vx1 ** 2 + vy1 ** 2)
        #vx1 = norm1 * -collision_vector[0]
        #vy1 = norm1 * -collision_vector[1]
        vx1 = proj1_perpendicular[0] - proj1_collision[0]
        vy1 = proj1_perpendicular[1] - proj1_collision[1]

        norm2 = math.sqrt(vx2 ** 2 + vy2 ** 2)
        vx2 = norm2 * collision_vector[0]
        vy2 = norm2 * collision_vector[1]

        # v1 = math.sqrt(vx1**2 + vy1**2)
        # v2 = math.sqrt(vx2**2 + vy2**2)
        # angle1 = math.atan2(vy1, vx1)
        # angle2 = math.atan2(vy2, vx2)
        # new_angle1 = 2 * angle - angle1
        # new_angle2 = 2 * angle - angle2
        # vx1 = v1 * math.cos(new_angle1)
        # vy1 = v1 * math.sin(new_angle1)
        # vx2 = v2 * math.cos(new_angle2)
        # vy2 = v2 * math.sin(new_angle2)

    return c1.x, c1.y, c2.x, c2.y, vx1, vy1, vx2, vy2


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
            x1, y1, x2, y2, vx1, vy1, vx2, vy2 = check_circles_collision(circle1, circle2)
            circle1.x = x1
            circle1.y = y1
            circle1.update_velocity((vx1, vy1))
            circle2.x = x2
            circle2.y = y2
            circle2.update_velocity((vx2, vy2))

# calculate vx and vy based on the direction and speed
def calculate_circle_velocity_vector(circle):
    vx = circle.speed * math.cos(circle.direction)
    vy = circle.speed * math.sin(circle.direction)
    return (vx, vy)

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