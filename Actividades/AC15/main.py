
import re
import requests
import json

texto1 = '''@Para@re4liz4r@t0@esta@p4rt3@part3@parte@usarás
@s4ndw1ch@d3@0p0ll0@la@l4l4@l4nd@API@de@wikipedia.
@Debes@d23@d83@d3bes@creaa4r@crear@tu@prop1a
@propol30@propia@l4nQ@qe3@0jos@d3volc4n@copia
@de@la@31sd2@famosa@fjids87h@página.
@Se@L2q@d3V@llamará@PrograPedia@y@tendrá
@l0gr4r@es0@eS89@Ez1@est0@4@sus@propias
@PrograPaginas@conFDfl3@cre4r@título,@32kf3@contenido,@sdf3@url(a@Wikipedia)@fj98@y@jdsf8@sus@jdfs8@id.
@El@hol444@k3paz4@contenido@c0t3n1d0@debe@d3b3
@3st4r@estar@separa3@separado@por@p0rpo0rpo0r
@s3cc10n@sección@k0n@con@su@respectiva@1nfo
@información.
@Las@l4s@p4gs@p4g1in4s@páginas@solo@t13n3n@od3b3n
@est4r@deben@estar@r3poll0@r3ch1ck3n@en@español'''

texto2 = '''@T.correctau@f.incorrecta1@prog.correctarama
@de.correctabe@de.iccd.re@s.correctaer@cap.correctaaz
@.3fd.coorcta@d.correctae@rec.correctaibir
@casi.correct4@u.correctana@pala.correctabra
@a.correcta@asi.corrcta@bu.correctascar.
@Lu.correctaego@lu.corr.cert@de.correctabe
@d.incorrectaee@most.correctarar@e.correctal
@res.correctaultado@c.corrt3@d.correctae@l.correctaa
@búsq.correctaueda@hol.corrrectaa@e.correctan
@pant.correctaalla@y.correcta@bast.ian@gua.correctardar@s.correctau@ultima.corrc.clase@info.correctarmación,@co.correctamo@
no.correcttttala@Prog.correctaraPágina,@p.correctaara@
pos.correctaterior@bue.correct.no
@us.correctao@d.correctael@qu.procorrect.fd
@pro.correctagrama.'''

texto3 = '''@De.be@est.ar@2EkpAAAzZzaermano@l.a@56@op.ción@
basTiAAAAnCITOHHHXZ@d.e@pode.r@Ae3P0llO@sa.lir@BCtrIangulO@de.l@
FAperRRo@pro.grama@.y.@la.s@4A0papA@página.s@0ojosdeVolCAAAnn@
y.a@cread.as@BGDlospoLLitosdiceNnnn@debe.n@7A2PIOPIO@s.er@
6E3cUandoTienen@gua.rdadas@d329Hd@p.ara@realiza.r@
42cUandoTienen@me.nos@Frio322@req.uests@F7BpOo@e.n@cas.o@
C3P0@d.e@R2D2@y.a@R30b0E32@BKKN12@exi.stir@yMe32sal3@e.n@
n0m4Scl4s3s@l.a@ba.se@no31@d.e@j4j4j4@dato.s'''

'''
Intruciones:

 Para esta parte usarás
 la API de wikipedia.
 Debes crear tu propia copia
 de la famosa página.
 Se llamará PrograPedia y tendrá
 sus propias
 PrograPaginas título, contenido, url(a Wikipedia) y sus id.
 El contenido debe estar separado por sección con su respectiva información.
 Las páginas solo deben estar en español

Tu programa
 debe ser capaz
 de recibir
 una palabra
 a buscar.
 Luego debe
 mostrar el
 resultado de la
 búsqueda en
 pantalla y guardar su información, como PrograPágina, para
posterior uso del programa.

estar la opción de poder salir del programa y las páginas creadas deben ser guardadas para realizar menos requests en caso de ya existir en la base de datos'''

class PrograPedia:
    def __init__(self):
        self.URL = 'https://es.wikipedia.org/w/api.php?'
        self.stop = False
        print('\nBIENVENIDO A PROGRAPEDIA\n')

    def buscar_pagina(self, termino):
        pagina = requests.get(self.URL, params={'action':'query', 'prop':'extracts', 'titles':termino, 'explaintext': '' ,'format':'json'})
        info = pagina.json()['query']['pages'][list(pagina.json()['query']['pages'].keys())[0]]
        url = 'www.es.wikipedia.org/wiki/{}'.format(termino.replace(' ','_'))
        return PrograPagina(info['title'], info['extract'], url , info['pageid'])

    def mostrar_pagina(self, termino):
        encontrado = False
        for pagina in PrograPagina.listado_paginas:
            if pagina.titulo.lower() == termino.lower():
                encontrado = True
                print()
                print(pagina.titulo.upper())
                print()
                print(pagina.contenido)
                print()
        if not encontrado:
            pagina = self.buscar_pagina(termino)
            print()
            print(pagina.titulo.upper())
            print()
            print(pagina.contenido)
            print()

    def salir(self):
        opcion = input('>>> Deseas hacer otra búsqueda? <si> <no> ')
        if opcion == 'no':
            print('Programa cerrado.')
            self.stop = True

    def start(self):
        while not self.stop:
            termino = input('>>> Que deseas buscar: ')
            self.mostrar_pagina(termino)
            self.salir()


class PrograPagina:
    listado_paginas = []
    def __init__(self, titulo, contenido, url, id):
        self.titulo = titulo
        self.contenido = contenido
        self.url = url
        self.id = id
        PrograPagina.listado_paginas.append(self)



def revisar1(palabra):
    for c in palabra:
        if re.match('[0-9]', c):
            return False
    return True


if __name__ == '__main__':
    lista = re.split('\@', texto1)
    nueva_lista = []
    for palabra in lista:
        if revisar1(palabra):
            nueva_lista.append(palabra)
    texto1_arreglado = ' '.join(nueva_lista)

    lista = re.split('\@', texto2)
    nueva_lista = []
    for palabra in lista:
        if '.correcta' in palabra:
            nueva_lista.append(re.sub('\.correcta','',palabra))
    texto2_arreglado = ' '.join(nueva_lista)

    lista = re.split('\@', texto3)
    nueva_lista = []
    for palabra in lista:
        if re.match('([a-z]*[áéíóú]*[a-z]*\.[a-z]*[áéíóú]*[a-z]*)', palabra):
            nueva_lista.append(re.sub('\.','',palabra))
    texto3_arreglado = ' '.join(nueva_lista)

    pp = PrograPedia()
    pp.start()