import pygame
import random
import sys
from tkinter import Tk, filedialog

# --- Cấu hình ---
DIFFICULTY = 4   # số mảnh mỗi chiều (4x4 = 16 mảnh, 10x10 = 100 mảnh)
WINDOW_SIZE = 600
BG_COLOR = (180, 180, 180)

# Tắt cửa sổ Tk gốc
Tk().withdraw()

# Cho user chọn ảnh
filename = filedialog.askopenfilename(title="Chọn hình để ghép",
                                      filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

if not filename:
    print("Không có ảnh được chọn!")
    sys.exit()

# --- Khởi tạo pygame ---
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Jigsaw Puzzle")
font = pygame.font.SysFont("Arial", 60, bold=True)

# --- Load ảnh và scale giữ đúng tỉ lệ ---
img = pygame.image.load(filename)
img_rect = img.get_rect()
ratio = min(WINDOW_SIZE / img_rect.width, WINDOW_SIZE / img_rect.height)
new_w, new_h = int(img_rect.width * ratio), int(img_rect.height * ratio)
img = pygame.transform.scale(img, (new_w, new_h))

# canh giữa
offset_x = (WINDOW_SIZE - new_w) // 2
offset_y = (WINDOW_SIZE - new_h) // 2

# --- Cắt ảnh thành mảnh ---
tile_w, tile_h = new_w // DIFFICULTY, new_h // DIFFICULTY
tiles = []
correct_positions = []
for row in range(DIFFICULTY):
    for col in range(DIFFICULTY):
        rect = pygame.Rect(col * tile_w, row * tile_h, tile_w, tile_h)
        tile = img.subsurface(rect).copy()
        pos = pygame.Rect(offset_x + col * tile_w, offset_y + row * tile_h, tile_w, tile_h)
        tiles.append([tile, pos])
        correct_positions.append(pos.copy())

# --- Tráo mảnh ---
random.shuffle(tiles)

# --- Game state ---
selected = None
running = True

def draw_board():
    screen.fill(BG_COLOR)
    for tile, rect in tiles:
        screen.blit(tile, rect)
    if check_win():
        text = font.render("YOU WIN!", True, (0, 200, 0))
        rect = text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
        screen.blit(text, rect)
    pygame.display.flip()

def check_win():
    for (tile, rect), correct in zip(tiles, correct_positions):
        if rect.topleft != correct.topleft:
            return False
    return True

while running:
    draw_board()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not check_win():
            pos = pygame.mouse.get_pos()
            for idx, (tile, rect) in enumerate(tiles):
                if rect.collidepoint(pos):
                    selected = idx
        elif event.type == pygame.MOUSEBUTTONUP and selected is not None:
            pos = pygame.mouse.get_pos()
            for idx, (tile, rect) in enumerate(tiles):
                if rect.collidepoint(pos):
                    # Swap vị trí 2 mảnh
                    tiles[selected][1], tiles[idx][1] = tiles[idx][1], tiles[selected][1]
            selected = None

pygame.quit()
