#!/usr/bin/env python3

import os, sys, getopt
from random import randint, shuffle
from rich.console import Console

'''
Assunzioni e convenzioni:
    - La dimensione della borsa deve essere almeno grande come il massimo numero 
    di lettere da consegnare in un nodo;

    - L'ufficio postale avrà il primo indirizzo libero in cui non bisogna fare consegne

    - Gli indirizzi di consegna saranno i primi
    
    - Percentuali nodi di consegna in base al livello
        # Easy = random 30-50%
        # Medium = 60-70%
        # Hard = 80-90%
        
'''
'''
CHIAMATA TIPO:

python generatore.py -n "easy_5" -i 4 -l "easy"
'''

file_name = ''

num_nodi, ufficio_postale, dim_borsa, max_step, level, ind_cons= None, None, None, None, None, None
archi = []
elenco_lettere = []

console = Console()

# Get command line parameters
try:
    opt = getopt.getopt(sys.argv[1:], 'n:i:l:')
except:
    err()

# Parse command line parameters
for arg, val in opt[0]:
    if arg == '-n':
        file_name = val
    elif arg == '-i':
        try:
            num_nodi = int(val)
            assert(num_nodi > 0)
        except:
            err('Num_nodi must be a positive integer value')
    elif arg == '-l':
        if val == 'easy':
            level = "easy"
            rand = randint(3,5)
            ind_cons = int(num_nodi * (rand / 10))
            ufficio_postale = ind_cons + 1
            max_step = int(num_nodi * 2)
        elif val == 'medium':
            level = "medium"
            rand = randint(6, 7)
            ind_cons = int(num_nodi * (rand/10))
            ufficio_postale = ind_cons + 1
            max_step = int(num_nodi * 2.5)
        elif val == 'hard':
            level = "hard"
            rand = randint(8, 9)
            ind_cons = int(num_nodi * (rand/10))
            ufficio_postale = ind_cons + 1
            max_step = int(num_nodi * 4)
        else:
            err('unsupported level type')



# Generating instances

with console.status('Genero istanza ...', spinner='bouncingBar'):

    #Genere pesi archi
    for i in range (0, num_nodi*num_nodi):
        num = randint(1,25)
        archi.append(num)
    for i in range(0,num_nodi):
        archi[(i*num_nodi) + i] = 0     

    #Genero numero lettere da consegnare
    max_lett = 0

    for i in range(0, num_nodi):
        num = randint(1,20)
        if num > max_lett:
            max_lett = num

        if i < ind_cons:
            elenco_lettere.append(num) #x lettere da consegnare
        else:
            elenco_lettere.append(0) #0 lettere da consegnare
    assert (len(elenco_lettere) == num_nodi)

    #Dimensione borsa
    if level == "easy":
        dim_borsa = max_lett * num_nodi
    elif level == "medium":
        dim_borsa = int(max_lett * 2)
    else:
        dim_borsa = max_lett

    console.log('Istanze generate correttamente!')


# Formattazione Minzinc
def minizinc():
    file = file_name + '.dzn'
    path = os.path.join('data', file)
    with open(path, 'w') as f:

        f.write(f'num_nodi = {num_nodi};\n')
        f.write(f'ufficio_postale = {ufficio_postale};\n')
        f.write(f'dim_borsa = {dim_borsa};\n')
        f.write(f'max_step = {max_step};\n')

        f.write(f'elenco_lettere = [')
        i = 0
        while i < len(elenco_lettere)-1:
            f.write(f'{elenco_lettere[i]}, ')
            i = i + 1
        f.write(f'{elenco_lettere[len(elenco_lettere)-1]}];\n')

        i = 0
        j = 1
        f.write(f'distanze = [')
        while j <= num_nodi:
            f.write(f'|')
            while i < ((num_nodi*j) - 1):
                f.write(f'{archi[i]}, ')
                i = i + 1
            f.write(f'{archi[i]}\n')
            i = i + 1
            j = j + 1
        f.write(f'|];\n')


# Formattazione ASP
def asp():
    file = file_name + '.lp'
    path = os.path.join('data', file)
    with open(path, 'w') as f:
        f.write(f'node(1..{num_nodi}).\n\n')
        f.write(f'ufficio_postale({ufficio_postale}).\n\n')
        f.write(f'dim_borsa({dim_borsa}).\n\n')
        f.write(f'time(1..{max_step}).\n\n')

        i = 1;

        while i <= num_nodi:
            f.write(f'lettere({i},{elenco_lettere[i-1]}).\n')
            i = i + 1

        f.write(f'\n')

        j = 1
        while j <= num_nodi:
            i = 1
            while i <= num_nodi:
                f.write(f'costo_arco({j}, {i}, {archi[(num_nodi*(j-1)) + i - 1]}).\n')
                i = i + 1
            j = j + 1
            f.write(f'\n')

minizinc()
asp()













