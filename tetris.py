import pygame
import random

# Inisialisasi
pygame.init()

# Dimensi layar
screen_width = 800
screen_height = 600

# Warna
black = (0, 0, 0)
white = (255, 255, 255)

# Membuat layar
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")

# Kecepatan jatuhnya bentuk
fall_speed = 0.1

# Menginisialisasi papan permainan
board = []
for _ in range(20):
    row = [0] * 10
    board.append(row)

# Mendefinisikan bentuk-bentuk yang mungkin
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 1, 0]]
]

def draw_board():
    for row in range(20):
        for col in range(10):
            if board[row][col] == 1:
                pygame.draw.rect(screen, white, (col * 30, row * 30, 30, 30))
            else:
                pygame.draw.rect(screen, black, (col * 30, row * 30, 30, 30), 1)

def draw_shape(shape, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                pygame.draw.rect(screen, white, ((x + col) * 30, (y + row) * 30, 30, 30))

def check_collision(shape, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                if int(y) + row >= 20 or x + col < 0 or x + col >= 10 or board[int(y) + row][x + col] == 1:
                    return True
    return False

def merge_shape(shape, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] == 1:
                board[int(y) + row][int(x) + col] = 1

def remove_completed_rows():
    rows_to_remove = []
    for row in range(20):
        if all(board[row]):
            rows_to_remove.append(row)

    for row in rows_to_remove:
        del board[row]
        new_row = [0] * 10
        board.insert(0, new_row)

def game_over():
    pygame.quit()
    quit()

# Memilih bentuk secara acak
current_shape = random.choice(shapes)
current_x = 3
current_y = 0

clock = pygame.time.Clock()

game_over_flag = False

# Game Loop
while not game_over_flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not check_collision(current_shape, current_x - 1, current_y):
                    current_x -= 1
            elif event.key == pygame.K_RIGHT:
                if not check_collision(current_shape, current_x + 1, current_y):
                    current_x += 1
            elif event.key == pygame.K_DOWN:
                if not check_collision(current_shape, current_x, current_y + 1):
                    current_y += 1
            elif event.key == pygame.K_UP:
                rotated_shape = list(zip(*current_shape[::-1]))
                if not check_collision(rotated_shape, current_x, current_y):
                    current_shape = rotated_shape

    if not check_collision(current_shape, current_x, current_y + 1):
        current_y += fall_speed
    else:
        merge_shape(current_shape, current_x, current_y)
        remove_completed_rows()
        current_shape = random.choice(shapes)
        current_x = 3
        current_y = 0

        if check_collision(current_shape, current_x, current_y):
            game_over_flag = True

    # Menggambar ke layar
    screen.fill(black)
    draw_board()
    draw_shape(current_shape, current_x, int(current_y))
    pygame.display.update()
    clock.tick(60)

game_over()