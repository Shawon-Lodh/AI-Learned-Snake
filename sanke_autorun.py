import pygame, sys, time, random, math
import numpy as np
import json
import deep_learn

model = deep_learn.main_model()

frame_size_x = 720
frame_size_y = 480

# Difficulty settings(basically frame speed )
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120

dificulty = 25

# #check for errors encountered
check_errors = pygame.init()

# check_errors ->(4,2) ->second number in tuple gives number of errors
# if second number in tuple is 0 then it means vedio display is ok
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initializing game,exiting ...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialized')

# now initialize game window

pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# colors choice in pygame(r,g,b)

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Fps(frame per second) Controller

fps_controller = pygame.time.Clock()

# game variables
# snake details

snake_pos = [100, 50]
snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]

##food details
food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
food_spawn = True

# direction details
direction = 'LEFT'
change_to = direction

# score details

score = 0


def angle_with_apple(snake_position, apple_position):
    apple_direction_vector = np.array(apple_position) - np.array(snake_position[0])
    snake_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

    norm_of_apple_direction_vector = np.linalg.norm(apple_direction_vector)
    norm_of_snake_direction_vector = np.linalg.norm(snake_direction_vector)
    if norm_of_apple_direction_vector == 0:
        norm_of_apple_direction_vector = 10
    if norm_of_snake_direction_vector == 0:
        norm_of_snake_direction_vector = 10

    apple_direction_vector_normalized = apple_direction_vector / norm_of_apple_direction_vector
    snake_direction_vector_normalized = snake_direction_vector / norm_of_snake_direction_vector
    angle = math.atan2(
        apple_direction_vector_normalized[1] * snake_direction_vector_normalized[0] - apple_direction_vector_normalized[
            0] * snake_direction_vector_normalized[1],
        apple_direction_vector_normalized[1] * snake_direction_vector_normalized[1] + apple_direction_vector_normalized[
            0] * snake_direction_vector_normalized[0]) / math.pi
    return angle


# input 1,2,3
def find_blockage(spos0, spos1):
    # find left,right,front blockage
    lblock = 0
    fblock = 0
    rblock = 0
    # 1
    if (spos0[0] == spos1[0]) and (spos0[1] < spos1[1]):  # snake go to up
        # snake is running on the alongside of the left boundary
        if spos0[0] == 0:
            lblock = 1
            rblock = 0
            fblock = 0
        if (spos0[0] == 0) and (spos0[1] == 0):
            lblock = 1
            rblock = 0
            fblock = 1

        # snake is running on the alongside of the right boundary
        if spos0[0] == 710:
            lblock = 0
            rblock = 1
            fblock = 0
        if (spos0[0] == 710) and (spos0[1] == 0):
            lblock = 0
            rblock = 1
            fblock = 1
        # snake is running middle
        if spos0[1] == 0:
            lblock = 0
            rblock = 0
            fblock = 1
    # 2
    if (spos0[0] == spos1[0]) and (spos0[1] > spos1[1]):  # snake go to down
        # snake is running on the alongside of the left boundary
        if spos0[0] == 0:
            lblock = 0
            rblock = 1
            fblock = 0
        if (spos0[0] == 0) and (spos0[1] == 470):
            lblock = 0
            rblock = 1
            fblock = 1

        # snake is running on the alongside of the right boundary
        if spos0[0] == 710:
            lblock = 1
            rblock = 0
            fblock = 0
        if (spos0[0] == 710) and (spos0[1] == 0):
            lblock = 1
            rblock = 0
            fblock = 1
        # snake is running middle
        if spos0[1] == 470:
            lblock = 0
            rblock = 0
            fblock = 1

    # 3
    if (spos0[0] < spos1[0]) and (spos0[1] == spos1[1]):  # snake go to left
        # snake is running on the alongside of the upper boundary
        if spos0[1] == 0:
            lblock = 0
            rblock = 1
            fblock = 0
        if (spos0[1] == 0) and (spos0[0] == 0):
            lblock = 0
            rblock = 1
            fblock = 1

        # snake is running on the alongside of the downside boundary
        if spos0[1] == 470:
            lblock = 1
            rblock = 0
            fblock = 0
        if (spos0[1] == 470) and (spos0[0] == 0):
            lblock = 1
            rblock = 0
            fblock = 1

        # snake is running middle
        if spos0[0] == 0:
            lblock = 0
            rblock = 0
            fblock = 1

    # 4
    if (spos0[0] > spos1[0]) and (spos0[1] == spos1[1]):  # snake go to right
        # snake is running on the alongside of the upper boundary
        if spos0[1] == 0:
            lblock = 1
            rblock = 0
            fblock = 0
        if (spos0[1] == 0) and (spos0[0] == 710):
            lblock = 1
            rblock = 0
            fblock = 1

        # snake is running on the alongside of the downside boundary
        if spos0[1] == 470:
            lblock = 0
            rblock = 1
            fblock = 0
        if (spos0[1] == 470) and (spos0[0] == 710):
            lblock = 0
            rblock = 1
            fblock = 1

        # snake is running middle
        if spos0[0] == 710:
            lblock = 0
            rblock = 0
            fblock = 1

    return lblock, fblock, rblock

