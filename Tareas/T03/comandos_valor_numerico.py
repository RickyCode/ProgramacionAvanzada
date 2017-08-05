
from functools import reduce

def LEN(X):
    return len(X)

def PROM(X):
    suma_total = reduce(lambda x, y: x+y, X)
    return suma_total / len(X)

def DESV(X):
    suma_total = reduce(lambda x,y: x+y, list(map(lambda x: (x-PROM(X))**2, X)))
    return (suma_total/len(X)-1)**(1/2)

def MEDIAN(X):
    X.sort()
    #Si el numero es par:
    if len(X) % 2 == 0:
        return PROM([X[(len(X)//2) - 1], X[len(X)//2]])
    #Si es impar:
    else:
        return X[len(X)//2]

def VAR(X):
    suma_total = reduce(lambda x, y: x + y, list(map(lambda x: (x - PROM(X)) ** 2, X)))
    return (suma_total / len(X) - 1)