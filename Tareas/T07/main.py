__author__ = 'Ricardo Del Rio'

import flask
import json
import sys
from datetime import datetime as dt
# IMPORTS PROPIOS:
from loggers import MyLogger
from eventos import EventoTelegram, EventoGit, Evento

# --------------------------------------------------------------------------------------------------------------- LOGERS

log_i = MyLogger(__name__, name='SERVIDOR',
                 formatter='%(name)s[{0}]:   %(message)s'.format(__name__))
log_w = MyLogger(__name__, name='SERVIDOR',
                 nombre_archivo='servidor.log', stream_handler=False,
                 mylevel='warning')
log_e = MyLogger(__name__, name='SERVIDOR',
                 nombre_archivo='servidor.log', stream_handler=False,
                 mylevel='error')
log_d = MyLogger(__name__, name='SERVIDOR',
                 nombre_archivo='servidor.log', stream_handler=False,
                 mylevel='debug')
space = MyLogger(__name__, formatter='%(message)s')

# ------------------------------------------------------------------------------------------------------------- PROGRAMA

app = flask.Flask(__name__)

# -------------------------------------------------------- SECCIONES

@app.route('/')
def principal():
    texto = '<h1>Pagina principal!</h1><br/>Ultimos eventos:<br />'
    if Evento.lista_eventos:
        Evento.lista_eventos.sort(reverse=True)
        for evento in Evento.lista_eventos:
            texto += '<br />{}'.format(str(evento))
    else:
        texto += '<br />NO ha ocurrido ningun evento'
    return texto

@app.route('/recibir_de_git', methods=['POST'])
def recibir_git():
    recibido = flask.request.json
    print(type(flask.request.json))
    print(type(json.dumps(flask.request.json)))
    EventoGit(recibido)
    EventoGit.ultimo_recibido = json.dumps(recibido, indent=4, sort_keys=True)
    return 'Se recibio la informacion!'

@app.route('/recibir_telegram/<token>', methods=['POST'])
def recibir_telegram(token):
    print(token)
    recibido = flask.request.json
    EventoTelegram(recibido)
    EventoTelegram.ultimo_recibido = json.dumps(recibido, indent=4, sort_keys=True)
    return 'Se recibio la informacion!'


@app.route('/ultimo_git')
def ultimo_git():
    return EventoGit.ultimo_recibido

@app.route('/ultimo_telegram')
def ultimo_telegram():
    return EventoTelegram.ultimo_recibido

if __name__ == '__main__':
    app.run(port=8080)