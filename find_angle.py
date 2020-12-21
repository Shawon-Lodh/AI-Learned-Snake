import math
import numpy as np

# s_pos = [580, 352]
# f_pos = [480, 300]


# def find_angle(s_pos, f_pos):
#     modVector_sPos = math.sqrt((s_pos[0] * s_pos[0]) + (s_pos[1] * s_pos[1]))
#     modVector_fPos = math.sqrt((f_pos[0] * f_pos[0]) + (f_pos[1] * f_pos[1]))
#
#     dotProduct_between_sPos_fPos = (s_pos[0] * f_pos[0]) + (s_pos[1] * f_pos[1])
#
#     cosTheta = dotProduct_between_sPos_fPos / (modVector_sPos * modVector_fPos)
#
#     # Theta value in degree
#     Theta = math.degrees(math.acos(cosTheta))
#
#     return cosTheta, Theta
#
#
# def angle_of_vectors(a, b, c, d):
#     dotProduct = a * c + b * d
#     # for three dimensional simply add dotProduct = a*c + b*d  + e*f
#     modOfVector1 = math.sqrt(a * a + b * b) * math.sqrt(c * c + d * d)
#     # for three dimensional simply add modOfVector = math.sqrt( a*a + b*b + e*e)*math.sqrt(c*c + d*d +f*f)
#     angle = dotProduct / modOfVector1
#     print("Cosθ =", angle)
#     angleInDegree = math.degrees(math.acos(angle))
#     print("θ =", angleInDegree, "°")
#
#
# def angle_with_apple(snake_position, apple_position):
#     apple_direction_vector = np.array(apple_position) - np.array(snake_position[0])
#     snake_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])
#
#     norm_of_apple_direction_vector = np.linalg.norm(apple_direction_vector)
#     norm_of_snake_direction_vector = np.linalg.norm(snake_direction_vector)
#     if norm_of_apple_direction_vector == 0:
#         norm_of_apple_direction_vector = 10
#     if norm_of_snake_direction_vector == 0:
#         norm_of_snake_direction_vector = 10
#
#     apple_direction_vector_normalized = apple_direction_vector / norm_of_apple_direction_vector
#     snake_direction_vector_normalized = snake_direction_vector / norm_of_snake_direction_vector
#     # angle = math.atan2(apple_direction_vector_normalized[1] * snake_direction_vector_normalized[0] - apple_direction_vector_normalized[0] * snake_direction_vector_normalized[1],apple_direction_vector_normalized[1] * snake_direction_vector_normalized[1] + apple_direction_vector_normalized[0] * snake_direction_vector_normalized[0]) / math.pi
#     # return angle
#
#
# # print(angle_of_vectors(580,352,480,300))
# #
# #
# #
# # print(find_angle(s_pos,f_pos))
# #
# # print(angle_with_apple(s_pos,f_pos))
#
#
# # apple_direction_vector = np.array(f_pos) - np.array(snake_position[0])
# # snake_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])
#
#
# # print(np.array(f_pos)-np.array(s_pos[0]))
#
# #spos0 means snake head
# def angle_detect(spos0,spos1, fpos):
#     if (spos0[0] == spos1[0]) and (spos0[1] != spos1[1]): #criteria up_down
#         secondary_pos = [spos0[0], fpos[1]]
#         x = spos0[1] - secondary_pos[1]
#         y = secondary_pos[0] - fpos[0]
#     else:  # criteria left_right
#         secondary_pos = [fpos[0],spos0[1]]
#         x = secondary_pos[0] - spos0[0]
#         y = fpos[1] - secondary_pos[1]
#     angle = math.degrees(math.atan(y / x))
#     return angle
#
#
# # print(angle_detect([690, 410], [690, 420], [610, 310]))
#
# print(math.degrees(math.atan(2 / 0)))

def angle_finding_helper(spos0, fpos, secondary_position_condition, angle_finding_condition):
    if secondary_position_condition == 0:  # criteria up_down
        secondary_pos = [spos0[0], fpos[1]]
        x = secondary_pos[1] - spos0[1]
        y = fpos[0] - secondary_pos[0]
    else:                                  # criteria left_right
        secondary_pos = [fpos[0], spos0[1]]
        x = secondary_pos[0] - spos0[0]
        y = fpos[1] - secondary_pos[1]
    #Find angle based on different condition

    if angle_finding_condition == 0:
        angle = math.degrees(math.atan(y / x))
    elif angle_finding_condition == 1:
        angle = math.degrees(math.atan(y / x)) - 180
    elif angle_finding_condition == 2:
        angle = math.degrees(math.atan(y / x)) + 180

    return angle


