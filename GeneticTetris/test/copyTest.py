#http://stackoverflow.com/questions/1410615/copy-deepcopy-vs-pickle
import copy
import pickle
import cPickle
import random
import TetrisBoard

b = TetrisBoard.TetrisBoard(22, 10)
d = b.getData()
for i in xrange(22):
    for j in xrange(10):
        d[i][j] = random.randint(0,7)

def copy1():
    return copy.deepcopy(b)

def copy2():
    return pickle.loads(pickle.dumps(b, -1))

def copy3():
    return cPickle.loads(cPickle.dumps(b, -1))

def travel(d):
    n = 0
    for i in d:
        for j in i:
            if j == 0:
                n += 1
    return n
#===============================================================================
if __name__ == '__main__':
    from timeit import Timer
    t = Timer("copyTest.copy1()", "import copyTest")
    print "deepcopy: ", t.timeit(1000)
    t = Timer("copyTest.copy2()", "import copyTest")
    print "pickle:   ", t.timeit(1000)
    t = Timer("copyTest.copy3()", "import copyTest")
    print "cPickle:  ", t.timeit(1000)
#===============================================================================