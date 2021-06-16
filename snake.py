import random
import sys
import time
import pygame
from pygame.locals import *
from collections import deque

Screen_Width = 600      # 屏幕宽度
Screen_Height = 480     # 屏幕高度
Size = 20               # 小方格大小
Line_Width = 1          # 网格线宽度

# 游戏区域的坐标范围
Scope_X = (0, Screen_Width // Size)
Scope_Y = (2, Screen_Height // Size)

# 食物的分值及颜色
Food_Style_List = [(10, (255, 100, 100)), (20, (100, 255, 100)), (30, (100, 100, 255))]


Black = (0, 0, 0)      # 黑色，蛇的颜色
Black = (0, 0, 0)           # 黑色，网格线颜色
Red = (200, 30, 30)         # 红色，GAME OVER 的字体颜色
Bgcolor = (255, 255, 255)      # 白色，背景色

# 显示整个界面
def print_text(screen, font, x, y, text, fcolor=(0, 0, 0)):
    imgText = font.render(text, True, fcolor)#渲染字体和分数
    screen.blit(imgText, (x, y))# 画上光标


# 初始化蛇
def init_snake():
    snake = deque()#创建一个空的初始化蛇
    snake.append((2, Scope_Y[0]))
    snake.append((1, Scope_Y[0]))
    snake.append((0, Scope_Y[0]))#初始化蛇的长度为3
    return snake

#随机创造果实
def create_food(snake):
    food_x = random.randint(Scope_X[0], Scope_X[1])
    food_y = random.randint(Scope_Y[0], Scope_Y[1])#随机创造果实的位置
    while (food_x, food_y) in snake:
        # 如果食物出现在蛇身上，则重来
        food_x = random.randint(Scope_X[0], Scope_X[1])
        food_y = random.randint(Scope_Y[0], Scope_Y[1])
    return food_x, food_y

#随机得到一个果实
def get_food_style():
    return Food_Style_List[random.randint(0, 2)]


def main():
    pygame.init()
    screen = pygame.display.set_mode((Screen_Width, Screen_Height))
    pygame.display.set_caption('贪吃蛇')

    font1 = pygame.font.SysFont('SimHei', 24)  # 得分的字体
    font2 = pygame.font.Font(None, 72)  # GAME OVER 的字体
    fwidth, fheight = font2.size('GAME OVER')

    # 如果蛇正在向右移动，那么快速点击向下向左，由于程序刷新没那么快，向下事件会被向左覆盖掉，导致蛇后退，直接GAME OVER
    # b 变量就是用于防止这种情况的发生
    b = True

    # 蛇
    snake = init_snake()
    # 食物
    food = create_food(snake)
    food_style = get_food_style()
    # 方向
    pos = (1, 0)

    game_over = True
    start = False       # 是否开始，当start = True，game_over = True 时，才显示 GAME OVER
    score = 0           # 得分
    orispeed = 0.5      # 原始速度
    speed = orispeed
    last_move_time = None
    pause = False       # 暂停

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if game_over:
                        start = True
                        game_over = False
                        b = True
                        snake = init_snake()
                        food = create_food(snake)
                        food_style = get_food_style()
                        pos = (1, 0)
                        # 得分
                        score = 0
                        last_move_time = time.time()
                elif event.key == K_SPACE:
                    if not game_over:
                        pause = not pause
                elif event.key in (K_w, K_UP):
                    # 这个判断是为了防止蛇向上移时按了向下键，导致直接 GAME OVER
                    if b and not pos[1]:
                        pos = (0, -1)
                        b = False
                elif event.key in (K_s, K_DOWN):
                    if b and not pos[1]:
                        pos = (0, 1)
                        b = False
                elif event.key in (K_a, K_LEFT):
                    if b and not pos[0]:
                        pos = (-1, 0)
                        b = False
                elif event.key in (K_d, K_RIGHT):
                    if b and not pos[0]:
                        pos = (1, 0)
                        b = False

        # 填充背景色
        screen.fill(Bgcolor)
        # 画网格线 竖线
        for x in range(Size, Screen_Width, Size):
            pygame.draw.line(screen, Black, (x, Scope_Y[0] * Size), (x, Screen_Height), Line_Width)
        # 画网格线 横线
        for y in range(Scope_Y[0] * Size, Screen_Height, Size):
            pygame.draw.line(screen, Black, (0, y), (Screen_Width, y), Line_Width)

        if not game_over:
            curTime = time.time()
            if curTime - last_move_time > speed:
                if not pause:
                    b = True
                    last_move_time = curTime
                    next_s = (snake[0][0] + pos[0], snake[0][1] + pos[1])
                    if next_s == food:
                        # 吃到了食物
                        snake.appendleft(next_s)
                        score += food_style[0]
                        speed = orispeed - 0.03 * (score // 100)
                        food = create_food(snake)
                        food_style = get_food_style()
                    else:
                        if Scope_X[0] <= next_s[0] <= Scope_X[1] and Scope_Y[0] <= next_s[1] <= Scope_Y[1] \
                                and next_s not in snake:
                            snake.appendleft(next_s)
                            snake.pop()
                        else:
                            game_over = True

        # 画食物
        if not game_over:
            # 避免 GAME OVER 的时候把 GAME OVER 的字给遮住了
            pygame.draw.rect(screen, food_style[1], (food[0] * Size, food[1] * Size, Size, Size), 0)

        # 画蛇
        for s in snake:
            pygame.draw.rect(screen, Black, (s[0] * Size + Line_Width, s[1] * Size + Line_Width,
                                            Size - Line_Width * 2, Size - Line_Width * 2), 0)

        print_text(screen, font1, 30, 7, f'速度: {score//100}')
        print_text(screen, font1, 450, 7, f'得分: {score}')

        if game_over:
            if start:
                print_text(screen, font2, (Screen_Width - fwidth) // 2, (Screen_Height - fheight) // 2, 'GAME OVER', Red)

        pygame.display.update()


if __name__ == '__main__':
    main()