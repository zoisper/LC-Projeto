import math
import random
from ortools.linear_solver import pywraplp

################
###Problema 2###
################

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
projetos[1] = (1,[2,3],1)
projetos[2] = (4,[5],1)
#projetos[3] = (3,[5,2],1)


availabiliy = {}
availabiliy[1] = [(a,b) for a in range(1,8) for b in range(1,5)]
availabiliy[2] = [(a,b) for a in range(1,8) for b in range(2,6)]
availabiliy[3] = [(a,b) for a in range(1,8) for b in range(3,7)]
availabiliy[4] = [(a,b) for a in range(1,8) for b in range(4,8)]
#availabiliy[5] = [(a,b) for a in range(1,8) for b in range(4,8)]
num_rooms = 3
num_days = 7
num_slots = 8
num_projetos = len(projetos)
num_employes = len(availabiliy)
solver = pywraplp.Solver.CreateSolver('SCIP')

schedule = {}


for day in range(1,num_days+1):
    for slot in range(1,num_slots+1):
        for room in range(1,num_rooms+1):
            for project in range(1,num_projetos+1):
                for employe in range(1,num_employes+1):
                    schedule[(day,slot,room,project, employe)] = solver.BoolVar('%i%i%i%i%i' % (day,slot,room,project, employe))

#colaborador so pode ir no seu horario e nos seus projetos
for employe in range(1,num_employes+1):
    for project in range(1,num_projetos+1):
        for day in range(1,num_days+1):
            for slot in range(1,num_slots+1):
                if (employe not in projetos[project][1] and employe != projetos[project][0]) or (day,slot) not in availabiliy[employe]:
                    for room in range(1,num_rooms+1):
                        solver.Add(schedule[(day,slot,room,project,employe)] == 0)
                        print(f'E{employe},P{project},D{day},S{slot}')

reunions = {}


for day in range(1,num_days+1):
    for slot in range(1,num_slots+1):
        for room in range(1,num_rooms+1):
            for project in range(1,num_projetos+1):
                reunions[(day,slot, room, project)] = solver.BoolVar("%i%i%i%i" % (day, slot, room, project))



# uma unica reuniao por sala no mesmo dia e hora
for day in range(1,num_days+1):
    for slot in range(1,num_slots+1):
        for room in range(1,num_rooms+1):
            solver.Add(solver.Sum(reunions[(day,slot,room, project)] for project in range(1,num_projetos+1)) == 1)

# numero de reunioes semanais
for project in range(1,num_projetos+1):
    solver.Add(solver.Sum(reunions[(day,slot,room, project)] for day in range(1,num_days+1) for slot in range(1, num_slots+1) for room in range(1, num_projetos+1)) == projetos[project][2])

# reuniao so quando o lider presente
for project in range(1, num_projetos+1):
    for day in range(1, num_days+1):
        for slot in range(1, num_slots+1):
            leader = projetos[project][0]
            if (day,slot) not in availabiliy[leader]:
                for room in range(1, num_rooms+1):
                    solver.Add(reunions[(day,slot,room,project)] == 0)

# renuniao so quando quorum de 50%
for project in range(1, num_projetos+1):
    for day in range(1, num_days+1):
        for slot in range(1, num_slots+1):
            for room in range(1, num_rooms + 1):
                if solver.Sum(schedule[(day,slot,room,project,employe)] for employe in range(1, num_employes+1)) <= (1+sum(projetos[project][1])) // 2:
                    solver.Add(reunions[day,slot,room,project] == 0)

# colaborador so vai quando ha reuniao
for employe in range(1, num_employes+1):
    for project in range(1, num_projetos+1):
        for day in range(1, num_days+1):
            for slot in range(1, num_slots+1):
                    if solver.Sum(reunions[(day,slot,room,project)] for room in range(1, num_rooms+1)) == 0:
                        for room in range(1, num_rooms + 1):
                            solver.Add(schedule[(day,slot,room,project,employe)] == 0 )


solver.Solve()

#imprimir resultado
for day in range(1,num_days+1):
    print(f'Dia {day}', end=" ")
    for slot in range(1,num_slots+1):
        print(f'Hora {slot}', end=" ")
        for room in range(1,num_rooms+1):
            print(f'Sala {room}', end=" ")
            for project in range(1,num_projetos+1):
                if reunions[(day, slot, room, project)].solution_value() == 1:
                    print(f'Projeto {project} Colaboradores:', end=" ")
                    for employe in range(1, num_employes+1):
                        if schedule[(day,slot,room,project,employe)].solution_value() == 1:
                            print(employe, end=" ")


    print("")










