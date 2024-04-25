import math
import circle

# check collision between two moving circles python
def check_circles_collision(x1, y1, r1, x2, y2, r2, vx1, vy1, vx2, vy2):

    # calculate the distance between two circles
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # check if the distance is less than the sum of the radii
    if distance < r1 + r2:

        # calculate the vector that connects the two circles
        collision_vector = [x2 - x1, y2 - y1]

        # normalize the vector
        length = math.sqrt(collision_vector[0] ** 2 + collision_vector[1] ** 2)
        collision_vector[0] /= length
        collision_vector[1] /= length

        # calculate the overlap distance
        overlap = (r1 + r2) - distance

        # use the vector to calculate the new position of the first circle
        x1 -= collision_vector[0] * overlap
        y1 -= collision_vector[1] * overlap

        # and the second circle
        x2 += collision_vector[0] * overlap
        y2 += collision_vector[1] * overlap

        # calculate the new velocities of the two circles ...



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

    return x1, y1, x2, y2, vx1, vy1, vx2, vy2


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

    for p2 in players:
        circle1 = circle
        circle2 = p2.circle
        if circle2 != circle1:
            (vx1, vy1) = circle1.get_velocity_vector()
            (vx2, vy2) = circle2.get_velocity_vector()
            x1, y1, x2, y2, vx1, vy1, vx2, vy2 = check_circles_collision(
                circle1.x,
                circle1.y,
                circle1.radius,
                circle2.x,
                circle2.y,
                circle2.radius,
                vx1,
                vy1,
                vx2,
                vy2,
            )
            circle1.x = x1
            circle1.y = y1
            circle1.update_velocity((vx1, vy1))
            circle2.x = x2
            circle2.y = y2
            circle2.update_velocity((vx2, vy2))

