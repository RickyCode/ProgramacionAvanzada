__author__ = 'Ricardo Del Rio'

#----------------------------------IMPORTACION MODULOS EXTERNOS---------------------------------------------------------


#----------------------------------IMPORTACION MODULOS PROPIOS----------------------------------------------------------
from simplificadores import SuperInput
from fecha_hora import fecha_hora_actual, FechaHora
from meteorologia import met
from usuarios import Usuarios
from recursos import Recursos


usr = Usuarios()
usr.cargar_datos()
recurso_id = usr.verificacion_usuario_contrasena()

met.cargar_datos()
print()
fecha_hora_actual.ingresar_fecha_hora()
fecha_hora_actual.interpretar()

rec = Recursos()
rec.cargar_datos()

stop = False
while not stop:

    parar = False
    while not parar:

        for recurso in rec.recursos:
            if recurso_id == '':
                opciones = ['[3] Ver Incendios Activos',
                            '[4] Ver Incencios Apagados',
                            '[5] Ver Recursos Mas Utilizados',
                            '[6] Ver Recursos Mas Efectivos',
                            '[7] Modificar Usuarios',
                            '[8] Agregar Pronostico',
                            '[9] Agregar Incendio',
                            '[10] Leer Bases de Datos \n',
                            '[0] Cambiar Hora',
                            '[1] Cerrar Sesión',
                            '[2] Salir']
                for i in opciones:
                    print(i)
                print()

                opcion = SuperInput('>>> Ingresa la opcion correspondiente: ', 'int').superinput()

                if opcion == [0]:
                    print()
                    fecha_hora_actual.ingresar_fecha_hora()
                    fecha_hora_actual.interpretar()
                    parar = True

                elif opcion == [1]:
                    print()
                    recurso_id = usr.verificacion_usuario_contrasena()
                    parar = True

                elif opcion == [3]:
                    parar = True
                    stop = True

                elif opcion == 3 or opcion == 4 or opcion == 5 or opcion == 6:
                    print()
                    print('Opcion no implementada, por favor ingresa otra opcion')
                    print()

                elif opcion == 10:
                    print('[1] Ver Incendios\n'
                          '[2] Ver Recursos\n'
                          '[3] Ver Usuarios\n')
                    opcion = SuperInput('>>> Ingresa la opcion correspondiente: ', 'int').superinput()

                    if opcion == 1:
                        pass
                    elif opcion == 2:
                        pass
                    elif opcion == 3:
                        print(usr)

                else:
                    print('Opcion invalida! Vuelve a iingresar')
                    print()


            elif recurso.idn == recurso_id:
                if recurso.tipo == 'AVION':
                    pass
                elif recurso.tipo == 'HELICOPTERO':
                    pass
                elif recurso.tipo == 'BRIGADA':
                    pass
                elif recurso.tipo == 'BOMBEROS':
                    pass

