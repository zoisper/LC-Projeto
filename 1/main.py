import math
def print_sudoku(sudoku):
    l = len(sudoku)
    n = int(math.sqrt(l))
    r = l * 2 + 2 * n +1
    for i in range(l):
        if i % n == 0:
            print("-"*r)
        for j in range(l):
            if  j % n == 0:
                print("|", end = " ")
            print(sudoku[i][j], end = " ")
            if  j == l-1:
                print("|", end = " ")
        print('')
    print("-" * r)

def check(sudoku, row, column, number):
    if number in sudoku[row]:
        return False
    for r in sudoku:
        if r[column] == number:
            return False
    n = int(math.sqrt(len(sudoku)))
    r = (row // n) * n
    c = (column // n) * n
    for i in range(n):
        for j in range(n):
            if sudoku[r+i][c+j] == number:
                return False
    return True

def solve_aux(sudoku, row, column):
    n = len(sudoku)
    if row == n:
        return True

    if column == n:
        return solve_aux(sudoku, row+1, 0)

    if sudoku[row][column] != 0:
        return solve_aux(sudoku, row, column+1)


    for number in range(1, n+1):
        if check(sudoku, row, column, number):
            sudoku[row][column] = number
            if solve_aux(sudoku,row, column+1):
                return True
        sudoku[row][column] = 0
    return False




def solve_sudoku(sudoku):
    solve_aux(sudoku,0,0)



sudoku = [[4,0,0,9,0,0,3,0,0],
           [0,0,2,1,0,0,0,0,4],
           [5,3,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,4,0,0,9,0,6,0],
           [0,0,7,8,0,0,0,0,2],
           [0,7,5,0,0,6,2,0,0],
           [0,0,9,0,0,7,0,0,8],
           [0,0,0,0,0,5,0,0,3]]


solve_sudoku(sudoku)
print_sudoku(sudoku)












