import pygame
import sys
import random
import os
from collections import deque
from tkinter import Tk, filedialog
from tkinter import messagebox
import heapq

# Kích thước màn hình
GAME_WIDTH, HEIGHT = 400, 400
SCREEN_WIDTH = 800
ROWS, COLS = 3, 3
TILE_SIZE = GAME_WIDTH // COLS

# Màu sắc
BG_COLOR = (245, 245, 220)
EXTENDED_BG_COLOR = (220, 230, 240)  # Màu xanh nhạt cho phần mở rộng
TILE_COLOR = (120, 160, 180)
EMPTY_COLOR = (220, 220, 220)
TEXT_COLOR = (50, 50, 50)
ACCENT_COLOR = (70, 130, 180)
BUTTON_COLOR = (100, 150, 200)
BUTTON_HOVER = (80, 130, 180)
GREEN = (80, 200, 120)
RED = (220, 100, 100)
TRASH_COLOR = (200, 80, 80)
TRASH_HOVER = (220, 100, 100)
RESET_COLOR = (150, 100, 200)
RESET_HOVER = (170, 120, 220)

# Đường dẫn icon thùng rác (chỉnh path nếu cần, file PNG khoảng 20x20px)
TRASH_ICON_PATH = 'bin.png'
RESET_ICON_PATH = 'reset.png'  # Thêm đường dẫn icon reset nếu có
trash_icon = None
reset_icon = None
if os.path.exists(TRASH_ICON_PATH):
    trash_icon = pygame.image.load(TRASH_ICON_PATH)
    trash_icon = pygame.transform.smoothscale(trash_icon, (20, 20))  # Scale fit nút

if os.path.exists(RESET_ICON_PATH):
    reset_icon = pygame.image.load(RESET_ICON_PATH)
    reset_icon = pygame.transform.smoothscale(reset_icon, (20, 20))  # Scale fit nút

total_step = 0
win = False
solving = False
solution_path = []
using_image = False
original_image = None
reference_image = None
image_tiles = []
initial_state = None  # Lưu trạng thái ban đầu

# Danh sách thuật toán
algorithms = ["BFS", "DFS", "UCS", "A*", "Greedy"]
current_algo = "BFS"
show_algo_menu = False


# Trạng thái ban đầu
def tao_state_random():
    dau = []
    tmp = set()
    for _ in range(3):
        lst = []
        for _ in range(3):
            hehe = random.randint(0, 8)
            while hehe in tmp:
                hehe = random.randint(0, 8)
            lst.append(hehe)
            tmp.add(hehe)
        dau.append(lst)
    return dau



# Trạng thái đích
state = tao_state_random()
goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]
clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, HEIGHT + 150))
pygame.display.set_caption("8 Puzzle Game")
font = pygame.font.SysFont("Arial", 50, bold=True)
font1 = pygame.font.SysFont("Arial", 20, bold=True)
font2 = pygame.font.SysFont("Arial", 16, bold=True)

# Lưu trạng thái ban đầu
initial_state = [row[:] for row in state]


def make_rounded_image(surface, radius):
    """Tạo phiên bản bo góc cho surface"""
    w, h = surface.get_size()
    mask = pygame.Surface((w, h), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0))
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, w, h), border_radius=radius)
    rounded = surface.copy().convert_alpha()
    rounded.blit(mask, (0, 0), None, pygame.BLEND_RGBA_MULT)
    return rounded


