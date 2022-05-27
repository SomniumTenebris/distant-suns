import pygame
from pygame import gfxdraw
import math
import global_vars as gbv

#####################
# Physics Functions #
#####################

def gravity(obj, planet):
    G = 10 #gravitational Constant
    delta_y = (planet.center[1]-obj.pos[1])
    delta_x = (planet.center[0]-obj.pos[0])
    
    distance = math.sqrt(delta_x**2 + delta_y**2)

    gravity = pygame.math.Vector2(delta_x, delta_y).normalize()
    gravity = gravity * G * planet.mass / distance**2#Condense eq?
    
    obj.velocity[0] += gravity.x #Minus because gravity pulls, not pushes
    obj.velocity[1] += gravity.y

def bounce(entity, entity1):
    ########
    # Note #
    ########
    # When I added mass, the ship sometimes glitches into the various asteroids when stationary. Maybe due to 0-magnitude component vectors? I don't know


    p1, p2 = pygame.math.Vector2(entity.pos[0], entity.pos[1]), pygame.math.Vector2(entity1.pos[0], entity1.pos[1])
    nv1, nv2 = p1 - p2, p2 - p1# Normal, positional vector
    
    v1, v2 = pygame.math.Vector2(entity.velocity[0], entity.velocity[1]), pygame.math.Vector2(entity1.velocity[0], entity1.velocity[1])
    vv1 = v1 - v2# Velocity vector
    vv2 = v2 - v1

    dot1, dot2 = vv1.dot(nv1), vv1.dot(nv2)

    mag = nv1.magnitude_squared() #Should be same for nv1 and nv2

    massRatio = entity.mass/entity1.mass


    vector1 = -dot1/mag * nv1 * massRatio**(-1)
    vector2 = dot2/mag * nv2 * massRatio 

    return vector1, vector2

def bounce2(entity, entity1): # Need to factor in mass
    p1 = pygame.math.Vector2(entity.pos[0], entity.pos[1])
    p2 = pygame.math.Vector2(entity1.pos[0], entity1.pos[1])
    nv1 = p1 - p2# Normal, positional vector
    nv2 = p2 - p1
    
    v1 = pygame.math.Vector2(entity.velocity[0], entity.velocity[1])
    v2 = pygame.math.Vector2(entity1.velocity[0], entity1.velocity[1])
    vv1 = v1 - v2# Velocity vector
    vv2 = v2 - v1

    dot1 = vv1.dot(nv1)
    dot2 = vv1.dot(nv2)#vv1 or vv2? If I have errors, I shuold look here

    mag = nv1.magnitude_squared() #Should be same for nv1 and nv2

    massRatio = entity.mass/entity1.mass

    vector1 = -dot1/mag * nv1 * massRatio**(-1)
    vector2 = dot2/mag * nv2 * massRatio 

    
    return vector1, vector2

##################
# Math Functions #
##################

def bound(angle):
    if angle < 0:
        angle += 360
    if angle >= 360:
        angle -= 360
    return angle

def angleBound(angle1, angle2, error): #angle1 is the test angle, angle 2 is tested against. Maybe not just angle
    if angle1 + error >= angle2 and angle1 - error <= angle2:
        return True
    else:
        return False

def trig(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]

    angle = math.atan2(dy, dx)
    distance = math.hypot(dx, dy)

    return angle, distance

def trig2(point1, point2):#Improved? I think so
    '''def get_type(variable): #Mybe universalization and optimization
        typ = type(variable)
        if typ == list:
            return typ'''
        
    delta_x = point1[0] - point2[0]
    delta_y = point1[1] - point2[1]

    distance = math.sqrt((delta_x)**2+(delta_y)**2)

    angle = math.atan2(delta_x, delta_y)

    if delta_x < 0:
        angle = (math.radians(360) + angle)

    return delta_x, delta_y, distance, angle

