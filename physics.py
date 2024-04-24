import math

# check collision between two moving circles python
def check_circles_collision(x1, y1, r1, x2, y2, r2, vx1, vy1, vx2, vy2):
    # calculate the distance between two circles
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    # check if the distance is less than the sum of the radii
    if distance < r1 + r2:
        # calculate the angle between the two circles
        angle = math.atan2(y2 - y1, x2 - x1)
        # calculate the overlap distance
        overlap = (r1 + r2) - distance
        # calculate the new position of the first circle
        x1 += math.cos(angle) * overlap
        y1 += math.sin(angle) * overlap
        # calculate the new position of the second circle
        x2 -= math.cos(angle) * overlap
        y2 -= math.sin(angle) * overlap
        # calculate the new velocities of the two circles
        v1 = math.sqrt(vx1 ** 2 + vy1 ** 2)
        v2 = math.sqrt(vx2 ** 2 + vy2 ** 2)
        angle1 = math.atan2(vy1, vx1)
        angle2 = math.atan2(vy2, vx2)
        new_angle1 = 2 * angle - angle1
        new_angle2 = 2 * angle - angle2
        vx1 = v1 * math.cos(new_angle1)
        vy1 = v1 * math.sin(new_angle1)
        vx2 = v2 * math.cos(new_angle2)
        vy2 = v2 * math.sin(new_angle2)
    return x1, y1, x2, y2, vx1, vy1, vx2, vy2

# check collision between a moving circle and a wall
def check_wall_collision(x, y, r, vx, vy, margin, width, height):
    # check if the circle is going to collide with the left wall
    if x - r < margin:
        x = r + margin
        vx = -vx
    # check if the circle is going to collide with the right wall
    if x + r > width:
        x = width - r
        vx = -vx
    # check if the circle is going to collide with the top wall
    if y - r < margin:
        y = r + margin
        vy = -vy
    # check if the circle is going to collide with the bottom wall
    if y + r > height:
        y = height - r
        vy = -vy
    return x, y, vx, vy

# calculate the new position of a moving circle
def move_circle(x, y, r, vx, vy, delta_time):
    x += vx * delta_time
    y += vy * delta_time
    return x, y

# calculate vx and vy based on the direction and speed
def calculate_velocity(direction, speed):
    vx = speed * math.cos(direction)
    vy = speed * math.sin(direction)
    return vx, vy

# calculate direction and speed based on vx and vy
def calculate_direction_speed(vx, vy):
    speed = math.sqrt(vx ** 2 + vy ** 2)
    direction = math.atan2(vy, vx)
    return direction, speed

# calculate the new speed based on the current speed and acceleration
def change_speed(current_speed, acceleration, top_speed):
    current_speed += acceleration
    if current_speed > top_speed:
        current_speed = top_speed
    return current_speed

# calculate the new direction based on the current direction and angular speed
def change_direction(direction, angular_speed):
    direction += angular_speed

    # normalize the direction to be between 0 and 2 * pi
    if direction > 2 * math.pi:
        direction -= 2 * math.pi

    return direction

# move Player
def move_player(player, map, delta_time):
    vx, vy = calculate_velocity(player.direction, player.current_speed)
    player.x, player.y = move_circle(
        player.x, 
        player.y, 
        player.radius, 
        vx, 
        vy, 
        delta_time)
    
    x, y, vx, vy = check_wall_collision(
        player.x, 
        player.y, 
        player.radius, 
        vx, 
        vy,
        map.margin,
        map.width, 
        map.height)
    
    player.x = x 
    player.y = y
    player.direction, player.current_speed = calculate_direction_speed(vx, vy)