__author__ = 'Ricado Del Río'

from loggers import MyLogger
from interprete import InterpreteTelegram
from requests import post
import json
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


class Evento:
    interprete = InterpreteTelegram()
    lista_eventos = []
    def __init__(self):
        self.numero = next(num_evento)
        self.__texto = ''

    @property
    def texto(self):
        if not self.__texto:
            self.__texto = '<br />{}'.format('-' * 80)
            for atr in self.__dict__.items():
                if atr[0] != '_Evento__texto':
                    self.__texto += '<br />{}: {}'.format(atr[0], atr[1])
        return self.__texto

    def __str__(self):
        return self.texto

    def __eq__(self, other):
        return self.numero == other.numero

    def __lt__(self, other):
        return self.numero < other.numero

class EventoGit(Evento):
    ultimo_recibido = 'Nada por aqui'
    def __init__(self, dic):
        Evento.__init__(self)
        self.autor_issue = dic['issue']['user']['login'].strip()
        self.num_issue = dic['issue']['number']
        self.titulo_issue = dic['issue']['title'].strip()
        self.link_issue = dic['issue']['url'].strip()

        if (dic['action'] == 'created'):
            self.texto_comentario = dic['comment']['body'].strip()
        elif (dic['action'] == 'opened'):
            self.texto_comentario = 'Se creó un nuevo issue.'
        else:
            self.texto_comentario = '--'

        self.texto_telegram = '[{0}]\n[#{1} - {2}]\n{3}\n[Link: {4}]'.format(self.autor_issue, self.num_issue,
                                                                            self.titulo_issue, self.texto_comentario,
                                                                            self.link_issue)
        Evento.lista_eventos.append(self)
        if dic['action'] == 'opened':
            self.issue_abierta_telegram()

    def issue_abierta_telegram(self):
        url = 'https://api.telegram.org/bot433706040:AAEfwDtNVHctRQUnpxmHWhEBBBuyVLvmL3A/sendMessage'
        header = {'content-Type': 'application/json'}
        print(self.texto_telegram)
        for chat_id in EventoTelegram.lista_chats:
            data = {'chat_id': chat_id, 'text': self.texto_telegram}
            req = post(url=url, headers=header, data=json.dumps(data))
            print(req.status_code)
            print(req.text)
            print()


class EventoTelegram(Evento):
    ultimo_recibido = 'Nada por aquí'
    lista_chats = []
    def __init__(self, dic):
        Evento.__init__(self)
        self.nombre = dic['message']['chat']['first_name'].strip() + ' ' + dic['message']['chat']['last_name'].strip()
        self.id = dic['message']['chat']['id']
        self.mensaje = dic['message']['text'].strip()
        if not self.id in EventoTelegram.lista_chats:
            EventoTelegram.lista_chats.append(self.id)
        Evento.lista_eventos.append(self)
        print('\n\nMENSAJE COMPLETO: {}\n\n'.format(self.mensaje))
        if self.mensaje[0] == '/':
            self.interprete.interpretar(self.mensaje, self.id)





def gen_num():
    contador = 1
    while True:
        yield contador
        contador += 1

num_evento = gen_num()
