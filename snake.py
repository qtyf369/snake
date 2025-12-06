import pygame
import random

# 常量
screen_width = 1200
screen_height = 800
grid_size = 60
grid_width = screen_width // grid_size
grid_height = screen_height // grid_size

# 颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (128, 0, 0)
gray = (128, 128, 128)

class Snake:
    def __init__(self):
        self.direction = "LEFT"
        self.speed = 2
        self.head = (grid_width // 2, grid_height // 2)
        self.body = [self.head, (self.head[0]+1, self.head[1]), (self.head[0]+2, self.head[1])]
        self.movedistance = 0
        self.stop = False

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == 'UP':    new_head = (head_x, head_y-1)
        elif self.direction == 'DOWN':new_head = (head_x, head_y+1)
        elif self.direction == 'LEFT':new_head = (head_x-1, head_y)
        elif self.direction == 'RIGHT':new_head = (head_x+1, head_y)
        self.body.insert(0, new_head)
        if not self.food_eaten(food):
            self.body.pop()

    def check_collision(self):
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= grid_width or head_y < 0 or head_y >= grid_height:
            return True
        return self.body[0] in self.body[1:]

    def food_eaten(self, food):
        return self.body[0] == food.position

    def draw(self, screen):
        # 绘制蛇身（白色方块）
        for seg in self.body[1:]:
            pygame.draw.rect(screen, white, (seg[0]*grid_size, seg[1]*grid_size, grid_size, grid_size))
        
        # 绘制方形蛇头（灰色，和蛇身区分）
        head_x = self.body[0][0] * grid_size
        head_y = self.body[0][1] * grid_size
        pygame.draw.rect(screen, gray, (head_x, head_y, grid_size, grid_size))

    def pause(self):
        self.stop = not self.stop
        if self.stop:
            self.saved_speed = self.speed
            self.speed = 0
        else:
            self.speed = self.saved_speed

class Food:
    def __init__(self):
        while True:
            self.position = (random.randint(0, grid_width-1), random.randint(0, grid_height-1))
            if self.position not in snake.body:
                break
    def draw(self, screen):
        pygame.draw.rect(screen, red, (self.position[0]*grid_size, self.position[1]*grid_size, grid_size, grid_size))

# 全局初始化
snake = None
food = None
score = 0
game_over = False

def init():
    global snake, food, score, game_over
    score = 0
    snake = Snake()
    food = Food()
    game_over = False

# Pygame初始化
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("贪吃蛇（方形蛇头基础版）")
clock = pygame.time.Clock()

# 字体
font = pygame.font.Font('C:/Windows/Fonts/msyh.ttc', 36)
pause_text = font.render("暂停，按空格继续", True, white)
pause_rect = pause_text.get_rect(center=(screen_width//2, screen_height//2+200))
game_over_text = font.render("结束，按R重新开始", True, white)
game_over_rect = game_over_text.get_rect(center=(screen_width//2, screen_height//2))
score_font = pygame.font.Font('C:/Windows/Fonts/msyh.ttc', 36)

# 主循环
init()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and snake.direction != 'DOWN':
                snake.direction = 'UP'
            elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake.direction != 'UP':
                snake.direction = 'DOWN'
            elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake.direction != 'RIGHT':
                snake.direction = 'LEFT'
            elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake.direction != 'LEFT':
                snake.direction = 'RIGHT'
            elif event.key == pygame.K_r and game_over:
                init()
            elif event.key == pygame.K_SPACE and not game_over:
                snake.pause()
    
    delta_time = clock.tick(60)/1000
    screen.fill(black)

    if not game_over and not snake.stop:
        snake.speed = 2 + round(score/1000, 1)
        snake.movedistance += delta_time * snake.speed
        if snake.movedistance >= 1:
            snake.move()
            snake.movedistance -= 1
            if snake.check_collision():
                game_over = True
            if snake.food_eaten(food):
                food = Food()
                score += 10

    snake.draw(screen)
    food.draw(screen)
    if snake.stop:
        screen.blit(pause_text, pause_rect)
    score_text = score_font.render(f"分数: {score}", True, white)
    screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, 50))
    if game_over:
        screen.blit(game_over_text, game_over_rect)

    pygame.display.flip()

pygame.quit()