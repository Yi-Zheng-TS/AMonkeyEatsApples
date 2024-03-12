import pygame
import time
from random import randint
from sys import exit


# 
SCREEN_HEIGHT = 580
SCREEN_WIDTH = 800
JUMP_STATUS = False
move_set = {pygame.K_LEFT:0, pygame.K_RIGHT:0, pygame.K_UP:0, pygame.K_DOWN:0}
START_TIME = None
GAME_OVER = False
# 定义一个画面帧率
fps = 60
# 定义一个动画周期
cycle = 30
# 控制游戏循环的频率对象
clock = pygame.time.Clock()
# 定义一个当前页面存储的苹果个数
ticks = 0


# 定义一个精灵类：猴子
class Monkey(pygame.sprite.Sprite):
    score = 0
    # 定义一个初始化方法，调用父类的初始化方法
    def __init__(self, mon_path, mon_pos):
        pygame.sprite.Sprite.__init__(self)
        # 设置猴子图片
        self.image = mon_path
        # 获取猴子图片矩形区域
        self.rect = self.image.get_rect()
        # 设置猴子图片位置
        self.rect.topleft = mon_pos
        self.speed = 100

    # 猴子移动的方法
    def move(self, move_set):
        global JUMP_STATUS
        x = self.rect.left + move_set[pygame.K_RIGHT] - move_set[pygame.K_LEFT]
        y = self.rect.top + move_set[pygame.K_DOWN] - move_set[pygame.K_UP]
        # 判断跳跃移动的位置
        if y <= 0:
            # 猴子在矩形区域最上方
            self.rect.top = 0
            # 如果y小于等于0意味着猴子已经跳跃了
            JUMP_STATUS = True
        elif y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
            JUMP_STATUS = False
        else:
            self.rect.top = y
            JUMP_STATUS = True

        # 判断左右移动的位置
        if x <= 0:
            self.rect.left = 0
        elif x >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left = x

    # 猴子拾到苹果，苹果消失
    def get_apple(self, apple_group):
        # 后去接到的苹果
        get_apples = pygame.sprite.spritecollide(self, apple_group, True)
        # 计算分数（一个苹果一分）
        self.score += len(get_apples)
        # 接到的苹果消失
        for apple in get_apples:
            apple.kill()


# 定义一个精灵类：苹果
class Apple(pygame.sprite.Sprite):
    # 定义一个初始化方法，调用父类的初始化方法
    def __init__(self, app_path, app_pos):
        pygame.sprite.Sprite.__init__(self)
        # 设置苹果图片
        self.image = app_path
        # 获取苹果图片矩形区域
        self.rect = self.image.get_rect()
        # 设置苹果图片位置
        self.rect.topleft = app_pos
        self.speed = 1

    # 定义一个刷新方法
    def update(self):
        global START_TIME
        if START_TIME is None:
            START_TIME = time.time()

        # 获取苹果矩形区域的top点
        self.rect.top += self.speed * (1 + (time.time() - START_TIME) / 50)
        # 判断苹果的最终top位置是否大于主窗口的屏幕高度，如果是，表示苹果落地
        if self.rect.top > SCREEN_HEIGHT:
            global GAME_OVER
            GAME_OVER = True
            self.kill()


# 初始化游戏
pygame.init()
# 设置游戏的主窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# 设置主窗口标题
pygame.display.set_caption('A monkey picks up apples')
# 设置背景图片
back_ground = pygame.image.load('bg.jpg').convert()
# 获取猴子图片
mon_path = pygame.image.load('monkey.png').convert_alpha()
# 获取苹果图片
app_path = pygame.image.load('apple.jpg').convert_alpha()
# 实例化猴子对象
monkey = Monkey(mon_path, (60, 50))
# 实例化苹果对象
apple = Apple(app_path, (10, 15))
# 创建苹果组
app_group = pygame.sprite.Group()
# 定义分数的字体
score_font = pygame.font.SysFont('arial', 40)
# 游戏主循环
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#     screen.blit(back_ground, (0, 0))
#     screen.blit(monkey.image, monkey.rect)
#     screen.blit(apple.image, apple.rect)
#     # 刷新游戏主窗口
#     pygame.display.flip()
while True:
    if GAME_OVER:
        break

    # 控制游戏最大帧率
    clock.tick(fps)
    # 绘制游戏的的背景图片
    screen.blit(back_ground, (0, 0))
    # 定义页面最多苹果个数
    if ticks >= cycle:
        ticks = 0
    # 如果ticks刚好为30或30的倍数，那么就要重新产生新的苹果
    if ticks % 30 == 0:
        apple = Apple(app_path, [randint(0, SCREEN_WIDTH-app_path.get_width()), 0])
        app_group.add(apple)
    # 刷新控制苹果
    app_group.update()
    # 绘制苹果组到游戏窗口
    app_group.draw(screen)
    # 绘制猴子到游戏窗口
    screen.blit(mon_path, monkey.rect)
    
    ticks += 1
    # 猴子实现接苹果的方法
    monkey.get_apple(app_group)
    # 更新分数
    score_surface = score_font.render(str(monkey.score), True, (0, 0, 255))
    # 将分数绘制到屏幕上方
    screen.blit(score_surface, (600, 100))
    # 更新屏幕
    pygame.display.update()
    # 判断事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # 控制猴子运行方向
        if event.type == pygame.KEYDOWN:
            if event.key in move_set:
                if event.key == pygame.K_UP:
                    move_set[event.key] = 400
                else:
                    move_set[event.key] = monkey.speed
        elif event.type == pygame.KEYUP:
            if event.key in move_set:
                move_set[event.key] = 0

        # 判断猴子跳跃动作
        if JUMP_STATUS:
            move_set[pygame.K_DOWN] = 200
            move_set[pygame.K_UP] = 0

        monkey.move(move_set)


# 游戏结束退出界面
score_surface = score_font.render(str(monkey.score), True, (0, 0, 255))
# 游戏结束提示信息
game_over_surface = score_font.render('GAME OVER', True, (0, 0, 255))
screen.blit(score_surface, (600, 10))
screen.blit(game_over_surface, (300, 240))


while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()