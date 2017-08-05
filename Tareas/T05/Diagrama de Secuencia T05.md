
### Movimiento del Campeon
- Usuario: Presiona tecla, mueve mouse (QKeyEvent)| UI: Thread Manejo de Teclado. Manejo de la posición del Mose (metodo: mover())|  Juego:Su estado se modifica a moviendo. Se fija su destino. (metodo: mostrar_GUI())| GUI: Muestra la nueva orientación del campeon y su desplazamiento.

### Ataque del Campeon
- Usuario: Hace click izquierdo (QKeyEvent) | UI: Interpreta el clickeo y obtiene su ubicación. Se comprueba si el oponente está en el rango de ataque (metodo: atacar())| Juego: Si esta en el rango ataca. Si no esta en el rango se desplaza y despues ataca (metodo: mostrar_GUI()) | GUI: Muestra el ataque o el desplazamiento.

- Usuario: Presiona el click derecho (QKeyEvent)| UI: Interpreta el clickeo y obtiene su ubicacion (metodo: atacar())|  Juego: Chequea la ultma vez que lo uso y el tiempo. Se define la orentación del ataque si es que este se puede realizar. (metodo: mostrar_GUI())| GUI: Muestra el ataque

- Usuario: Mueve el mouse (QKeyEvent) | UI: Detecta si debajo del mouse hay un objeto (metodo: apuntar())| Juego: Detecta si pasa sobre un objeto atacable. De ser así se le asigna un atributo que indique debe ser resaltado. De lo contrario nada (metodo: mostrar_GUI()) | GUI:  Resalta el contonro de la figura si es atacable.

### Merte Inhibidor
- Usuario: Ataco el inhibidor (QKeyEvent)| Juego: Si el inhibidor queda sin vida se guarda el tiempo en el que ocurrio. (metodo: mostrar_GUI())| UI: Mestra el inhibidor muerto | Juego: Al pasar el tiempo, se vuelve a definir el inhibidor como vivo (metodo: mostrar_GUI()) | GUI: El inhibodor se vuelve a mostrar como vivo.
