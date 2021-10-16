import math
from ortools.linear_solver import pywraplp

sudoku = [[4,0,0,9,0,0,3,0,0],
           [0,0,2,1,0,0,0,0,4],
           [5,3,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0],
           [0,0,4,0,0,9,0,6,0],
           [0,0,7,8,0,0,0,0,2],
           [0,7,5,0,0,6,2,0,0],
           [0,0,9,0,0,7,0,0,8],
           [0,0,0,0,0,5,0,0,3]]

def print_solution(sudoku):
    l = len(sudoku)
    n = int(math.sqrt(l))
    r = l * 2 + 2 * n +1
    for i in range(l):
        if i % n == 0:
            print("-"*r)
        for j in range(l):
            if  j % n == 0:
                print("|", end = " ")
            print(round(sudoku[i][j].solution_value()), end = " ")
            if  j == l-1:
                print("|", end = " ")
        print('')
    print("-" * r)









def zeros(mat):
    dim = len(mat)
    result = 0
    for row in range(dim):
        for col in range(dim):
            if mat[row][col] == 0:
                result +=1
    return result

def rows(mat):
    dim = len(mat)
    for row in mat:
        if len(set(row)) < dim:
            return False
    return True

def columns(mat):
    dim = len(mat)
    for col in range(dim):
        s = set()
        for row in range(dim):
            s.add(mat[row][col])
        if len(s) < dim:
            return False
    return True

def corners(mat):
    dim = len(mat)
    num_corners = int(math.sqrt(dim))
    for i in range(num_corners):
        row = i - i % dim
        for j in range(num_corners):
            col = j - j % dim
            s  = set()
            for r in range(num_corners):
                for c in range(num_corners):
                    s.add(mat[row+r][col+c])
            if len(s) < dim:
                return False
    return True


def sudoku_solver(sudoku):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    dim = len(sudoku)
    mat = [[0 for col in range(dim)] for row in range(dim) ]
    for row in range(dim):
        for col in range(dim):
            if sudoku[row][col] != -1:
                mat[row][col] = solver.IntVar(1,9,'grid %x %x' % (row, col))





    solver.Add(rows(mat))
    solver.Add(columns(mat))
    solver.Add(corners(mat))
    solver.Minimize(zeros(mat))

    status = solver.Solve()

    print_solution(mat)

sudoku_solver(sudoku)