def angle_find(spos0, spos1, fpos):
    print(spos0[0],spos0[1],fpos[0],fpos[1],'\t',spos1[0],spos1[1])
    angle = 0
    #find the angle zero degree

    if (spos0[0] == spos1[0]) and (spos0[1] < spos1[1]):  # snake go to up
        if spos0[0] == fpos[0] and spos0[1]-10 == fpos[1]:
            angle = 0
    # 2
    if (spos0[0] == spos1[0]) and (spos0[1] > spos1[1]):  # snake go to down
        if spos0[0] == fpos[0] and spos0[1]+10 == fpos[1]:
            angle = 0
    # 3
    if (spos0[0] < spos1[0]) and (spos0[1] == spos1[1]):  # snake go to left
        if spos0[0]-10 == fpos[0] and spos0[1] == fpos[1]:
            angle = 0
    # 4
    if (spos0[0] > spos1[0]) and (spos0[1] == spos1[1]):  # snake go to right
        if spos0[0]+10 == fpos[0] and spos0[1] == fpos[1]:
            angle = 0


    # find the angle 90 degree
    # 1
    if (spos0[0] == spos1[0]) and (spos0[1] < spos1[1]):  # snake go to up
        if spos0[1]-10 == fpos[1]:  # food is on the same line of the snake head
            if spos0[0] > fpos[0]:  # food is on the left side of the snake head
                angle = 90
            else:  # food is on the right side of the snake head
                angle = -90
    # 2
    if (spos0[0] == spos1[0]) and (spos0[1] > spos1[1]):  # snake go to down
        if spos0[1]+10 == fpos[1]:  # food is on the same line of the snake head
            if spos0[0] < fpos[0]:  # food is on the left side of the snake head
                angle = 90
            else:  # food is on the right side of the snake head
                angle = -90

    # 3
    if (spos0[0] < spos1[0]) and (spos0[1] == spos1[1]):  # snake go to left
        if spos0[0]-10 == fpos[0]:  # food is on the same line of the snake head
            if spos0[1] > fpos[1]:  # food is on the up side of the snake head
                angle = 90
            else:  # food is on the down side of the snake head
                angle = -90

    # 4
    if (spos0[0] > spos1[0]) and (spos0[1] == spos1[1]):  # snake go to right
        if spos0[0]+10 == fpos[0]:  # food is on the same line of the snake head
            if spos0[1] > fpos[1]:  # food is on the up side of the snake head
                angle = -90
            else:  # food is on the down side of the snake head
                angle = 90

    # find the angle 180 or -180
    # 1
    if (spos0[0] == spos1[0]) and (spos0[1] < spos1[1]):  # snake go to up
        if spos0[0] == fpos[0]:  # snake body and food on the same line
            if spos0[1] > fpos[1]+10:  # food is on the front side of the snake head
                angle = 180
            else:  # food is on the totally reverse side of the snake head
                angle = -180

    # 2
    if (spos0[0] == spos1[0]) and (spos0[1] > spos1[1]):  # snake go to down
        if spos0[0] == fpos[0]:  # snake body and food on the same line
            if spos0[1] < fpos[1]-10:  # food is on the front side of the snake head
                angle = 180
            else:  # food is on the totally reverse side of the snake head
                angle = -180

    # 3
    if (spos0[0] < spos1[0]) and (spos0[1] == spos1[1]):  # snake go to left
        if spos0[1] == fpos[1]:  # snake body and food on the same line
            if spos0[0] > fpos[0]+10:  # food is on the front side of the snake head
                angle = 180
            else:  # food is on the totally reverse side of the snake head
                angle = -180

    # 4
    if (spos0[0] > spos1[0]) and (spos0[1] == spos1[1]):  # snake go to right
        if spos0[1] == fpos[1]:  # snake body and food on the same line
            if spos0[0] < fpos[0]-10:  # food is on the front side of the snake head
                angle = 180
            else:  # food is on the totally reverse side of the snake head
                angle = -180

    # find the angle between (0> or <180) and  (<0 or >-180)
    # i
    if (spos0[0] == spos1[0]) and (spos0[1] < spos1[1]):  # snake go to up
        # a -> snake go to up and food is on the same side of the snake head
        if spos0[1] > fpos[1]:  # food is on the upper side of the snake head
            #1
            if spos0[0] < fpos[0]:  #food is on upper side and right side of the snake
                angle = angle_finding_helper(spos0,fpos,0,0)
            #2
            else:  #food is on upper side and left side of the snake
                angle = angle_finding_helper(spos0,fpos,0,0)

        # b -> snake go to up and food is on the opposite side of the snake head

        else:                    # food is on the opposite side of the snake head
            #1
            if spos0[0] < fpos[0]:  #food is on opposite side and right side of the snake
                angle = angle_finding_helper(spos0,fpos,0,1)
            #2
            else:  #food is on opposite side and left side of the snake
                angle = angle_finding_helper(spos0,fpos,0,2)

    # ii
    if (spos0[0] == spos1[0]) and (spos0[1] > spos1[1]):  # snake go to down
        # a -> snake go to down and food is on the same side of the snake head
        if spos0[1] < fpos[1]:  # food is on the upper side of the snake head
            # 1
            if spos0[0] > fpos[0]:  # food is on upper side and right side of the snake
                angle = angle_finding_helper(spos0, fpos, 0, 0)
            # 2
            else:  # food is on upper side and left side of the snake
                angle = angle_finding_helper(spos0, fpos, 0, 0)

        # a -> snake go to down and food is on the opposite side of the snake head

        else:                    # food is on the opposite side of the snake head
            # 1
            if spos0[0] > fpos[0]:  # food is on the opposite side and right side of the snake
                angle = angle_finding_helper(spos0, fpos, 0, 1)
            # 2
            else:  # food is on upper side and left side of the snake
                angle = angle_finding_helper(spos0, fpos, 0, 2)


    # iii
    if (spos0[0] < spos1[0]) and (spos0[1] == spos1[1]):  # snake go to left
        # a -> snake go to left and food is on the same side of the snake head
        if spos0[0] > fpos[0]:  # food is on the left side of the snake head
            #1
            if spos0[1] > fpos[1]:  #food is on left side and upper side of the snake
                angle = angle_finding_helper(spos0,fpos,1,0)
            #2
            else:  #food is on left side and lower side of the snake
                angle = angle_finding_helper(spos0,fpos,1,0)

        # b -> snake go to left and food is on the opposide side of the snake head

        else:                    # food is on the opposite side of the snake head
            #1
            if spos0[1] > fpos[1]:  #food is on opposite side and upper side of the snake
                angle = angle_finding_helper(spos0,fpos,1,2)
            #2
            else:  #food is on opposite side and lower side of the snake
                angle = angle_finding_helper(spos0,fpos,1,1)

    # iv
    if (spos0[0] > spos1[0]) and (spos0[1] == spos1[1]):  # snake go to right
        # a -> snake go to right and food is on the same side of the snake head
        if spos0[0] < fpos[0]:  # food is on the right side of the snake head
            # 1
            if spos0[1] > fpos[1]:  #food is on right side and upper side of the snake
                angle = angle_finding_helper(spos0, fpos, 1, 0)
            # 2
            else:  #food is on right side and lower side of the snake
                angle = angle_finding_helper(spos0, fpos, 1, 0)

        # b -> snake go to right and food is on the opposide side of the snake head

        else:                    # food is on the opposite side of the snake head
            # 1
            if spos0[1] > fpos[1]:  #food is on opposite side and upper side of the snake
                angle = angle_finding_helper(spos0, fpos, 1, 1)
            # 2
            else:  #food is on opposite side and lower side of the snake
                angle = angle_finding_helper(spos0, fpos, 1, 2)

    return angle/180

