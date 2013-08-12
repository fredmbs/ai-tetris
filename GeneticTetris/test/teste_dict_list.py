import time
import random

def nulo():
    a = 10
    b = a
    a = b

def teste1(b, n):
    t1 = time.clock()
    
    for t in xrange(n):
        for i in b:
            i()

    t2 = time.clock()
    print "0 - List: ", round(t2-t1, 3)
    return t2-t1
        
def teste2(b, n):
    t1 = time.clock()
    
    for t in xrange(n):
        for i in b.values():
            i()
            
    t2 = time.clock()
    print "1 - Dict: ", round(t2-t1, 3)
    return t2-t1
        
def teste3(b, n):
    t1 = time.clock()
    
    for t in xrange(n):
        for i in b.viewvalues():
            i()
            
    t2 = time.clock()
    print "2 - Dict - View: ", round(t2-t1, 3)
    return t2-t1
        
def perform(s, e, n):
    bl = [nulo for i in xrange(e)]
    #b = [[0 for col in xrange(x)] for row in xrange(y)]
    s[0] += teste1(bl, n)
    
    bd = {}
    for i in xrange(e):
        bd[i] = nulo
        
    s[1] += teste2(bd, n)
    s[2] += teste3(bd, n)

s = [0 for i in xrange(3)]
t = 100
for i in xrange(t):
    perform(s, 10, 100000)
    
for i in xrange(len(s)):
    print "media teste ", i, " = ", (s[i] / t)
    