import random

def get_heights(board):
    heights = []
    for i in range(10):
        found = False
        for j in range(20):
            if board[i + j * 10] == "#":
                found = True
                heights.append(j)
                break
        if not found:
            heights.append(20)
    return heights

def get_rows(board):
    rows = []
    for i in range(20):
        row = 0
        for j in range(10):
            if board[i * 10 + j] == "#":
                row += 1
        rows.append(row)
    return rows

def place_piece(board, orient, pos, heights, rows):
    high = 20
    top = -1
    for i in range(len(orient)):
        if heights[pos + i] + orient[i][0] - 1 < high:
            high = heights[pos + i] + orient[i][0] - 1
        top = max(top, orient[i][0] + orient[i][1])
    if high - top < 0:
        return ("GAME OVER", -1)
    for y in range(20):
        for x in range(10):
            if x >= pos and x < pos + len(orient) and y <= high - orient[x - pos][0] and y >= high - orient[x - pos][0] - orient[x - pos][1]:
                board = board[:x + y * 10] + "#" + board[x + y * 10 + 1:]
                rows[y] += 1
    clear = 0
    for i in range(20):
        if rows[i] == 10:
            clear += 1
            board = "          " + board[:i * 10] + board[(i + 1) * 10:]
    points = 0
    if clear == 1:
        points = 40
    elif clear == 2:
        points = 100
    elif clear == 3:
        points = 300
    elif clear == 4:
        points = 1200
    return (board, points)

def fitness(strat, board, score):
    res = strat[0] * score
    above = [False, False, False, False, False, False, False, False, False, False]
    well = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    height = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
    holes = 0
    peak = 0
    interior = 0
    deep = 0
    blocks = 0
    diffy = 0
    diff = 0
    for i in range(10):
        for j in range(20):
            if board[j * 10 + i] == "#":
                blocks += 1
                if (i == 0 or board[j * 10 + i - 1] == "#") and (i == 9 or board[j * 10 + i + 1] == "#"):
                    if not above[i]:
                        well[i] += 1
                    if j > 0 and board[j * 10 - 10 + i] == "#":
                        interior += 1
                if not above[i]:
                    height[i] = j
                    above[i] = True
            elif above[i]:
                holes += 1
    for i in range(10):
        deep = max(deep, well[i])
        peak = min(peak, height[i])
        if i != 9:
            if abs(height[i] - height[i + 1]) > diffy:
                diff = diffy
                diffy = abs(height[i] - height[i + 1])
            elif abs(height[i] - height[i + 1]) > diff:
                diff = abs(height[i] - height[i + 1])
    return res + holes * strat[1] + peak * strat[2] + interior * strat[3] + deep * strat[4] + blocks * strat[5] + diff * strat[6]

def breed(s1, s2):
    strat = []
    for i in range(len(s1)):
        if random.randint(0, 1) == 0:
            strat.append(s1[i])
        else:
            strat.append(s2[i])
    return strat

def mutate(strat):
    for i in range(FEATURES):
        if random.uniform(0, 1) < MUTATE_MINI:
            while True:
                val = strat[i] + random.uniform(-ADJUST_VAL, ADJUST_VAL)
                if -1 <= val <= 1:
                    strat[i] = val
                    break

def play_game(strategy):
    board = "                                                                                                                                                                                                        "
    points = 0
    while True:
        heights = get_heights(board)
        rows = get_rows(board)
        best, new, boost = -1000000000, "", 0
        piece = pieces[random.randint(0, 6)]
        for orient in piece:
            for pos in range(11 - len(orient)):
                bored, boo = place_piece(board, orient, pos, heights, rows.copy())
                if boo != -1:
                    fit = fitness(strategy, bored, boo)
                    if fit > best:
                        best = fit
                        new = bored
                        boost = boo
        board = new
        if best == -1000000000:
            break
        points += boost
    return points

def play_print(strategy):
    board = "                                                                                                                                                                                                        "
    points = 0
    while True:
        heights = get_heights(board)
        rows = get_rows(board)
        best, new, boost = -1000000000, "", 0
        piece = pieces[random.randint(0, 6)]
        for orient in piece:
            for pos in range(11 - len(orient)):
                bored, boo = place_piece(board, orient, pos, heights, rows.copy())
                if boo != -1:
                    fit = fitness(strategy, bored, boo)
                    if fit > best:
                        best = fit
                        new = bored
                        boost = boo
        if best == -1000000000:
            break
        board = new
        points += boost
        print_board(board)
        print("Current score:", points)