def draw_grid():
    """Vẽ lưới bàn cờ"""
    # Vẽ nền chính (phần trái - game area)
    screen.fill(BG_COLOR)

    # Vẽ nền phần mở rộng (phần phải)
    extended_area = pygame.Rect(GAME_WIDTH, 0, SCREEN_WIDTH - GAME_WIDTH, HEIGHT)
    pygame.draw.rect(screen, EXTENDED_BG_COLOR, extended_area)

    # Vẽ đường phân cách nhẹ giữa 2 phần
    pygame.draw.line(screen, ACCENT_COLOR, (GAME_WIDTH, 0), (GAME_WIDTH, HEIGHT), 2)

    for i in range(ROWS):
        for j in range(COLS):
            num = state[i][j]
            x, y = j * TILE_SIZE, i * TILE_SIZE
            rect = pygame.Rect(x + 5, y + 5, TILE_SIZE - 10, TILE_SIZE - 10)

            if num != 0:
                if using_image and image_tiles:
                    # Vẽ phần hình ảnh nếu đang sử dụng hình, với bo góc
                    tile_index = num - 1  # Vì số từ 1-8, index từ 0-7
                    rounded_tile = make_rounded_image(image_tiles[tile_index], 10)
                    screen.blit(rounded_tile, (x + 5, y + 5))
                else:
                    # Vẽ ô vuông màu nếu không dùng hình
                    pygame.draw.rect(screen, TILE_COLOR, rect, border_radius=10)
                    text = font.render(str(num), True, TEXT_COLOR)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
            else:
                if using_image and image_tiles:
                    # Vẽ tile cho ô trống (num=0): image_tiles[8], nhưng xám và mờ
                    tile = image_tiles[8].copy()
                    grayscale_tile = pygame.transform.grayscale(tile)
                    grayscale_tile.set_alpha(128)  # 50% mờ
                    rounded_tile = make_rounded_image(grayscale_tile, 10)
                    screen.blit(rounded_tile, (x + 5, y + 5))
                else:
                    pygame.draw.rect(screen, EMPTY_COLOR, rect, border_radius=10)


def find_blank():
    """Tìm vị trí ô trống"""
    for i in range(ROWS):
        for j in range(COLS):
            if state[i][j] == 0:
                return i, j


def move(direction):
    if win: return
    i, j = find_blank()
    global total_step
    step = False
    if direction == "up" and i < 2:
        state[i][j], state[i + 1][j] = state[i + 1][j], state[i][j]
        step = True
    elif direction == "down" and i > 0:
        state[i][j], state[i - 1][j] = state[i - 1][j], state[i][j]
        step = True
    elif direction == "left" and j < 2:
        state[i][j], state[i][j + 1] = state[i][j + 1], state[i][j]
        step = True
    elif direction == "right" and j > 0:
        state[i][j], state[i][j - 1] = state[i][j - 1], state[i][j]
        step = True
    if step: total_step += 1


def check_win():
    return state == goal_state


def state_to_tuple(state):
    """Chuyển trạng thái thành tuple để có thể băm được"""
    return tuple(tuple(row) for row in state)


def get_possible_moves(state):
    """Lấy danh sách các nước đi có thể từ trạng thái hiện tại"""
    moves = []
    i, j = find_blank_in_state(state)

    if i > 0: moves.append(("down", i - 1, j))
    if i < 2: moves.append(("up", i + 1, j))
    if j > 0: moves.append(("right", i, j - 1))
    if j < 2: moves.append(("left", i, j + 1))

    return moves


def find_blank_in_state(state):
    """Tìm vị trí ô trống trong một trạng thái bất kỳ"""
    for i in range(ROWS):
        for j in range(COLS):
            if state[i][j] == 0:
                return i, j
    return -1, -1


def apply_move(state, move):
    """Áp dụng một nước đi lên trạng thái"""
    direction, i, j = move
    new_state = [row[:] for row in state]
    blank_i, blank_j = find_blank_in_state(new_state)

    new_state[blank_i][blank_j], new_state[i][j] = new_state[i][j], new_state[blank_i][blank_j]

    return new_state


def heuristic(state):
    """Heuristic Manhattan distance cho 8-puzzle"""
    total = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                target_i = (state[i][j] - 1) // 3
                target_j = (state[i][j] - 1) % 3
                total += abs(i - target_i) + abs(j - target_j)
    return total


def bfs_solve(initial_state, goal_state):
    """Giải bài toán bằng thuật toán BFS"""
    queue = deque([(initial_state, [])])
    visited = set()
    visited.add(state_to_tuple(initial_state))

    while queue:
        current_state, path = queue.popleft()

        if current_state == goal_state:
            return path

        for move in get_possible_moves(current_state):
            direction, _, _ = move
            new_state = apply_move(current_state, move)
            new_state_tuple = state_to_tuple(new_state)

            if new_state_tuple not in visited:
                visited.add(new_state_tuple)
                queue.append((new_state, path + [direction]))

    return None


