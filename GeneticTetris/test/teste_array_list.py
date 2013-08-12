import time
import array
import random

def tlist(b, x, y, n):
    t1 = time.clock()

    for n in xrange(n):
        for j in range(y):
            for i in range(x):
                w = b[j][i]

    t2 = time.clock()
    print "0 - List[y][x]: ", round(t2-t1, 3)
    return t2-t1

def tlist2(b, x, y, n):
    t1 = time.clock()

    for n in xrange(n):
        for j in xrange(y):
            for i in xrange(x):
                w = b[j][i]

    t2 = time.clock()
    print "1 - List[y][x] + xrange: ", round(t2-t1, 3)
    return t2-t1

def tlist3(b, x, y, n):
    t1 = time.clock()

    for n in xrange(n):
        for i in xrange(x):
            for j in xrange(y):
                w = b[j][i]

    t2 = time.clock()
    print "2 - List[y][x] + xrange + x->y: ", round(t2-t1, 3)
    return t2-t1

def tlist4(b, x, y, n):
    t1 = time.clock()

    for n in xrange(n):
        for j in xrange(y):
                w = min(b[j])

    t2 = time.clock()
    print "3 - List[y][x] + min (line scan) + xrange: ", round(t2-t1, 3)
    return t2-t1

def tlist5(b, x, y, n):
    t1 = time.clock()

    for n in xrange(n):
        for j in b:
            for i in j:
                w = i

    t2 = time.clock()
    print "4 - List in [y] in [x]: ", round(t2-t1, 3)
    return t2-t1

def tlist6(b, x, y, n):
    t1 = time.clock()

    for n in xrange(n):
        for j in xrange(y):
            lineFull = True
            for i in xrange(x):
                w = b[i][j]
                if w == 0:
                    lineFull = False
                    break
            if lineFull:
                pass
            else:
                pass

    t2 = time.clock()
    print "5 - List[x][y] + (line scan) + xrange: ", round(t2-t1, 3)
    return t2-t1

def tarray(b, x, y, n):
    t1 = time.clock()

    for n in xrange(n):
        for i in xrange(x*y):
            w = b[i]

    t2 = time.clock()
    print "6 - Array[i] + xrange: ", round(t2-t1, 3)
    return t2-t1

def tarray2(b, x, y, n):
    t1 = time.clock()

    for n in xrange(n):
        for j in xrange(y):
            for i in xrange(x):
                w = b[i*j]

    t2 = time.clock()
    print "7 - Array[i*j] + xrange: ", round(t2-t1, 3)
    return t2-t1

def perform(x, y, n, s):
    b = [[random.randint(0,7) for col in xrange(x)] for row in xrange(y)]
    #b = [[0 for col in xrange(x)] for row in xrange(y)]
    s[0] += tlist(b, x, y, n)
    s[1] += tlist2(b, x, y, n)
    s[2] += tlist3(b, x, y, n)
    s[3] += tlist4(b, x, y, n)
    s[4] += tlist5(b, x, y, n)

    b2 = [[b[row][col] for row in xrange(y)] for col in xrange(x)]
    s[5] += tlist6(b2, x, y, n)

    b1 = []
    for i in xrange(x):
        for j in xrange(y):
            b1.append(b[j][i])
    b3 = array.array('B', b1)
    s[6] += tarray(b3, x, y, n)
    s[7] += tarray2(b3, x, y, n)

s = [0.0 for i in xrange(10)]
t = 1
for i in xrange(t):
    perform(10, 20, 100000, s)
    
for i in xrange(len(s)):
    print "media teste ", i, " = ", (s[i] / t)
    