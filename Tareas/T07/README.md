# Bot Telegram-GutHub
## Tarea 7.- programación Avanzada 2017

***Autor: Ricardo Del Río G.***

*Estudiate de Pedagogía Media en Matemáticas 
de la Pontificia Universidad Católica de Chile*

* * *

## Comentarios Generales
La tarea está casi casi lista, me falto una pequeña parte, terminar de estructurar los comandos `/label` y `/close`.

## Estructura de los Módulos
- En el `main` se crean las URLs del servidor junto con los algoritmos que permitirán recibir los mensajes de los webhook de Telegram y de GitHub

- `loggers.py` es un modulo que he usado en varias tareas para manejar logs, la puse por si acaso pero no la usé, y olvidé quitarla.

- Cada vez que se recibe un mensaje de los webhooks se crea un objeto de una subclase de `Evento` en el módulo `eventos.py`

- En el módulo `interprete.py` están los metodos que permiten interpretar los comandos ingresados en el chat de Telegram. Aquí también se producen las consecuencias en GitHub de dichos comandos a través de requests.

## Funcionalidades
- Esta implementado el webhook de GitHub. Todo lo que ocurre en mi repositorio público referido a las `issues` y los `comments` es informado al programa del servidor. De hecho se muestra un pequeño resumen de los últimos eventos de GitHub y de Telegram en la página principal. Cuando el mensaje recibido indica que se creo una nueva issue, se envía un mensaje a todos quienes hayan enviado anteriormente un mensaje a mi bot de Telegram.

- Respecto a los comandos de Telegram: `/get` esta totalmente implementada y funciona bien. En cuanto a `/post`  el programa recibe e interpreta el comando y envía a Telegram la confirmación, pero no se genera el cambio en GitHub. No alcancé a corregirlo pues justo me llegó el correo con el commit a revisar. Misma historia con los otros dos, los comandos son interpretados pero no generan consecuencias. Pero vamos, es practicamente lo mismo que los anteriores con pequeñas variaciones como la url de la API de GitHub. Sabía como hacerlo pero no alcancé. Piedad :(

- Todos los mensajes que se envían a Telegram tienen el formato indicado. En el caso de `/get` en honor al tiempo no recuperé el nombre de la issue, pero los demás datos si están.

- Todo lo referido al Bot y a la comunicación del programa con la API de Telegram funciona.

- Heroku: Totalmente implementado. El servidor está corriendo en internet sin problemas.

- Bonus: No implementado.

Eso es todo,
Saludos ;D
