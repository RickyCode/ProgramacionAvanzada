__author__ = 'Ricardo Del Río'

from loggers import MyLogger
from os import listdir, getcwd
from requests import get, post, patch
import json
from random import choice

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

class InterpreteTelegram:
    def __init__(self):
        self.dic_cmds = {'/get': self.get_req,
                         '/post': self.post_req,
                         '/label': self.label,
                         '/close': self.close}
        self.credenciales = None
        # Ejecución de metodos:
        self.obtener_credenciales()

    def obtener_credenciales(self):
        if 'credenciales' in listdir(getcwd()):
            with open("credenciales") as f:
                self.credenciales = tuple(f.read().splitlines())

    def interpretar(self, texto, chat_id):
        # print('INFO: Texto a interpretar en esta solicitud: '+texto)
        # pos_gato = texto.find('#')
        # pos_dos_puntos = texto.find(':')
        # comando = texto[:pos_gato].strip()
        # print('INFO: Comando de esta solicitud: '+comando)
        # if pos_dos_puntos != -1:
        #     num_issue = texto[pos_gato+1:pos_dos_puntos]
        #     valor = texto[pos_dos_puntos:].strip()
        #     if valor[0] == '*':
        #         valor = valor[valor.find(':') + 1:].strip()
        #     self.dic_cmds[comando](chat_id,num_issue, valor)
        # else:
        #     num_issue = texto[pos_gato+1:]
        #     self.dic_cmds[comando](chat_id,int(num_issue))

        try:
            pos_gato = texto.find('#')
            if pos_gato != -1:
                comando = texto[:pos_gato].strip()
                print('INFO: Comando de esta solicitud: '+comando)
                restante = texto[pos_gato+1:]
                pos_esp = restante.find(' ')
                if pos_esp != -1:
                    num_issue = int(restante[:pos_esp])
                    print('INFO: Numero issue de esta solicitud: '+str(num_issue))
                    valor = restante[pos_esp:].strip().replace('*','')
                    print('INFO: Valor de esta solicitud: '+valor)
                    self.dic_cmds[comando](chat_id,num_issue, valor)
                else:
                    num_issue = int(restante)
                    self.dic_cmds[comando](chat_id,int(num_issue))
            else:
                mensaje = '[ERROR]\nComando mal ingresado.'
                self.enviar_mensaje_telegram(mensaje, chat_id)
        except:
            mensaje = '[ERROR]\nComando mal ingresado.'
            self.enviar_mensaje_telegram(mensaje, chat_id)



    # -------------------------------------------------------------------------------------------------------------- GET

    def get_req(self,chat_id, *args):
        num_issue = args[0]
        url = "https://api.github.com/repos/RickyUC/TAREA07/issues/{}".format(num_issue)
        req = get(url, auth=self.credenciales)
        print(req.status_code)
        print(req.text)
        issue = req.json()

        if 'message' in issue:
            if issue['message'] == "Not Found":
                mensaje = '[ERROR]\nNo existe la issue {}'.format(num_issue)
                self.enviar_mensaje_telegram(mensaje, chat_id)
        else:
            enunciado = 'Se obtuvo la issue:'
            self.enviar_mensaje_telegram(self.texto_telegram(num_issue, enunciado, issue['body']), chat_id)


        # url = "https://api.github.com/repos/RickyUC/TAREA07/issues/{}/comments".format(num_issue)
        # if self.credenciales:
        #     req1 = get(url, auth=self.credenciales)
        # else:
        #     req1 = get(url)
        # print(req1.status_code)
        # print(req1.text)
        # comentarios = req1.json()
        # print('INFO: Comentarios de la issue: {}'.format(comentarios))
        #
        # if isinstance(comentarios, dict):
        #     if comentarios['message'] == "Not Found":
        #         enunciado = 'No existe la issue {}'.format(num_issue)
        #         self.enviar_mensaje_telegram(self.texto_telegram(num_issue, enunciado, '--'), chat_id)
        # elif isinstance(comentarios, list):
        #     if comentarios:
        #         num = req1.json()[-1]['id']
        #         print('INFO: Numero ultimo commit issue {}: {}'.format(num_issue,num))
        #
        #         url = "https://api.github.com/repos/RickyUC/TAREA07/issues/comments/{}".format(num)
        #         if self.credenciales:
        #             req2 = get(url, auth=self.credenciales)
        #         else:
        #             req2 = get(url)
        #         dic = req2.json()
        #         texto_comentario = dic['body']
        #         enunciado = 'Se obtuvo el último comentario de la Issue {}: '.format(num_issue)
        #         self.enviar_mensaje_telegram(self.texto_telegram(num_issue, enunciado, texto_comentario), chat_id)
        #     else:
        #         enunciado = 'Esta issue aun no tiene comentarios.'
        #         self.enviar_mensaje_telegram(self.texto_telegram(num_issue, enunciado, '--'), chat_id)

        #
        # url = 'https://api.telegram.org/bot433706040:AAEfwDtNVHctRQUnpxmHWhEBBBuyVLvmL3A/sendMessage'
        # header = {'content-Type': 'application/json'}
        # data = {'chat_id': chat_id, 'text': texto_telegram}
        # req = post(url=url, headers=header, data=json.dumps(data))

    # ------------------------------------------------------------------------------------------------------------- POST

    def post_req(self,chat_id, *args):
        num_issue = args[0]
        valor = {'body':args[1]}

        url = "https://api.github.com/repos/RickyUC/TAREA07/issues/{}/comments".format(num_issue)
        if self.credenciales:
            req = post(url, data=json.dumps(valor), auth=self.credenciales)
        else:
            req = post(url, data=json.dumps(valor))
        enunciado = 'Se publicó el comentario: '
        self.enviar_mensaje_telegram(self.texto_telegram(num_issue, enunciado, str(args[1])), chat_id)

    # ------------------------------------------------------------------------------------------------------------ LABEL

    def label_existe(self, nombre_label):
        url = "https://api.github.com/repos/RickyUC/TAREA07/labels"
        req = get(url, auth=self.credenciales)
        lista_labels = req.json()
        for label in lista_labels:
            if label['name'] == nombre_label:
                print('Si existe esa label')
                return True
        print('No existe esa label')
        return False

    def color(self):
        lista_colores = ['CCFFF', 'FFFFCC', 'CCCCFF', 'FFCCCC', '99FFFF', '66FFCC', 'CCCCCC', '99FF99', '00FFFF',
                         'FFFF00', '33CCCC', '6666FF', 'FF6666']
        return choice(lista_colores)

    def crear_label(self, nombre_label):
        if not self.label_existe(nombre_label):
            url = "https://api.github.com/repos/RickyUC/TAREA07/labels"
            info_label = {'name': nombre_label, 'color': self.color()}
            req = post(url, data=json.dumps(info_label), auth=self.credenciales)
            print(req.status_code)
            print(req.text)
        else:
            'Ya existe ese label.'

    def anadir_label_issue(self, num_issue, nombre_label):
        labels = [nombre_label]
        url = "https://api.github.com/repos/RickyUC/TAREA07/issues/{}/labels".format(num_issue)
        req = post(url, data=json.dumps(labels), auth=self.credenciales)
        print(req.status_code)
        print(req.text)


    def label(self,chat_id, *args):
        num_issue = args[0]
        nombre_label = str(args[1])
        self.crear_label(nombre_label)
        self.anadir_label_issue(num_issue,nombre_label)
        enunciado = 'Se añadió la etiqueta:'
        self.enviar_mensaje_telegram(self.texto_telegram(num_issue, enunciado, nombre_label), chat_id)


    # ------------------------------------------------------------------------------------------------------------ CLOSE

    def cerrar_issue(self, num_issue):
        url = "https://api.github.com/repos/RickyUC/TAREA07/issues/{}".format(num_issue)
        data = {'state': 'closed'}
        req = patch(url, data=json.dumps(data), auth=self.credenciales)
        print(req.status_code)
        print(req.text)

    def close(self,chat_id, *args):
        num_issue = args[0]
        self.cerrar_issue(num_issue)
        enunciado = 'Se cerró la issue: '
        self.enviar_mensaje_telegram(self.texto_telegram(num_issue, enunciado, str(num_issue)), chat_id)

    # ------------------------------------------------------------------------------------------------- ENVIO A TELEGRAM

    def texto_telegram(self, num_issue, enunciado, texto):
        url = "https://api.github.com/repos/RickyUC/TAREA07/issues/{}".format(num_issue)
        if self.credenciales:
            req = get(url, auth=self.credenciales)
        else:
            req = get(url)
        dic = req.json()
        autor_issue = dic['user']['login'].strip()
        link_issue = dic['url'].strip()
        titulo = dic['title']
        return '[{0}]\n[#{1} - {4}]\n{2}\n{5}\n[Link: {3}]'.format(autor_issue, num_issue, enunciado, link_issue, titulo, texto)

    def enviar_mensaje_telegram(self, mensaje, chat_id):
        url = 'https://api.telegram.org/bot433706040:AAEfwDtNVHctRQUnpxmHWhEBBBuyVLvmL3A/sendMessage'
        header = {'content-Type': 'application/json'}
        data = {'chat_id': chat_id, 'text': mensaje}
        post(url=url, headers=header, data=json.dumps(data))


