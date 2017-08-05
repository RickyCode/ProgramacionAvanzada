
from math import pi, e, factorial

def normal(mi, sigma, x):
    if sigma <= 0:
        pass #Debe generar un error
    else:
        div1 = (1/(((2*pi*(sigma**2))**(1/2))))
        exponente = (-1/2)*(((x - mi)/sigma)**2)
        return div1*(e**exponente)

def exponencial(ni, x):
    if (ni <= 0) or (x < 0):
        pass #Debe levantar ERROR
    else:
        return ni*(e**(-ni*x))

def gamma(ni, k, x):
    if x < 0:
        pass #Debe levantar ERROR
    else:
        mul1 = ((ni**k)/factorial(k-1))
        mul2 = x**(k-1)
        mul3 = e**(-ni*x)
        return mul1 * mul2 * mul3
