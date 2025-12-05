class Snake:
    def __init__(self):
        
        self.direction = "left" #初始方向向左
        self.speed = 1 #移动速度，每秒移动的网格数
        self.head = (grid_width // 2, grid_height // 2) #初始位置在屏幕中心
        self.body = [self.head, (self.head[0] + 1, self.head[1]), (self.head[0] + 2, self.head[1])] #三段
    
    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == 'UP':    new_head = (head_x, head_y - 1)
        if self.direction == 'DOWN':  new_head = (head_x, head_y + 1)
        if self.direction == 'LEFT':  new_head = (head_x - 1, head_y)
        if self.direction == 'RIGHT': new_head = (head_x + 1, head_y)

        self.body.insert(0, new_head) #新头插入到列表前端
        self.body.pop() #删除列表最后一个元素，即蛇尾
    def check_collision(self):
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= grid_width or head_y < 0 or head_y >= grid_height:
            return True
        for segment in self.body[1:]:
            if segment == (head_x, head_y):
                return True
    def collide_with_self(self):
        return self.body[0] in self.body[1:]
    def food_eaten(self, food):
        return self.body[0] == food.position
    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, white, (segment[0] * grid_size, segment[1] * grid_size, grid_size, grid_size))
    







#pygame
import pygame

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")
#
#分成10*10的网格
grid_size = 20
grid_width = screen_width // grid_size 
grid_height = screen_height // grid_size

#定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (128, 0, 0)