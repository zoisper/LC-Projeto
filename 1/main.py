import math
import random
from ortools.linear_solver import pywraplp
import z3
from z3 import *

''''''
################
###Problema 2###
################
from ortools.linear_solver.pywraplp import Solver

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






#sudoku = sudoku_generetor(3,0.2)

#sudoku_printer(sudoku)

#sudoku_solver(sudoku)

''''''

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

################
###Problema 1###
################

projetos = {}
projetos[1] = (1,[1,2,3],1)
#projetos[2] = (4,[5],1)
#projetos[3] = (3,[5,2],1)


availability = {}
availability[1] = [(a,b) for a in range(1,6) for b in range(1,5)]
availability[2] = [(a,b) for a in range(1,6) for b in range(1,5)]
#availability[2] = [(a,b) for a in range(1,6) for b in range(2,6)]
availability[3] = [(a,b) for a in range(1,6) for b in range(1,5)]
#availability[4] = [(a,b) for a in range(1,6) for b in range(4,8)]
#availability[5] = [(a,b) for a in range(1,6) for b in range(4,8)]

num_rooms = 1
num_days = 5
num_slots = 8
num_projetos = len(projetos)
num_employes = len(availability)






rooms = [x for x in range(1,num_rooms+1)]
days = [x for x in range(1,num_days+1)]
slots = [x for x in range(1,num_slots+1)]
projects = [x for x in range(1,num_projetos+1)]
employes = [x for x in range(1, num_employes+1)]
leaders = set()
for p in projects:
    leaders.add(projetos[p][0])

rs = pywraplp.Solver.CreateSolver('SCIP')
reunions ={}

#inicializar vairiaveis
for d in days:
    for s in slots:
        for r in rooms:
            for p in projects:
                for e in employes:
                    reunions[(d,s,r,p,e)] = rs.BoolVar('%i%i%i%i%i' %(d,s,r,p,e))

#funcionarios so vao as reunioes que podem
for e in employes:
    for d in days:
        for s in slots:
            if (d,s) not in availability[e]:
                for r in rooms:
                    for p in projects:
                        rs.Add(reunions[(d,s,r,p,e)] == 0)

#funcionarios so nos seus projetos:
for e in employes:
    for p in projects:
        if e not in projetos[p][1]:
            for d in days:
                for s in slots:
                    for r in rooms:
                        rs.Add(reunions[(d,s,r,p,e)] == 0)


#sala so pode ter uma reuniao ao mesmo tempo
for r in rooms:
    for d in days:
        for s in slots:
            rs.Add(sum([reunions[(d,s,r,p,l)] for p in projects for l in leaders]) <=1)

# reuniao so quando ha lider
for d in days:
    for s in slots:
        for r in rooms:
            for p in projects:
                leader = projetos[p][0]
                for e in employes:
                    rs.Add(reunions[d,s,r,p,leader] >= reunions[d,s,r,p,e])

# reuniao com quorum minimo:
for d in days:
    for s in slots:
        for r in rooms:
            for p in projects:
                leader = projetos[p][0]
                quorum = len(projetos[p][1]) /2
                rs.Add(sum([reunions[(d,s,r,p,e)] for e in employes]) >= (reunions[(d,s,r,p,leader)] * quorum))

#numero minimo de reunioes
for p in projects:
    num_reunions = projetos[p][2]
    leader = projetos[p][0]
    rs.Add(sum([reunions[(d,s,r,p,leader)] for d in days for s in slots for r in rooms]) == num_reunions)



status = rs.Solve()
print(status == pywraplp.Solver.OPTIMAL )

for p in projects:
    print(f'Projeto:{p}')
    leader = projetos[p][0]
    for d in days:
        for s in slots:
            for r in rooms:
                if reunions[(d,s,r,p,leader)].solution_value() == 1:
                    print(f'Dia {d} Hora {s} Sala {r}', end=" ")
                    for e in employes:
                        if reunions[(d,s,r,p,e)].solution_value()==1:
                            print(f'E {e}', end=" ")





