def find_direction(direction, prediction):
    change_to = direction
    if direction == 'UP':
        if prediction == 0:
            change_to = 'UP'
        if prediction == 1:
            change_to = 'RIGHT'
        if prediction == -1:
            change_to = 'LEFT'

    if direction == 'DOWN':
        if prediction == 0:
            change_to = 'DOWN'
        if prediction == 1:
            change_to = 'RIGHT'
        if prediction == -1:
            change_to = 'LEFT'

    if direction == 'LEFT':
        if prediction == 0:
            change_to = 'LEFT'
        if prediction == 1:
            change_to = 'UP'
        if prediction == -1:
            change_to = 'DOWN'

    if direction == 'RIGHT':
        if prediction == 0:
            change_to = 'RIGHT'
        if prediction == 1:
            change_to = 'DOWN'
        if prediction == -1:
            change_to = 'UP'

    return change_to

# Game over
def game_over(lblk,fblk,rblk,angle,snake_condition):
    # print(lblk,fblk,rblk,angle,snake_condition)
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('You Died', True, red)
    game_over_rectangle = game_over_surface.get_rect()
    game_over_rectangle.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rectangle)
    show_score(0, red, 'times new roman', 20)
    pygame.display.flip()
    time.sleep(1)
    pygame.quit()
    sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rectangle = score_surface.get_rect()
    if choice == 1:
        score_rectangle.midtop = (frame_size_x / 10, 15)
    else:
        score_rectangle.midtop = (frame_size_x / 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rectangle)
    # pygame.display.flip()

snake_condition = 0
# snake dead -> -1 ,just alive -> 0,eat food -> 1
# main logic
while True:
    for event in pygame.event.get():
        # if anyone press cross button of window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # # W or key up -> up ; S or key down -> down ; A or key left -> left ; D or key right -> right
            # if event.key == pygame.K_UP or event.key == ord('w'):
            #     change_to = 'UP'
            # if event.key == pygame.K_DOWN or event.key == ord('s'):
            #     change_to = 'DOWN'
            # if event.key == pygame.K_LEFT or event.key == ord('a'):
            #     change_to = 'LEFT'
            # if event.key == pygame.K_RIGHT or event.key == ord('d'):
            #     change_to = 'RIGHT'

            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # print([find_blockage(snake_body[0], snake_body[1])[0], find_blockage(snake_body[0], snake_body[1])[1],
    #       find_blockage(snake_body[0], snake_body[1])[2], angle_with_apple(snake_body, food_pos),
    #       snake_condition])

    snake_condition = 0

    prediction = deep_learn.find_predicted_value(model,[find_blockage(snake_body[0], snake_body[1])[0], find_blockage(snake_body[0], snake_body[1])[1],
          find_blockage(snake_body[0], snake_body[1])[2], angle_with_apple(snake_body, food_pos),
          snake_condition])

    change_to = find_direction(direction,prediction)
    print(prediction,change_to)

    # Making sure the snake cannot move in the opposite direction instantaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        # print_condition(0)
        # snake_condition = 0
        snake_pos[1] -= 10
    if direction == 'DOWN':
        # print_condition(0)
        # snake_condition = 0
        snake_pos[1] += 10
    if direction == 'LEFT':
        # print_condition(0)
        # snake_condition = 0
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        # print_condition(0)
        # snake_condition = 0
        snake_pos[0] += 10

    # snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        snake_condition = 1  # snake is alive and get score
        # print_condition('term\n1')
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # spawing food on the screen
    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
    food_spawn = True

    # GFX
    game_window.fill(black)
    for pos in snake_body:
        # snake body
        # .draw.rect(play_surface,color,xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # snake food draw
    pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # game Over conditions
    # Touching the boundary
    if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10:
        snake_condition = -1  # snake is dead
        # print_condition('term\n-1')
        game_over(find_blockage(snake_body[0], snake_body[1])[0], find_blockage(snake_body[0], snake_body[1])[1],
          find_blockage(snake_body[0], snake_body[1])[2], angle_with_apple(snake_body, food_pos),
          snake_condition)
    if snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
        snake_condition = -1  # snake is dead
        # print_condition('term\n-1')
        game_over(find_blockage(snake_body[0], snake_body[1])[0], find_blockage(snake_body[0], snake_body[1])[1],
          find_blockage(snake_body[0], snake_body[1])[2], angle_with_apple(snake_body, food_pos),
          snake_condition)
    # Touching the snakebody
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            snake_condition = -1  # snake is dead
            # print_condition('term\n-1')
            game_over(find_blockage(snake_body[0], snake_body[1])[0], find_blockage(snake_body[0], snake_body[1])[1],
          find_blockage(snake_body[0], snake_body[1])[2], angle_with_apple(snake_body, food_pos),
          snake_condition)

    # snake is alive but not get any score
    # print(snake_body,'\t',food_pos)
    # print(snake_condition)

    show_score(1, white, 'consolas', 20)

    # print(snake_condition)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(dificulty)
