import bottle
import os
import random
import pprint
import math

DEBUG = True

taunts = [
  "Don't tread on me!",
  "Full of MSG!",
  "ABCDEFG",
  "testing!"
]

last_move = None
last_move_count = 0

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json

    if (DEBUG):
        print "/start"
        pprint.pprint(data)

    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#00FF00',
        'taunt': random.choice(taunts),
        'head_url': head_url,
        'name': 'Mr Noodles'
    }

def distance_between_coords(first, second):
    return math.hypot(second[0] - first[0], second[1] - first[1])

def find_our_snake(snake_id, snakes):
    for snake in snakes:
        if snake['id'] == snake_id : return snake

def find_distance_from_walls(snake, board_height, board_width):
    snake_head_pos = snake['coords'][0]
    return {
        'north': snake_head_pos[1],
        'east': board_width - snake_head_pos[0] - 1,
        'south': board_height - snake_head_pos[1],
        'west': snake_head_pos[0],
    }

def find_nearest_safe_food(snake, snakes, food_items):
    snake_head_pos = snake['coords'][0]
    nearest_distance = None
    nearest_food_item = None
    for food_item in food_items:
        distance = distance_between_coords(snake_head_pos, food_item)
        if nearest_distance == None or nearest_distance > distance:
            nearest_distance = distance
            nearest_food_item = food_item
    return nearest_food_item

def move_to_target(source, target):
    diff = {
        'x': abs(source[0] - target[0]),
        'y': abs(source[1] - target[1]),
    }
    if diff['x'] > diff['y']:
        # move along the x axis
        if source[0] > target[0]:
            return 'left'
        else:
            return 'right'
    elif diff['y'] > diff['x']:
        # move along the y axis
        if source[1] > target[1]:
            return 'up'
        else:
            return 'down'
    else:
        # pick x or y at random
        if random.choice(['x', 'y']) == 'x':
            if source[0] > target[0]:
                return 'left'
            else:
                return 'right'
        else:
            if source[1] > target[1]:
                return 'up'
            else:
                return 'down'

@bottle.post('/move')
def move():
    data = bottle.request.json

    if (DEBUG):
        print "/move"
        pprint.pprint(data)

    board_width = data['width']
    board_height = data['height']
    food = data['food']
    you = data['you']
    snakes = data['snakes']

    directions = ['up', 'down', 'left', 'right']
    our_snake = find_our_snake(you, snakes)
    our_snake_length = len(our_snake['coords'])
    wall_distances = find_distance_from_walls(our_snake, board_height, board_width)

    valid_direction = False
    while valid_direction == False:
        chosen_direction = random.choice(directions)
        if chosen_direction == 'up':
            if wall_distances['north'] > 0:
                valid_direction = True
        elif chosen_direction == 'right':
            if wall_distances['east'] > 0:
                valid_direction = True
        elif chosen_direction == 'down':
            if wall_distances['south'] > 0:
                valid_direction = True
        else:
            if wall_distances['west'] > 0:
                valid_direction = True

    food_target = find_nearest_safe_food(our_snake, snakes, food)
    chosen_direction = move_to_target(our_snake['coords'][0], food_target)

    return {
        'move': chosen_direction,
        'taunt': random.choice(taunts),
    }
\
# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