def trig3(e1, e2):
    dx = e2.pos[0] - e1.pos[0]
    dy = e2.pos[1] - e1.pos[1]
    angle = math.atan2(dy, dx)
    distance = math.hypot(dx, dy)

    return dx, dy, angle, distance

def scalar_proj(v1, v2): #Where v1 is the object vector and v2 is a position vector
    dot = v1.dot(v2)
    mag = v2.magnitude()
    final = dot/mag
    return final

def vel_update(entity, v): #Where v is a vector
    entity.velocity[0] += v.x
    entity.velocity[1] += v.y

###############
# Pathfinding #
###############

def orientation(p1, p2, p3):
	# to find the orientation of
	# an ordered triplet (p1,p2,p3)
	# function returns the following values:
	# 0 : Collinear points
	# 1 : Clockwise points
	# 2 : Counterclockwise
	val = (float(p2[1] - p1[1]) * (p3[0] - p2[0])) - \
		(float(p2[0] - p1[0]) * (p3[1] - p2[1]))
	if (val > 0):	
		# Clockwise orientation
		return 1
	elif (val < 0):	
		# Counterclockwise orientation
		return -1
	else:
		# Collinear orientation
		return 0



######################
# Graphics Functions #
######################

def blitRotate(sprite, g_loc):
    a, b, w, h = sprite.image.get_rect()
    g_locx, g_locy = g_loc
    
    sin_a, cos_a = math.sin(math.radians(sprite.angle)), math.cos(math.radians(sprite.angle)) 
    min_x, min_y = min([0, sin_a*h, cos_a*w, sin_a*h + cos_a*w]), max([0, sin_a*w, -cos_a*h, sin_a*w - cos_a*h])

    pivot = pygame.math.Vector2(sprite.center_x, -sprite.center_y)# calculate the translation of the pivot 
    pivot_rotate = pivot.rotate(sprite.angle)
    pivot_move   = pivot_rotate - pivot

    origin = (sprite.x - sprite.center_x + min_x - pivot_move[0] - g_locx,
              sprite.y - sprite.center_y - min_y + pivot_move[1] + g_locy)#calculate the upper left origin of the rotated image
    
    #rotated_image = pygame.transform.rotozoom(sprite.image, sprite.angle, 1)# get a rotated image
    rotated_image = pygame.transform.rotate(sprite.image, sprite.angle)

    sprite.rect = rotated_image.get_rect()
    sprite.rect.x += sprite.x - sprite.center_x + min_x - pivot_move[0] - g_locx
    sprite.rect.y += sprite.y - sprite.center_y - min_y + pivot_move[1] + g_locy

    gbv.screen.blit(rotated_image, origin)

def wrap_text(txt, color):
    # Wraps text based on the "&" operator
    textList = txt.split("&")
    rendered_text = []

    for line in textList:
        rendered_text.append(gbv.font.render(line, True, color))

    return rendered_text

def animated_arc(i, angle, arc_color, zoom):
    x, y = int(i.chart_pos[0] + i.tiny_center_x), int(i.chart_pos[1] + i.tiny_center_y)
    scale = 15

    radius = int(i.map_radius)
    radius += int(50/zoom)

    gfxdraw.arc(gbv.screen, x, y, radius + int(scale/zoom),
                0 - 2*angle, 50 - 2*angle, arc_color)
    gfxdraw.arc(gbv.screen, x, y, radius + int(scale/zoom),
                100 - 2*angle, 150 - 2*angle, arc_color)
    gfxdraw.arc(gbv.screen, x, y, radius + int(2*scale/zoom),
                0 + angle, 50 + angle, arc_color)
    gfxdraw.arc(gbv.screen, x, y, radius + int(2*scale/zoom),
                100 + angle, 250 + angle, arc_color)
    gfxdraw.arc(gbv.screen, x, y, radius + int(3*scale/zoom),
                100 + 3*angle, 150 + 3*angle, arc_color)