def dfs_solve(initial_state, goal_state):
    """Giải bài toán bằng thuật toán DFS"""
    stack = [(initial_state, [])]
    visited = set()
    visited.add(state_to_tuple(initial_state))

    while stack:
        current_state, path = stack.pop()

        if current_state == goal_state:
            return path

        for move in get_possible_moves(current_state):
            direction, _, _ = move
            new_state = apply_move(current_state, move)
            new_state_tuple = state_to_tuple(new_state)

            if new_state_tuple not in visited:
                visited.add(new_state_tuple)
                stack.append((new_state, path + [direction]))

    return None


def ucs_solve(initial_state, goal_state):
    """Giải bài toán bằng thuật toán UCS (Uniform Cost Search)"""
    priority_queue = []
    heapq.heappush(priority_queue, (0, initial_state, []))  # (cost, state, path)
    visited = set()
    visited.add(state_to_tuple(initial_state))

    while priority_queue:
        cost, current_state, path = heapq.heappop(priority_queue)

        if current_state == goal_state:
            return path

        for move in get_possible_moves(current_state):
            direction, _, _ = move
            new_state = apply_move(current_state, move)
            new_state_tuple = state_to_tuple(new_state)

            if new_state_tuple not in visited:
                visited.add(new_state_tuple)
                new_cost = cost + 1
                heapq.heappush(priority_queue, (new_cost, new_state, path + [direction]))

    return None


def a_star_solve(initial_state, goal_state):
    """Giải bài toán bằng thuật toán A*"""
    priority_queue = []
    heapq.heappush(priority_queue, (0 + heuristic(initial_state), 0, initial_state, []))  # (f, g, state, path)
    visited = set()
    visited.add(state_to_tuple(initial_state))

    while priority_queue:
        _, g, current_state, path = heapq.heappop(priority_queue)

        if current_state == goal_state:
            return path

        for move in get_possible_moves(current_state):
            direction, _, _ = move
            new_state = apply_move(current_state, move)
            new_state_tuple = state_to_tuple(new_state)

            if new_state_tuple not in visited:
                visited.add(new_state_tuple)
                new_g = g + 1
                f = new_g + heuristic(new_state)
                heapq.heappush(priority_queue, (f, new_g, new_state, path + [direction]))

    return None


def greedy_solve(initial_state, goal_state):
    """Giải bài toán bằng thuật toán Greedy Best-First Search"""
    priority_queue = []
    heapq.heappush(priority_queue, (heuristic(initial_state), initial_state, []))  # (h, state, path)
    visited = set()
    visited.add(state_to_tuple(initial_state))

    while priority_queue:
        _, current_state, path = heapq.heappop(priority_queue)

        if current_state == goal_state:
            return path

        for move in get_possible_moves(current_state):
            direction, _, _ = move
            new_state = apply_move(current_state, move)
            new_state_tuple = state_to_tuple(new_state)

            if new_state_tuple not in visited:
                visited.add(new_state_tuple)
                h = heuristic(new_state)
                heapq.heappush(priority_queue, (h, new_state, path + [direction]))

    return None


def start_solution(algo):
    """Bắt đầu quá trình giải tự động bằng thuật toán được chọn"""
    global solving, solution_path

    solving = True
    if algo == "BFS":
        solution_path = bfs_solve(state, goal_state)
    elif algo == "DFS":
        solution_path = dfs_solve(state, goal_state)
    elif algo == "UCS":
        solution_path = ucs_solve(state, goal_state)
    elif algo == "A*":
        solution_path = a_star_solve(state, goal_state)
    elif algo == "Greedy":
        solution_path = greedy_solve(state, goal_state)

    if solution_path:
        print(f"Tìm thấy giải pháp với {len(solution_path)} bước bằng {algo}")
    else:
        print(f"Không tìm thấy giải pháp bằng {algo}")
        solving = False


def draw_button(rect, text, base_color, hover_color, border_color=(60, 60, 60), disabled_color=None, is_disabled=False):
    """Hàm chung để vẽ nút"""
    mouse_over = rect.collidepoint(pygame.mouse.get_pos())
    if is_disabled and disabled_color:
        color = disabled_color
    elif mouse_over:
        color = hover_color
    else:
        color = base_color
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=8)
    txt = font2.render(text, True, TEXT_COLOR)
    txt_center = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_center)


