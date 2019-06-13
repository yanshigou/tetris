import pygame
import sys
import random


block_initial_position = [20, 5]
score = [0]
times = 0
gameover = []
press = False
all_block = [
    [[0, 0], [0, -1], [0, 1], [0, 2]], [[0, 0], [0, 1], [-1, 1], [-1, 0]], [[0, 0], [0, -1], [-1, 0], [-1, 1]],
    [[0, 0], [0, 1], [-1, -1], [-1, 0]], [[0, 0], [0, 1], [1, 0], [0, -1]], [[0, 0], [1, 0], [-1, 0], [1, -1]],
    [[0, 0], [1, 0], [-1, 0], [1, 1]]
]
background = [[0 for a in range(0, 10)] for row in range(0, 22)]
background[0] = [1 for i in range(0, 10)]
select_block = list(random.choice(all_block))


def new_draw():
    for row, column in select_block:
        row += block_initial_position[0]
        column += block_initial_position[1]
        pygame.draw.rect(screen, (255, 165, 0), (column * 25, 500 - row * 25, 23, 23))
    for row in range(0, 20):
        for column in range(0, 10):
            if background[row][column]:
                pygame.draw.rect(screen, (0, 0, 255), (column * 25, 500 - row * 25, 23, 23))


def move_left_right(n):
    y_drop, x_move = block_initial_position
    x_move += n
    for row, column in select_block:
        row += y_drop
        column += x_move
        if column < 0 or column > 9 or background[row][column]:
            break
    else:
        block_initial_position.clear(), block_initial_position.extend([y_drop, x_move])


def rotate():
    rotating_position = [(-column, row) for row, column in select_block]
    for row, column in rotating_position:
        row += block_initial_position[0]
        column += block_initial_position[1]
        if column < 0 or column > 9 or background[row][column]:
            break
    else:
        select_block.clear(), select_block.extend(rotating_position)


def move_down():
    y_drop, x_move = block_initial_position
    y_drop -= 1
    for row, column in select_block:
        row += y_drop
        column += x_move
        if background[row][column] == 1:
            break
    else:
        block_initial_position.clear()
        block_initial_position.extend([y_drop, x_move])
        return
    for row, column in select_block:
        background[block_initial_position[0] + row][block_initial_position[1] + column] = 1
    complete_row = []
    for row in range(1, 21):
        if 0 not in background[row]:
            complete_row.append(row)
    complete_row.sort(reverse=True)
    for row in complete_row:
        background.pop(row)
        background.append([0 for x in range(0, 10)])
    score[0] += 100*len(complete_row)
    pygame.display.set_caption('当前得分:' + str(score[0]))
    pygame.display.update()
    select_block.clear()
    select_block.extend(list(random.choice(all_block)))
    block_initial_position.clear()
    block_initial_position.extend([20, 4])
    for row, column in select_block:
        row += block_initial_position[0]
        column += block_initial_position[1]
        if background[row][column]:
            gameover.append(1)


pygame.init()
pygame.display.set_caption('俄罗斯方块简单版')
screen = pygame.display.set_mode((250, 500))


while True:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            move_left_right(-1)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            move_left_right(1)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            rotate()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            press = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            press = False
    if press:
        times += 10
    if times >= 50:
        move_down()
        times = 0
    else:
        times += 1
    if gameover:
        sys.exit()
    new_draw()
    pygame.time.Clock().tick(200)
    pygame.display.flip()
