import sys
import time
import pygame

# Define colors and sizes
backgroundColor = (251, 247, 245)
lineColor = (0, 0, 0)
selectedColor = (173, 216, 230)  # Light blue color for highlighting
buttonColor = (100, 100, 100)    # Gray color for button
buttonTextColor = (255, 255, 255) # White color for button text
userInputColor = (0, 0, 255)     # Blue color for user input numbers
cellSize = 50
gridPos = (50, 100)  # Adjusted to make space for the button
gridSize = cellSize * 9
buttonWidth, buttonHeight = 100, 40
buttonPos = (gridPos[0] + (gridSize - buttonWidth) // 2, gridPos[1] - 60)  # Centered and closer to the grid

# Initialize the grid
grid = [[0 for _ in range(9)] for _ in range(9)]  # 9x9 grid with all cells initialized to 0
userInputGrid = [[False for _ in range(9)] for _ in range(9)]  # Track user-added numbers

def draw_grid(win):
    # Draw the Sudoku grid
    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(win, lineColor, (gridPos[0] + cellSize * i, gridPos[1]), 
                             (gridPos[0] + cellSize * i, gridPos[1] + gridSize), 5)
            pygame.draw.line(win, lineColor, (gridPos[0], gridPos[1] + cellSize * i), 
                             (gridPos[0] + gridSize, gridPos[1] + cellSize * i), 5)
        else:
            pygame.draw.line(win, lineColor, (gridPos[0] + cellSize * i, gridPos[1]), 
                             (gridPos[0] + cellSize * i, gridPos[1] + gridSize), 2)
            pygame.draw.line(win, lineColor, (gridPos[0], gridPos[1] + cellSize * i), 
                             (gridPos[0] + gridSize, gridPos[1] + cellSize * i), 2)

def draw_numbers(win):
    # Draw the numbers on the grid
    font = pygame.font.SysFont(None, 40)
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                color = userInputColor if userInputGrid[i][j] else lineColor
                text = font.render(str(grid[i][j]), True, color)
                win.blit(text, (gridPos[0] + j * cellSize + 15, gridPos[1] + i * cellSize + 10))

def highlight_cell(win, pos):
    # Draw a rectangle around the selected cell
    pygame.draw.rect(win, selectedColor, (gridPos[0] + pos[0] * cellSize, gridPos[1] + pos[1] * cellSize, cellSize, cellSize))

def draw_button(win):
    # Draw the "Solve" button
    pygame.draw.rect(win, buttonColor, (*buttonPos, buttonWidth, buttonHeight))
    font = pygame.font.SysFont(None, 30)
    text = font.render("Solve", True, buttonTextColor)
    win.blit(text, (buttonPos[0] + 20, buttonPos[1] + 7))

def draw_instructions(win):
    # Draw the instructions below the grid
    font = pygame.font.SysFont(None, 30)
    instructions = ["Click on the cell and add a number 1-9.", "If you want to delete press 0."]
    y_offset = gridPos[1] + gridSize + 20
    for line in instructions:
        text = font.render(line, True, lineColor)
        win.blit(text, (gridPos[0], y_offset))
        y_offset += 30

def turn_user_numbers_blue():
    # Change the color of user-added numbers to blue
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                userInputGrid[i][j] = True  # Mark this cell as user-inputted

def is_valid(num, pos):
    # Check if the number is valid in the given position
    # Check row
    for i in range(9):
        if grid[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(9):
        if grid[i][pos[1]] == num and pos[0] != i:
            return False

    # Check 3x3 box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if grid[i][j] == num and (i, j) != pos:
                return False

    return True

def find_empty():
    # Find an empty space in the grid
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return (i, j)  # row, col

    return None

def draw_solution(win, number, pos, delay=0.5):
    # Draw the number in the cell with a delay to show the solving process
    font = pygame.font.SysFont(None, 40)
    text = font.render(str(number), True, lineColor)
    win.blit(text, (gridPos[0] + pos[1] * cellSize + 15, gridPos[1] + pos[0] * cellSize + 10))
    pygame.display.update()
    time.sleep(delay)

def solve_sudoku(win):
    turn_user_numbers_blue()

    def find_empty_with_mrv():
        # Find the empty cell with the fewest legal values remaining
        min_options = 10  # More than the maximum possible options (1-9)
        best_pos = None

        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    num_options = sum(1 for n in range(1, 10) if is_valid(n, (i, j)))
                    if num_options < min_options:
                        min_options = num_options
                        best_pos = (i, j)
        return best_pos

    def forward_checking():
        # Use MRV to choose the next empty cell and propagate constraints
        find = find_empty_with_mrv()
        if not find:
            return True  # Puzzle solved
        else:
            row, col = find

        for i in range(1, 10):
            if is_valid(i, (row, col)):
                grid[row][col] = i
                draw_solution(win, i, (row, col), delay=0.1)  # Show the number with a smaller delay

                if forward_checking():
                    return True

                grid[row][col] = 0
                draw_solution(win, 0, (row, col), delay=0.1)  # Erase the number with a smaller delay

        return False

    forward_checking()


def main():
    pygame.init()
    win = pygame.display.set_mode((550, 650))  # Adjusted height for better spacing
    pygame.display.set_caption("Sudoku Solver")

    selected = None

    while True:
        win.fill(backgroundColor)
        draw_button(win)  # Draw the "Solve" button
        draw_grid(win)

        if selected:
            highlight_cell(win, selected)
        
        draw_numbers(win)  # Draw numbers last to ensure they appear on top
        draw_instructions(win)  # Draw the instructions below the grid

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                
                # Check if the "Solve" button is clicked
                if buttonPos[0] <= mousePos[0] <= buttonPos[0] + buttonWidth and buttonPos[1] <= mousePos[1] <= buttonPos[1] + buttonHeight:
                    solve_sudoku(win)

                # Detect which cell was clicked
                elif gridPos[0] < mousePos[0] < gridPos[0] + gridSize and gridPos[1] < mousePos[1] < gridPos[1] + gridSize:
                    x = (mousePos[0] - gridPos[0]) // cellSize
                    y = (mousePos[1] - gridPos[1]) // cellSize
                    selected = (x, y)

            if event.type == pygame.KEYDOWN:
                if selected is not None:
                    if event.key == pygame.K_1: grid[selected[1]][selected[0]] = 1
                    elif event.key == pygame.K_2: grid[selected[1]][selected[0]] = 2
                    elif event.key == pygame.K_3: grid[selected[1]][selected[0]] = 3
                    elif event.key == pygame.K_4: grid[selected[1]][selected[0]] = 4
                    elif event.key == pygame.K_5: grid[selected[1]][selected[0]] = 5
                    elif event.key == pygame.K_6: grid[selected[1]][selected[0]] = 6
                    elif event.key == pygame.K_7: grid[selected[1]][selected[0]] = 7
                    elif event.key == pygame.K_8: grid[selected[1]][selected[0]] = 8
                    elif event.key == pygame.K_9: grid[selected[1]][selected[0]] = 9
                    elif event.key == pygame.K_0: grid[selected[1]][selected[0]] = 0  # To delete the number
                    userInputGrid[selected[1]][selected[0]] = True if grid[selected[1]][selected[0]] != 0 else False

        pygame.display.update()

if __name__ == "__main__":
    main()
