import sys
import time
import pygame

# Define colors and sizes
backgroundColor = (251, 247, 245)
lineColor = (0, 0, 0)
selectedColor = (173, 216, 230)  # Light blue for highlighting
buttonColor = (100, 100, 100)    # Gray for button
buttonTextColor = (255, 255, 255)  # White for button text
userInputColor = (0, 0, 255)     # Blue for user input
cellSize = 50
gridPos = (50, 100)  # Adjusted to make space for the buttons
gridSize = cellSize * 9
buttonWidth, buttonHeight = 100, 40
solveButtonPos = (gridPos[0], gridPos[1] - 60)  # Solve button position
clearButtonPos = (gridPos[0] + 150, gridPos[1] - 60)  # Clear button position

# Initialize the grid
grid = [[0 for _ in range(9)] for _ in range(9)]  # 9x9 grid initialized to 0
userInputGrid = [[False for _ in range(9)] for _ in range(9)]  # Track user-added numbers

def draw_grid(win):
    for i in range(0, 10):
        thickness = 5 if i % 3 == 0 else 2
        pygame.draw.line(win, lineColor, (gridPos[0] + cellSize * i, gridPos[1]),
                         (gridPos[0] + cellSize * i, gridPos[1] + gridSize), thickness)
        pygame.draw.line(win, lineColor, (gridPos[0], gridPos[1] + cellSize * i),
                         (gridPos[0] + gridSize, gridPos[1] + cellSize * i), thickness)

def draw_numbers(win):
    font = pygame.font.SysFont(None, 40)
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                color = userInputColor if userInputGrid[i][j] else lineColor
                text = font.render(str(grid[i][j]), True, color)
                win.blit(text, (gridPos[0] + j * cellSize + 15, gridPos[1] + i * cellSize + 10))

def draw_buttons(win):
    # Draw Solve and Clear buttons
    pygame.draw.rect(win, buttonColor, (*solveButtonPos, buttonWidth, buttonHeight))
    pygame.draw.rect(win, buttonColor, (*clearButtonPos, buttonWidth, buttonHeight))
    
    font = pygame.font.SysFont(None, 30)
    solve_text = font.render("Solve", True, buttonTextColor)
    clear_text = font.render("Clear", True, buttonTextColor)
    win.blit(solve_text, (solveButtonPos[0] + 20, solveButtonPos[1] + 7))
    win.blit(clear_text, (clearButtonPos[0] + 20, clearButtonPos[1] + 7))

def clear_board():
    global grid, userInputGrid
    grid = [[0 for _ in range(9)] for _ in range(9)]
    userInputGrid = [[False for _ in range(9)] for _ in range(9)]

def turn_user_numbers_blue():
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                userInputGrid[i][j] = True

def is_valid(num, pos):
    row, col = pos
    if num in grid[row]: return False
    if num in [grid[i][col] for i in range(9)]: return False

    box_x, box_y = col // 3, row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if grid[i][j] == num and (i, j) != pos:
                return False
    return True

def find_empty():
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)  # row, col
    return None

def draw_solution(win, number, pos, delay=0.1):
    font = pygame.font.SysFont(None, 40)
    text = font.render(str(number), True, lineColor)
    win.blit(text, (gridPos[0] + pos[1] * cellSize + 15, gridPos[1] + pos[0] * cellSize + 10))
    pygame.display.update()
    time.sleep(delay)

def solve_sudoku(win):
    turn_user_numbers_blue()

    def find_empty_with_mrv():
        min_options, best_pos = 10, None
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    options = sum(1 for n in range(1, 10) if is_valid(n, (i, j)))
                    if options < min_options:
                        min_options, best_pos = options, (i, j)
        return best_pos

    def forward_checking():
        find = find_empty_with_mrv()
        if not find: return True  # Solved
        row, col = find
        for i in range(1, 10):
            if is_valid(i, (row, col)):
                grid[row][col] = i
                draw_solution(win, i, (row, col))
                if forward_checking(): return True
                grid[row][col] = 0
        return False

    forward_checking()

def main():
    pygame.init()
    win = pygame.display.set_mode((550, 650))  # Adjusted height for buttons
    pygame.display.set_caption("Sudoku Solver")

    selected = None

    while True:
        win.fill(backgroundColor)
        draw_buttons(win)
        draw_grid(win)
        if selected: pygame.draw.rect(win, selectedColor, (gridPos[0] + selected[0] * cellSize, gridPos[1] + selected[1] * cellSize, cellSize, cellSize))
        draw_numbers(win)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()

                # Check if "Solve" button clicked
                if solveButtonPos[0] <= mousePos[0] <= solveButtonPos[0] + buttonWidth and solveButtonPos[1] <= mousePos[1] <= solveButtonPos[1] + buttonHeight:
                    solve_sudoku(win)

                # Check if "Clear" button clicked
                elif clearButtonPos[0] <= mousePos[0] <= clearButtonPos[0] + buttonWidth and clearButtonPos[1] <= mousePos[1] <= clearButtonPos[1] + buttonHeight:
                    clear_board()

                # Check for grid clicks
                elif gridPos[0] < mousePos[0] < gridPos[0] + gridSize and gridPos[1] < mousePos[1] < gridPos[1] + gridSize:
                    x, y = (mousePos[0] - gridPos[0]) // cellSize, (mousePos[1] - gridPos[1]) // cellSize
                    selected = (x, y)

            if event.type == pygame.KEYDOWN and selected:
                key = event.key
                if pygame.K_1 <= key <= pygame.K_9:
                    grid[selected[1]][selected[0]] = key - pygame.K_0
                    userInputGrid[selected[1]][selected[0]] = True
                elif key == pygame.K_0:
                    grid[selected[1]][selected[0]] = 0
                    userInputGrid[selected[1]][selected[0]] = False

        pygame.display.update()

if __name__ == "__main__":
    main()