def print_board(board):
    print("=======================")
    for count in range(20):
        print(' '.join(list(("|" + board[count * 10: (count + 1) * 10] + "|"))), " ", count)
    print("=======================")
    print()
    print("  0 1 2 3 4 5 6 7 8 9  ")
    print()

pieces = [[[(0, 0), (0, 1), (0, 0)], [(1, 0), (0, 2)], [(1, 0), (0, 1), (1, 0)], [(0, 2), (1, 0)]], [[(0, 0), (0, 0), (0, 1)], [(2, 0), (0, 2)], [(0, 1), (1, 0), (1, 0)], [(0, 2), (0, 0)]], [[(0, 1), (0, 0), (0, 0)], [(0, 2), (2, 0)], [(1, 0), (1, 0), (0, 1)], [(0, 0), (0, 2)]], [[(0, 3)], [(0, 0), (0, 0), (0, 0), (0, 0)]], [[(0, 0), (0, 1), (1, 0)], [(1, 1), (0, 1)]], [[(1, 0), (0, 1), (0, 0)], [(0, 1), (1, 1)]], [[(0, 1), (0, 1)]]]

POP_SIZE = 500
FEATURES = 7
NUM_CLONES = 50
TOUR_SIZE = 30
TOUR_WIN_PROB = .8
MUTATE_RATE = .1
MUTATE_MINI = .25
ADJUST_VAL = 0.1

file = open("tetrisout.txt", "w+")

print("(N)ew process, or (L)oad saved process? ", end = "")
choice = input()

pop = []
if choice == "L":
    print("What is the file name? ", end = "")
    file = open(input(), "r")
    for i in range(POP_SIZE):
        line = file.readline().split()
        pop.append((-1, []))
        for j in range(FEATURES):
            pop[i][1].append(float(line[j]))
        pop[i] = (float(line[FEATURES]), pop[i][1])
    gen = int(file.readline())
    print("Generation:", str(gen))
    print("Best strategy so far:", pop[0][1])
else:
    for i in range(POP_SIZE):
        pop.append((-1, []))
        for j in range(FEATURES):
            pop[i][1].append(random.uniform(-1, 1))
    choice = "C"
    gen = 0

while True:
    if choice == "P":
        play_print(pop[0][1])
    elif choice == "L":
        pass
    else:
        sum = 0
        poppy = pop.copy()
        pop = []
        for ind, s in enumerate(poppy):
            print("Evaluating strategy number", ind, "--> ", end = "")
            if s[0] == -1:
                total = 0
                for i in range(5):
                    total += play_game(s[1])
                pop.append((total / 5, s[1].copy()))
            else:
                pop.append((s[0], s[1].copy()))
            print(pop[ind][0])
            sum += pop[ind][0]
        pop.sort(reverse = True)
        print("Average:", sum / POP_SIZE)
        print("Generation:", gen)
        print("Best strategy so far:", pop[0][1])
    print("(P)lay a game with current best strategy, (S)ave current process, or (C)ontinue? ", end = "")
    choice = input()
    if choice == "S":
        print("What filename? ", end = "")
        file = open(input(), "w+")
        for entry in pop:
            for val in entry[1]:
                file.write(str(val) + " ")
            file.write(str(entry[0]) + "\n")
        file.write(str(gen))
        break
    elif choice == "C":
        next = []
        for i in range(NUM_CLONES):
            next.append(pop[i])
        while len(next) < POP_SIZE:
            group = random.sample(pop, 2 * TOUR_SIZE)
            side1, side2 = group[:20], group[20:40]
            side1.sort(reverse = True)
            side2.sort(reverse = True)
            for i in range(20):
                if random.uniform(0, 1) < TOUR_WIN_PROB:
                    p1 = side1[i][1]
                    break
            for i in range(20):
                if random.uniform(0, 1) < TOUR_WIN_PROB:
                    p2 = side2[i][1]
                    break
            child = breed(p1, p2)
            next.append((-1, child))
        for i in range(NUM_CLONES, POP_SIZE):
            if random.uniform(0, 1) < MUTATE_RATE:
                mutate(next[i][1])
                next[i] = (-1, next[i][1])
            pop[i] = next[i]
        gen += 1