#input 1,2,3
def find_blockage(spos0,spos1):
    # find left,right,front blockage
    # 1
    if (spos0[0] == spos1[0]) and (spos0[1] < spos1[1]):  # snake go to up
        #snake is running on the alongside of the left boundary
        if spos0[0]==0:
            lblock = 1
            rblock = 0
            fblock = 0
        if (spos0[0]==0) and (spos0[1] ==0):
            lblock = 1
            rblock = 0
            fblock = 1

        #snake is running on the alongside of the right boundary
        if spos0[0]==710:
            lblock = 0
            rblock = 1
            fblock = 0
        if (spos0[0] == 710) and (spos0[1] == 0):
            lblock = 0
            rblock = 1
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

    return [lblock,fblock,rblock]


def find_movement(direction,change_to):
    move = 0
    if direction == 'UP':
        if change_to == 'UP':
            move = 0
        if change_to =='LEFT':
            move = -1
        if change_to == 'RIGHT':
            move = 1
    if direction == 'DOWN':
        if change_to == 'DOWN':
            move = 0
        if change_to == 'LEFT':
            move = -1
        if change_to == 'RIGHT':
            move = 1
    if direction == 'LEFT':
        if change_to == 'LEFT':
            move = 0
        if change_to == 'UP':
            move = 1
        if change_to == 'DOWN':
            move = -1
    if direction == 'RIGHT':
        if change_to == 'RIGHT':
            move = 0
        if change_to == 'UP':
            move = -1
        if change_to == 'DOWN':
            move = 1
    return  move

print(find_movement('RIGHT','UP'))