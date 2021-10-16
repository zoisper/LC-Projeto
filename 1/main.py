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

def print_solution(sudoku, dim):
    n = int(math.sqrt(dim))
    r = dim * 2 + 2 * n +1
    for i in range(dim):
        if i % n == 0:
            print("-"*r)
        for j in range(dim):
            if  j % n == 0:
                print("|", end = " ")
            for k in range(dim):
                if sudoku[(i,j,k)].solution_value() == 1:
                    print(k+1, end = " ")
            if  j == dim-1:
                print("|", end = " ")
        print('')
    print("-" * r)


def sudoku_solver(sudoku):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    dim = len(sudoku)
    num_corners = int(math.sqrt(dim))
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
        corner_y = i - i % num_corners
        for j in range(dim):
            corner_x = j - j % num_corners
            for depth in range(dim):
                val = []
                for row in range(num_corners):
                    for col in range(num_corners):
                        val.append(cube[corner_y + row, corner_x + col, depth])
                solver.Add(solver.Sum(val) == 1)

    for i in range(dim):
        for j in range(dim):
            if sudoku[i][j] != 0:
                solver.Add(cube[(i,j,sudoku[i][j]-1)] == 1)



    status = solver.Solve()
    print_solution(cube,dim)


sudoku_solver(sudoku)








