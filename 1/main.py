import math
import random
from ortools.linear_solver import pywraplp

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
projetos[1] = (1,[1,2],1)
#projetos[2] = (4,[5],1)
#projetos[3] = (3,[5,2],1)


availabiliy = {}
availabiliy[1] = [(a,b) for a in range(1,6) for b in range(1,5)]
availabiliy[2] = [(a,b) for a in range(1,6) for b in range(1,5)]
#availabiliy[2] = [(a,b) for a in range(1,6) for b in range(2,6)]
#availabiliy[3] = [(a,b) for a in range(1,6) for b in range(3,7)]
#availabiliy[4] = [(a,b) for a in range(1,6) for b in range(4,8)]
#availabiliy[5] = [(a,b) for a in range(1,6) for b in range(4,8)]
num_rooms = 1
num_days = 5
num_slots = 8
num_projetos = len(projetos)
num_employes = len(availabiliy)
solver = pywraplp.Solver.CreateSolver('SCIP')

schedule = {}
reunions = {}
rooms = {}

#definir dicionarios de horarios e inicializar
for employe in range(1,num_employes+1):
    for project in range(1,num_projetos+1):
            for day in range(1,num_days+1):
                for slot in range(1,num_slots+1):
                    schedule[(employe,project,day,slot)] = solver.BoolVar('%i%i%i%i' % (employe,project,day,slot))
                    if (employe not in projetos[project][1] and employe != projetos[project][0]) or (day,slot) not in availabiliy[employe]:
                        solver.Add(schedule[(employe,project,day,slot)] == 0)

#definir dicionarios de salas em que cada sala so pode ter um projeto num dia e hora
for room in range(1, num_rooms+1):
    for day in range(1, num_days+1):
        for slot in range(1, num_slots+1):
            acc = []
            for project in range(1, num_projetos+1):
                rooms[(room,day,slot,project)] = solver.BoolVar('%i%i%i%i' % (room,day,slot, project))
                acc.append(rooms[(room,day,slot,project)])
            solver.Add(solver.Sum(acc) <= 1)


#definir dicionarios de reunioes e cada uma so pode ocorrer numa sala
for day in range(1,num_days+1):
    for slot in range(1,num_slots+1):
        for room in range(1,num_rooms+1):
            acc = []
            for project in range(1,num_projetos+1):
                reunions[(day,slot, room, project)] = solver.BoolVar("%i%i%i%i" % (day, slot, room, project))
                acc.append(reunions[(day,slot,room,project)])
            solver.Add(solver.Sum(acc) <= 1)

#definir numero de reunioes semanais
for project in range(1, num_projetos+1):
    acc = []
    for day in range(1, num_days+1):
        for slot in range(1, num_slots+1):
            for room in range(1, num_rooms+1):
                acc.append(reunions[(day,slot,room,project)])
    solver.Add(solver.Sum(acc) == projetos[project][2])

#quorum minimo de 50%
for project in range(1, num_projetos):
    for day in range(1, num_days):
        for slot in range(1, num_slots):
            acc = []
            for employe in range(1, num_employes +1):
                acc.append(schedule[(employe,project,day,slot)])
            solver.Add(solver.Sum(acc) >= sum(projetos[project][1]) //2)

#reuniao so com o lider
for project in projetos:
    leader = projetos[project][0]
    colaborators = projetos[project][1]
    leader_avilability = availabiliy[leader]
    for day in range(1, num_days+1):
        for slot in range(1, num_slots+1):
            if(day,slot) not in leader_avilability:
                for employe in colaborators:
                    solver.Add(schedule[(employe,project,day,slot)] == 0)
                for room in range(1, num_rooms+1):
                    solver.Add(rooms[(room,day,slot,project)] == 0)
                    solver.Add(reunions[(day, slot,room, project)] == 0)





status = solver.Solve()



