def draw_trash_icon(rect, base_color, hover_color, border_color=(60, 60, 60)):
    """Vẽ nút thùng rác với icon load từ file (fallback vẽ thủ công nếu ko có file)"""
    mouse_over = rect.collidepoint(pygame.mouse.get_pos())
    color = hover_color if mouse_over else base_color

    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=8)

    center_x, center_y = rect.center

    if trash_icon:
        # Load và vẽ icon từ file
        icon_rect = trash_icon.get_rect(center=(center_x, center_y))
        screen.blit(trash_icon, icon_rect)
    else:
        # Fallback vẽ thủ công nếu ko có file
        icon_size = 16
        bin_rect = pygame.Rect(center_x - 8, center_y - 6, 16, 12)
        pygame.draw.rect(screen, TEXT_COLOR, bin_rect, 2)
        lid_rect = pygame.Rect(center_x - 10, center_y - 8, 20, 3)
        pygame.draw.rect(screen, TEXT_COLOR, lid_rect)
        handle_rect = pygame.Rect(center_x - 3, center_y - 10, 6, 2)
        pygame.draw.rect(screen, TEXT_COLOR, handle_rect, 1)
        pygame.draw.line(screen, TEXT_COLOR, (center_x - 4, center_y - 3), (center_x - 4, center_y + 3), 2)
        pygame.draw.line(screen, TEXT_COLOR, (center_x, center_y - 3), (center_x, center_y + 3), 2)
        pygame.draw.line(screen, TEXT_COLOR, (center_x + 4, center_y - 3), (center_x + 4, center_y + 3), 2)


def draw_reset_icon(rect, base_color, hover_color, border_color=(60, 60, 60)):
    """Vẽ nút reset với icon load từ file (fallback vẽ thủ công nếu ko có file)"""
    mouse_over = rect.collidepoint(pygame.mouse.get_pos())
    color = hover_color if mouse_over else base_color

    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=8)

    center_x, center_y = rect.center

    if reset_icon:
        # Load và vẽ icon từ file
        icon_rect = reset_icon.get_rect(center=(center_x, center_y))
        screen.blit(reset_icon, icon_rect)
    else:
        # Fallback vẽ thủ công nếu ko có file - vẽ mũi tên xoay tròn
        radius = 8
        pygame.draw.circle(screen, TEXT_COLOR, (center_x, center_y), radius, 2)
        # Vẽ mũi tên
        pygame.draw.line(screen, TEXT_COLOR, (center_x + radius - 2, center_y - 5),
                         (center_x + radius + 2, center_y - 1), 2)
        pygame.draw.line(screen, TEXT_COLOR, (center_x + radius + 2, center_y - 1),
                         (center_x + radius - 2, center_y + 3), 2)


def choose_image():
    """Mở hộp thoại chọn hình ảnh"""
    global using_image, original_image, image_tiles, reference_image, state, initial_state

    root = Tk()
    root.withdraw()  # Ẩn cửa sổ chính của Tkinter

    file_path = filedialog.askopenfilename(
        title="Chọn hình ảnh",
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
    )

    root.destroy()

    if file_path:
        try:
            # Tải hình ảnh và chia thành các ô, sử dụng smoothscale để giữ chất lượng
            img = pygame.image.load(file_path)
            original_image = pygame.transform.smoothscale(img, (GAME_WIDTH - 10, HEIGHT - 10))  # Scale nhẹ để fit
            image_tiles = []
            # Thêm 9 tiles: 8 cho số 1-8, 1 cho ô trống (có thể là phần cuối cùng)
            for i in range(ROWS):
                for j in range(COLS):
                    # Tạo surface cho từng ô
                    tile_surface = pygame.Surface((TILE_SIZE - 10, TILE_SIZE - 10), pygame.SRCALPHA)
                    # Cắt phần hình ảnh tương ứng với smoothscale nếu cần
                    tile_surface.blit(original_image, (0, 0),
                                      (j * TILE_SIZE, i * TILE_SIZE,
                                       TILE_SIZE - 10, TILE_SIZE - 10))
                    image_tiles.append(tile_surface)

            reference_image = pygame.transform.smoothscale(original_image, (150, 150))

            using_image = True
            # Tạo state mới và lưu làm initial_state
            state = tao_state_random()
            initial_state = [row[:] for row in state]
            print("Đã tải hình ảnh thành công!")
        except Exception as e:
            print(f"Lỗi khi tải hình ảnh: {e}")
            # Hiển thị thông báo lỗi
            root = Tk()
            root.withdraw()
            messagebox.showerror("Lỗi", "Không thể tải hình ảnh. Vui lòng chọn file hợp lệ.")
            root.destroy()


