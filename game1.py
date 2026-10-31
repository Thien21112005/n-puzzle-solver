import pygame
pygame.init()
screen = pygame.display.set_mode((601, 601))
pygame.display.set_caption('Ran San Moi')
running = True
PINK = (255, 141, 161)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
clock = pygame.time.Clock()
snake = [10, 10]   # vị trí ban đầu

direction = "right"  # chỉ khởi tạo 1 lần
while running:
    clock.tick(10)   # tốc độ rắn (10 fps thôi cho dễ nhìn)
    screen.fill(PINK)
    for i in range(21):
        pygame.draw.line(screen, WHITE, (0, i*30), (600, i*30))
        pygame.draw.line(screen, WHITE, (i*30, 0), (i*30, 600))
    # xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "down":
                direction = "up"
            if event.key == pygame.K_DOWN and direction != "up":
                direction = "down"
            if event.key == pygame.K_LEFT and direction != "right":
                direction = "left"
            if event.key == pygame.K_RIGHT and direction != "left":
                direction = "right"
    # cập nhật vị trí rắn theo hướng
    if direction == "up":
        snake[1] -= 1
    if direction == "down":
        snake[1] += 1
    if direction == "left":
        snake[0] -= 1
    if direction == "right":
        snake[0] += 1
    pygame.draw.rect(screen, GREEN, (snake[0]*30, snake[1]*30, 30, 30))
    pygame.display.flip()



