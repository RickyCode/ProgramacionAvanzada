# PograPop
## Tarea 6.- Programación Avanzada 2017

***Autor: Ricardo Del Río G.***
*Estudiate de Pedagogía Media en Matemáticas de la Pontificia Universidad Católica de Chile*

* * *



## Comentarios Generales
- Comenzé creando el servidor del programa y despúes continué con el Cliente, pero no alcancé a terminarlo todo. Es por esto que hay cosas que estpan implementadas o parcialmente implementadas en el servidor que no están en el Cliente.
- Para reducir el tiempo de conversión todas las canciones se cortan en 20 segundos antes de aplicar el filtro del ecualizador. Si daso la aplicación del filtro la cancion se alarga, se vuelve a cortar. Pero si la cancion se corta queda con menos tiempo.
- Las canciones se cortan a los 40 segundos de reproducción antes de aplicar el filtro 2x
- Todos los sonidos de los filtros son creados digitalmente, ningun animal fue maltratado en la creación de este programa.


## Estructura de los Módulos

- **Módulo `loggers.py`:
Contiene la clase `MyLogger` que es usada en todos los demás módulos para manejar los loggers. Algunos con mostrados a través de la consola, otros son almacenados en archivos `.log`.

**SERVIDOR**

- **Módulo `PrograPopServer.py:`**
Este el el módulo principal del Servidor. Aquí se lleva a cabo todo lo referido con las conexiones del servidor con los usuarios, el envío de mensajes y el envío de archivos.

- **Módulo `chat.py`:**
Contiene una implementación parcial del chat del juego.
 
- **Módulo `clientes_usuarios.py`:**
Posee la clase `ClienteUsuario` que contiene varios métodos estáticos para llevar el manejo de los usuarios. Es decir, permite revisar cuando un usuario está activo o no y también si ya existe el nombre de usuario que el cliente ingresa.

- **Módulo `procesador_comandos.py`:**
Contiene la clase `ProcesadorComandosConsola` que recibe y permite interpretar constantemente gracias a un thread los comandos que se ingresan en la consola del servidor para facilitar su uso.

- **Módulo `salas_canciones.py`:**
En este se encuentran todas las clases y métodos relacionados con la modificación de los archivos wav (corte, filtros), además de la creación de las carpetas en las que se guardarán estos audios.

**CLIENTE**

- **Módulo `PrograPopClient.py`:**
Es el main del cliente. Aquí hay clases y métodos que reunen y conectan los elementos relacionados con la comunicación con e servidor y la interfaz gráfica.

- **Módulo `cliente.py`:**
Principalmente contiene lo relacionado a la comunicación con el servidor.

- **Carpeta `GUI`:
Contiene los archivos `.ui` creados en QtDesigner y sus equivalentes en formato `python` obtenidos con el script `pyuic5`. Están los 3 tipos de ventanas que se utilizan en el rpograma: `inicio_cliente`, `pantalla_inicio` y `sala`. Esta carpeta tiene a su vez la carpeta `Emojis` que pretendía usar en la implementación del chat, pero no alcancé.

- **Carpeta `temp`:
Está carpeta tenía el objetivo de almacenar las canciones cortadas enviadas desde el servidor para su reproducción. La intención era que las canciones se fueran eliminando a medida que ya habían sido reproducidas. Además los archivos se debían guardar con una serie numérica para evitar que el jugador hiciera trampa tratando de ver los nombres de los archivos.

## Funcionalidades:

- **Ingreso**:
Creé una ventana de la GUI que permite al usuario ingresar un nombre como además el PORT y el HOST, a modo de facilitar la modificación de estos datos. Se muestran sugerencias de que PORT y que HOST se pueden utilizar. Para cumplir con el enunciado de todos modos se pueden ingresar en la primera linea del archivo. Si se ingresan de esa manera, esos serán los datos sugeridos al momento de mostrar la ventana. Si no se ingresan en el archivo, los datos sugerido serán la IP del cmputador y el puerto 8000.
El programa es capaz de revisar si un usuario ya existe y si está activo o no además de negar o aceptar los accesos dependiendo del caso. Esto funciona mientras no se finalice el servidor, pues no alcancé a crear una base de datos que se mantuviera despues de desconectar el servidor. Cuando se ingresa un nombre correcto hay que esperar algunos segundo y luego se muestra la ventana principal.

- **Salas:**
No pude encontrar la manera de mostrar una cantidad ilimitada de salas en la ventana principal, pero se muestran hasta 18 salas incluyendo las versiones ecualizador y 2x. En la carpeta Canciones del servdor se pueden crear hasta 6 subcarpetas distintas (Esta cantidad se triplica con los filtros). Con más carpetas habrá un error cuando la GUI intente mostralas.
Se crean sin problemas las vetanas de cada sala y se puede desplazar con facilidad entre las salas y la ventana principal.
Pese a que implementé todos los filtros y los métodos para enviar los archivos, y tenía pensados los mecanismos para la reproducción de los audios en cada sala, no alcance a imlementarlo en el Cliente. Por lo que las salas tienen los espacios para mostrar el tiempo de reproducción, las altenativas y los puntajes de los jugadores, pero estos no se muestran.

- **Canciones:**
Todas las carpetas con canciones deben estar en la carpeta `Canciones` en el servidor. Al momento de aplicar los filtros dentro de esa misma carpeta se crean archivos `.ppop`que servirán de base de datos y la carpeta `__SalasPrograPop__` en la que a su vez se crearán 3 carpetas. Una que contiene los primeros 20 segundos de las canciones y las otras 2 que contienen los primeros 20 segundos de las canciones con filtros (las canciones de menos de 40 segundos pueden durar menos de 20 segundos al aplicar los filtros). Esta estructura permite separar las canciones que ha entregado el usuario de las modificadas por el programa y así evitar cargar las todas las canciones cada vez, sino que solo las nuevas. En aplicar los filtros a las canciones que se entregaron de muestra mi computador se demoró alrededor de 10 minutos.}

- **Filtros**:
Ambos implementados en su totalidad.

- **Puntaje:**
Tanto para el calculo del puntaje como para mostrar el tiempo restante de reproducción tenía pensado hacer un generador que retornara numeros desde el 20 hasta el 0 y que a este se le hiciera next cada vez que pasaba una cantidad de tiempo lo más sercana posible a 1 segundo (usando el método `now` de datetime y threads). Pero no alcancé a implementarlo.

- **Cliente-Servidor**:
Implementado. En general funciona bien y la finalización de uno de los 2 la mayoría de las veces no implica la caida (con errores) del otro, a no ser que se cierren de manera abrupta justo en mitad del envío de algún archivo o mensaje.

- **Estructura de Archivos:**
Como mencioné anteriormente modifique la estructura de la carpeta Canciones para diferenciar las canciones originales de las transformadas.

- **Intefaz Gráfica:**
En general funciona bien.

- **Bonificaciones**
Filtro 2x implementado.
Chat, parcialmente implementado. En el servidor hay métodos y clases creadas con este fin. Está implementado de modo que si alguien manda un chat, el servidor lo reenvía a todos los clientes conectados. No alcancé a implementar que discriminara según la sala en la que estaba el cliente ni que la parte de la UI mostrara los mensajes y los emojis.
Desafíos: No implementado.