def remove_image():
    """Xóa hình ảnh đang sử dụng và quay về chế độ số"""
    global using_image, original_image, image_tiles, reference_image
    using_image = False
    original_image = None
    image_tiles = []
    reference_image = None


def reset_state():
    """Reset về trạng thái ban đầu (sau shuffle)"""
    global state, total_step, win, solving, solution_path
    state = [row[:] for row in initial_state]
    total_step = 0
    win = False
    solving = False
    solution_path = []
    print("Đã reset về trạng thái ban đầu!")


# Game loop
running = True
last_move_time = 0
move_delay = 200  # milliseconds between moves

while running:
    current_time = pygame.time.get_ticks()
    clock.tick(60)
    draw_grid()

    # Vẽ panel điều khiển
    control_panel = pygame.Rect(0, HEIGHT, SCREEN_WIDTH, 150)
    pygame.draw.rect(screen, (230, 230, 230), control_panel)
    pygame.draw.line(screen, ACCENT_COLOR, (0, HEIGHT), (SCREEN_WIDTH, HEIGHT), 2)

    # Hiển thị số bước di chuyển
    res = "Moves: " + str(total_step)
    txt = font1.render(res, True, TEXT_COLOR)
    screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, HEIGHT + 15))

    # Hiển thị trạng thái giải
    if solving:
        if solution_path:
            status_text = f"Đang giải bằng {current_algo}: {len(solution_path)} bước còn lại"
        else:
            status_text = f"Đang tìm giải pháp bằng {current_algo}..."
        status_surface = font2.render(status_text, True, ACCENT_COLOR)
        screen.blit(status_surface, (SCREEN_WIDTH // 2 - status_surface.get_width() // 2, HEIGHT + 45))

    # Tạo các nút với padding cải thiện
    button_width = 80  # Giảm để fit
    button_height = 35
    trash_button_size = 35  # Nút thùng rác vuông
    reset_button_size = 35  # Nút reset vuông
    button_margin = 10  # Giảm margin
    button_y = HEIGHT + 80  # Hàng nút chính

    # Layout nút chính (Shuffle | Choose | Algo | Solve) - thân thiện, cân bằng
    num_buttons = 4
    total_width = (num_buttons * button_width) + ((num_buttons - 1) * button_margin)
    start_x = (SCREEN_WIDTH - total_width) // 2

    # Nút Shuffle (bên trái, xanh để nổi bật chức năng random)
    shuffle_rect = pygame.Rect(start_x, button_y, button_width, button_height)
    draw_button(shuffle_rect, "Shuffle", GREEN, (100, 220, 140))

    # Nút Choose (bên cạnh Shuffle, cho chọn hình)
    choose_x = start_x + button_width + button_margin
    choose_rect = pygame.Rect(choose_x, button_y, button_width, button_height)
    draw_button(choose_rect, "Choose", BUTTON_COLOR, BUTTON_HOVER)

    # Nút Algo (selector dropdown cho thuật toán)
    algo_x = choose_x + button_width + button_margin
    algo_rect = pygame.Rect(algo_x, button_y, button_width, button_height)
    draw_button(algo_rect, current_algo, BUTTON_COLOR, BUTTON_HOVER)

    # Nút Solve (bên phải, kích hoạt giải bằng algo hiện tại)
    solve_x = algo_x + button_width + button_margin
    solve_rect = pygame.Rect(solve_x, button_y, button_width, button_height)
    draw_button(solve_rect, "Solve", BUTTON_COLOR, BUTTON_HOVER, disabled_color=(180, 180, 180), is_disabled=solving)

    # Vẽ menu dropdown nếu show_algo_menu
    if show_algo_menu:
        menu_width = button_width
        menu_height = button_height * len(algorithms)
        total_height = HEIGHT + 150
        if button_y + button_height + menu_height > total_height:
            menu_y = button_y - menu_height
        else:
            menu_y = button_y + button_height
        menu_rect = pygame.Rect(algo_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(screen, (220, 220, 220), menu_rect, border_radius=8)
        pygame.draw.rect(screen, (60, 60, 60), menu_rect, 2, border_radius=8)

        for idx, algo in enumerate(algorithms):
            option_rect = pygame.Rect(algo_x, menu_y + button_height * idx, menu_width, button_height)
            draw_button(option_rect, algo, (240, 240, 240), (200, 200, 200))

    # Nút Reset (luôn hiển thị)
    reset_rect = pygame.Rect(SCREEN_WIDTH - reset_button_size - 10, HEIGHT + 10, reset_button_size, reset_button_size)
    draw_reset_icon(reset_rect, RESET_COLOR, RESET_HOVER)

    # Nút Trash (chỉ hiện khi using_image, đặt bên cạnh nút reset)
    if using_image:
        trash_rect = pygame.Rect(reset_rect.left - trash_button_size - 5, HEIGHT + 10, trash_button_size, trash_button_size)
        draw_trash_icon(trash_rect, TRASH_COLOR, TRASH_HOVER)

    # Hiển thị hình hoàn chỉnh bên phải nếu đang sử dụng hình ảnh
    if using_image and reference_image:
        # Vẽ khung cho hình hoàn chỉnh với nền mới
        ref_size = 150
        ref_x = GAME_WIDTH + (GAME_WIDTH - ref_size) // 2
        ref_y = (HEIGHT - ref_size) // 2
        ref_rect = pygame.Rect(ref_x, ref_y, ref_size, ref_size)

        # Tạo khung với viền đẹp hơn
        pygame.draw.rect(screen, (255, 255, 255), ref_rect, border_radius=15)  # Nền trắng
        pygame.draw.rect(screen, ACCENT_COLOR, ref_rect, 3, border_radius=15)  # Viền xanh

        screen.blit(reference_image, (ref_x, ref_y))

        # Tiêu đề cho hình hoàn chỉnh
        ref_text = font2.render("Hình hoàn chỉnh", True, TEXT_COLOR)
        screen.blit(ref_text, (ref_x + (ref_size - ref_text.get_width()) // 2, ref_y + ref_size + 10))

    # Hiển thị thông báo chiến thắng
    if win:
        win_text = font1.render("YOU WIN!", True, GREEN)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, HEIGHT + 120))

    pygame.display.flip()

    if check_win():
        pygame.display.set_caption("8 Puzzle Game - 🎉 YOU WIN!")
        win = True
        solving = False
    else:
        pygame.display.set_caption("8 Puzzle Game")

    # Xử lý các bước di chuyển tự động
    if solving and solution_path and current_time - last_move_time > move_delay:
        next_move = solution_path.pop(0)
        move(next_move)
        last_move_time = current_time

        if not solution_path:
            solving = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not solving:
            if event.key == pygame.K_UP:
                move("up")
            elif event.key == pygame.K_DOWN:
                move("down")
            elif event.key == pygame.K_LEFT:
                move("left")
            elif event.key == pygame.K_RIGHT:
                move("right")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if shuffle_rect.collidepoint(mouse_x, mouse_y) and not solving:
                    state = tao_state_random()
                    initial_state = [row[:] for row in state]  # Cập nhật initial_state
                    total_step = 0
                    win = False
                elif choose_rect.collidepoint(mouse_x, mouse_y):
                    choose_image()
                elif reset_rect.collidepoint(mouse_x, mouse_y):
                    reset_state()
                elif using_image and trash_rect.collidepoint(mouse_x, mouse_y):
                    remove_image()
                elif algo_rect.collidepoint(mouse_x, mouse_y):
                    show_algo_menu = not show_algo_menu
                elif solve_rect.collidepoint(mouse_x, mouse_y) and not solving and not win:
                    start_solution(current_algo)
                    total_step = 0
                elif show_algo_menu:
                    # Xử lý click vào option trong menu
                    for idx, algo in enumerate(algorithms):
                        option_rect = pygame.Rect(algo_x, menu_y + button_height * idx, button_width, button_height)
                        if option_rect.collidepoint(mouse_x, mouse_y):
                            current_algo = algo
                            show_algo_menu = False
                            break
pygame.quit()
sys.exit()