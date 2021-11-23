import random

lista_rizou =  [0, 2, 4, 6, 14, 20, 28, 30, 32, 34, 42, 56, 70]  #Λίστα με τα index των μαύρων boxes
'''
#_#_#_#
_______
#_____#
_______
#_#_#_#
_______
#______
_______
#______
_______
#______
'''
lista_Karabos = [0, 12, 14, 24, 28, 36, 42, 52, 56, 68, 70]
'''
#______
_____#_
#______
___#___
#______
_#_____
#______
___#___
#______
_____#_
#______
'''
x = input(str('Choose between Rizos and Karampoikis.\n Type R to check Rizos or K to check Karampoikis: '))       #Επιλογή γράμματος παίρνει μονο τα Κ και Ρ, ανεξαρτήτως αν είναι κεφαλαία ή μικρά.
while(x.upper() != 'R' and x.upper() != 'K'):
    print(x)
    x = input(str('Choose between Rizos and Karampoikis.\n Type R to check Rizos or K to check Karampoikis:'))
if x.upper() == 'R':
    END_GRID = lista_rizou
    percent = 10/14
else:
    END_GRID = lista_Karabos
    percent = 10/12

STARTING_POOL = 100


#evaluation function
def eval_fun(rg, g):            #Καλείται για να αποδόση βαθμολογία σε κάθε grid, επί της ουσίας συγκρίνει να δεί αν τα indexes βρίσκονται στις σωστές θέσει
    tmp_rg = rg.copy()
    result = 1
    for i in g:
        if i in tmp_rg:
            result += 1
            tmp_rg.remove(i)

    return result/(len(rg) +1 )

#Explanatory function          Καλείται όταν βρεθεί καλή λύση και εκτυπώνει πράγματα για το grid που βρήκε
def the_end(rg,g):
    tmp_rg = rg.copy()
    result = 1
    for i in g:
        if i in tmp_rg:
            result += 1
            tmp_rg.remove(i)
    print('Result is:',result,', at ', len(rg) +1)

#Gnerate grid function        Καλείται για να δημιουργήσει grid. Αυτό επιτυγχάνεται καλώντας 12 ή 14 ανάλογα με το END GRID εντελώς τυχαία νούμερα που θα είναι μεταξύ τους διαφορετικά
def generate_grid():
    grid = list()
    list_of_nums = list()
    for i in range(len(END_GRID)):
        num = random.randint(0,76)
        while(num in list_of_nums):
            num = random.randint(0,76)
        list_of_nums.append(num)
        grid.append(num)
    grid.sort()
    return grid

#geneating random genetic pool  Καλείται για να δημιουργήσει τον αρχικό μας πληθυσμό. Κάθε Pool έχει 100 (STARTING POOL) grid
# και έναν αριθμό που αργότερα θα αναπαριστά το eval_func
def generate_pool(pool_size):
    pool = []
    for g in range(0, pool_size):
        grid = generate_grid()
        pool.append([grid, 0])
    return pool



#generates the roulette for each stage  Επίσης κάνει σόρτ και ύστερα στο pool αλλάζει το eval func με το ποσοστό των επιτυχώμενων καταστάσεων του grid ανά την βαθμολογία των συνολικών grids
def roulette_generator(rg ,pool):
    sum = 0
    for elem in pool:
        elem[1] = eval_fun(rg ,elem[0])
        if(elem[1]!=0):
            sum += elem[1]

    for elem in pool:
        if elem[1]!=0:
            elem[1] /= sum

    pool.sort(key = lambda elem: elem[1], reverse = True)
    total = 0
    tmp = 0
    for elem in pool:
        tmp = elem[1]
        elem[1] = elem[1] + total
        total += tmp


#Choose Parents Function            Επιλέγει γονείς και τους βγάζει από το pool
def chooseParents(rg, pool): 
    pair = [0, 0]
    for i in range(0, 2):
        roulette_generator(rg, pool)
        #choose parent i
        point = random.uniform(0, 1)
        for elem in pool:
            if( point <= elem[1]):
                pair[i] = elem
                pool.remove(elem)
                break
    return pair


#Mating Parents Function            Κάνει Crossovers τους γονείς και δημιουργεί δύο παιδιά
def mateParents(pair):
    children = [pair[0], pair[1]]
    point = random.randint(1,11)
    for i in range(point, len(END_GRID)):
        children[0][0][i] = pair[1][0][i]
        children[1][0][i] = pair[0][0][i]
    children[0][0].sort()
    children[1][0].sort()
    return children

#Nice Print Function                Εκτυπώνει με ωραίο τρόπο την λίστα μας
def nice_print(grid):
    print('-'*50)
    s = ''
    for i in range(1, 78):
        if i-1 in grid[0]:
            s+='#'
        else: 
            s+='_'
        if i%7 ==0:
            print(s)
            s = ''
    print(grid[0])


#isDone Function            Ελέγχει αν βρέθηκε αρκετά καλή λύση
def isDone(rg,g):
    e = eval_fun(END_GRID, pool[0][0])
    if( e >= percent ):
        print('Current best')
        nice_print(pool[0])
        the_end(END_GRID,pool[0][0])
        return True
    return False


#STARTING PROGRAMM
random.seed(a = None, version = 2)          #Επιλέγω εντελώς τυχαίο seed
pool = generate_pool(STARTING_POOL)         #Φτιάχνω τον αρχαίο πληθυσμό
i = 0
to_change = int(STARTING_POOL / 5)          #Μεταβλητή όπου θα αλλάζει τα to_change χειρότερα grids με καινούριο τυχαία 
while(True):
    tmp = []
    roulette_generator(END_GRID, pool)
    if(isDone(END_GRID, pool[0][0])):
        break
    for j in range(0, int(STARTING_POOL/2)):
        pair = chooseParents(END_GRID, pool)
        children = mateParents(pair)
        tmp.append(children[0])
        tmp.append(children[1])
    pool = tmp.copy()
    roulette_generator(END_GRID, pool)
    if(isDone(END_GRID, pool[0][0])):
        break
    if(i % 10 == 0):                            #Κάθε 10 φορές θα χρησιμοποιεί την to change να αλλάξει τα to change χειρότερα δείγματα
        for j in range(0, to_change):
            g = generate_grid()
            pool[STARTING_POOL -j -1][0] = g.copy()
    if(isDone(END_GRID, pool[0][0])):
        break
    i += 1

