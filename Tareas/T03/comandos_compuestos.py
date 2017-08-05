
def do_if(consulta_a, consulta_b, consulta_c):
    if consulta_b():
        return consulta_a()
    else:
        return consulta_c()