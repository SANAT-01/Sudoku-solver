import tkinter as tk
import numpy as np

Num = 9

def displaying(lst, canvas): # to display the output result
    canvas.delete("all")
    canvas.create_rectangle(0, 0, 450, 450, outline="black", width=2)

    for i in range(Num):
        for j in range(Num):
            x0, y0 = j * 50, i * 50
            x1, y1 = x0 + 50, y0 + 50

            canvas.create_rectangle(x0, y0, x1, y1, outline="black", width=1)
            if lst[i][j] != 0:
                canvas.create_text(x0 + 25, y0 + 25, text=str(lst[i][j]), font=("Arial", 16))

def check(gri, rows, cols, nums): # to check the occurence the same number in its domain
    for x in range(9):
        if gri[rows][x] == nums or gri[x][cols] == nums:
            return False

    startRow = rows - rows % 3
    startCol = cols - cols % 3
    for i in range(3):
        for j in range(3):
            if gri[i + startRow][j + startCol] == nums:
                return False
    return True

def isValidSudoku(board):
    def isValid(arr):
        return sum(arr) == sum(set(arr))
    
    # Check each row in the board
    def checkRow():
        for row in board:
            if not isValid(row):
                return False
        return True
    
    # Check each col in the board,
    # To access each col, we first unpack the board into sperate lists using *
    # We then zip these rows together into columns.
    def checkCol():
        for col in zip(*board):
            if not isValid(col):
                return False
        return True
    
    # To get each sub-box, we first get the top-left indices of each sub-box,
    # We then go 3 steps on each row and 3 steps on each col to construct the box.
    def checkSub():
        for r in range(0,9,3):
            for c in range(0,9,3):
                sub = [board[r+dr][c+dc] for dr in range(3) for dc in range(3)]
                if not isValid(sub):
                    return False
        return True
    
    # In order to be a valid Sudoku, all row, col, and sub-box need to be valid
    return checkRow() and checkCol() and checkSub()


def solve(gri, rows, cols): # solves sudoku using backtracking
    if (rows == Num - 1 and cols == Num):
        return True

    if cols == Num:
        rows += 1
        cols = 0

    if gri[rows][cols] > 0:
        return solve(gri, rows, cols + 1)

    for num in range(1, Num + 1, 1):
        if check(gri, rows, cols, num):
            gri[rows][cols] = num
            if solve(gri, rows, cols + 1):
                return True
        gri[rows][cols] = 0
    return False

def solve_sudoku(): # Main function to solve sudoku
    grid_matrix = [[0 for _ in range(Num)] for _ in range(Num)]

    # Function to handle input from the GUI
    def get_input(event):
        for i in range(Num):
            for j in range(Num):
                val = entry_vars[i][j].get()
                if val:
                    grid_matrix[i][j] = int(val)
                else:
                    grid_matrix[i][j] = 0
        if not isValidSudoku(grid_matrix):
            raise "Invalid Inputs"
        root.destroy()
        
	# Creating an input grid of 9X9
    root = tk.Tk()
    root.title("Sudoku Solver")

    entry_vars = [[tk.StringVar() for _ in range(Num)] for _ in range(Num)]
    for i in range(Num): # creating each grid
        for j in range(Num):
            entry = tk.Entry(root, textvariable=entry_vars[i][j], width=5, font=("Arial", 16))
            entry.grid(row=i, column=j)

    solve_button = tk.Button(root, text="Solve", font=("Arial", 16))
    solve_button.grid(row=Num, columnspan=Num) # solve button
    solve_button.bind("<Button-1>", get_input)

    root.mainloop()

    if (solve(grid_matrix, 0, 0)):
        return grid_matrix
    else:
        return None

def solve_and_display():
    solution = solve_sudoku()
    if solution:
        root = tk.Tk()
        root.title("Sudoku Solver")

        canvas = tk.Canvas(root, width=450, height=450, bg="white")
        canvas.pack()

        displaying(solution, canvas)

        root.mainloop()
    else:
        print("Oops!!\nsorry, no solution exists ")

if __name__ == "__main__":
    solve_and_display()
