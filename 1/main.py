import math
import random
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

def sudoku_printer(sudoku):
    l = len(sudoku)
    n = int(math.sqrt(l))
    pad = 1 + l // 10
    r = (l + n) * (pad + 1)  +1
    for i in range(l):
        if i % n == 0:
            print("-"*r)
        for j in range(l):
            if  j % n == 0:
                print("|".ljust(pad), end = " ")
            print(f'{sudoku[i][j]}'.ljust(pad), end = " ")
            if  j == l-1:
                print("|".ljust(pad), end = " ")
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

def sudoku_generetor(N, alpha):
    dim = N*N
    filled = int(dim * dim * alpha)
    mat = [[0 for a in range(dim)] for a in range(dim)]
    while(filled > 0):
        row = random.randint(0,dim-1)
        col = random.randint(0,dim-1)
        number = random.randint(1, dim - 1)
        while(mat[row][col] != 0 or not check(mat,row,col,number)):
            row = random.randint(0, dim-1)
            col = random.randint(0, dim-1)
            number = random.randint(1,dim-1)
        mat[row][col] = number
        filled -=1

    return mat

def converter(cube,dim):
    mat = [[0 for a in range(dim)] for b in range(dim) ]
    for row in range(dim):
        for col in range(dim):
            for depth in range(dim):
                if cube[(row,col,depth)].solution_value() == 1:
                    mat[row][col] = depth + 1
    return mat



def sudoku_solver(sudoku):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    dim = len(sudoku)
    num_squares = int(math.sqrt(dim))
    cube = {}

    for row in range(dim):
        for col in range(dim):
            for depth in range(dim):
                cube[(row,col,depth)] = solver.BoolVar('%i%i%i' % (row,col,depth))


    for row in range(dim):
        for col in range(dim):
            val = []
            for depth in range(dim):
                val.append(cube[(row,col,depth)])
            solver.Add(solver.Sum(val) == 1)

    for row in range(dim):
        for depth in range(dim):
            val = []
            for col in range(dim):
                val.append(cube[(row,col,depth)])
            solver.Add(solver.Sum(val) == 1)

    for depth in range(dim):
        for col in range(dim):
            val = []
            for row in range(dim):
                val.append(cube[(row, col, depth)])
            solver.Add(solver.Sum(val) == 1)

    for i in range(dim):
        corner_y = i - i % num_squares
        for j in range(dim):
            corner_x = j - j % num_squares
            for depth in range(dim):
                val = []
                for row in range(num_squares):
                    for col in range(num_squares):
                        val.append(cube[corner_y + row, corner_x + col, depth])
                solver.Add(solver.Sum(val) == 1)

    for i in range(dim):
        for j in range(dim):
            if sudoku[i][j] != 0:
                solver.Add(cube[(i,j,sudoku[i][j]-1)] == 1)


    status = solver.Solve()
    mat = converter(cube, dim)
    if status == pywraplp.Solver.OPTIMAL:
        sudoku_printer(mat)
    else:
        print("Sem Solução")






sudoku = sudoku_generetor(3,0.2)

sudoku_printer(sudoku)

sudoku_solver(sudoku)



'''
def sudoku_generetor(N, alpha):
    dim = N*N
    filled = int(dim * dim * alpha)
    num_frequence = filled // 9
    num_squares = int(math.sqrt(dim))
    solver = pywraplp.Solver.CreateSolver('SCIP')
    cube = {}

    for row in range(dim):
        for col in range(dim):
            for depth in range(dim):
                cube[(row, col, depth)] = solver.BoolVar('%i%i%i' % (row, col, depth))

    for row in range(dim):
        for col in range(dim):
            val = []
            for depth in range(dim):
                val.append(cube[(row,col,depth)])
            solver.Add(solver.Sum(val) <= 1)

    for row in range(dim):
        for depth in range(dim):
            val = []
            for col in range(dim):
                val.append(cube[(row,col,depth)])
            solver.Add(solver.Sum(val) <= 1)

    for depth in range(dim):
        for col in range(dim):
            val = []
            for row in range(dim):
                val.append(cube[(row, col, depth)])
            solver.Add(solver.Sum(val) <= 1)

    for i in range(dim):
        corner_y = i - i % num_squares
        for j in range(dim):
            corner_x = j - j % num_squares
            for depth in range(dim):
                val = []
                for row in range(num_squares):
                    for col in range(num_squares):
                        val.append(cube[corner_y + row, corner_x + col, depth])
                solver.Add(solver.Sum(val) <= 1)

    val = []
    for row in range(dim):
        for col in range(dim):
            for depth in range(dim):
                val.append(cube[(row,col,depth)])
    solver.Add(solver.Sum(val) == filled)

    for depth in range(dim):
        val = []
        for row in range(dim):
            for col in range(dim):
                val.append(cube[(row,col,depth)])
        solver.Add(solver.Sum(val) <= num_frequence + 1)


    solver.Solve()
    mat = converter(cube,dim)
    return mat
'''







