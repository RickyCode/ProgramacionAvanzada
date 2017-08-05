
# Super Luchín
Software de gestion de recursos para combatir incendios forestales.

*Autor: Ricardo Del Río G*
*Estudiate de Pedagogía Media en Matemáticas de la Pontificia Universidad Católica de Chile*

* * *

#### Estructura de los Módulos:

- Los módulos `incendios.py`, `meteorologia.py`, `recursos.py` y `usuarios.py`: Contienen una clase que lee e interpreta la información de las bases de datos. Cada línea es convertida en un objeto de otra clase el cual es almacenado en una lista que es un atributo de esta primera clase. Contienen una segunda clase en la que se crean los objetos que se almacenan en la primera.

- El objetivo del modulo `entidades.py` era contener clases que representaran a las instituciones que podían utilizar el programa. Cada una de estas clases debía heredar de las clases `Usuarios` y `Entidades` y proveer metodos especificos de cada institución aparte de los entregados en clases padres. No alcancé a implementar el módulo, por lo que solo está su estructura.

- El módulo `calendario.py` posee clases y metodos que permiten al programa identificar si una fecha está correcta, teniendo en cuenta los años biciestos, años seculares y la cantidad de días de cada mes. El programa es capaz de validar cualquier fecha desde el año 0 y sin limites hacia el futuro. (buno, hasta el entero más grande que puede procesar python)

- El módulo `fecha_hora.py` es el encargado de interpretar todos los formatos de fecha y hora que el programa recibe (bases de datos y lo que entrega el usuario). Los objetos de la clase `FechaHora` son almacenados como atributos de los objetos crados con las interpretaciones en las bases de datos. La "fecha actual" del programa tambien es un objeto de la clase `FechaHora`.

- El módulo `linea_tiempo` finalemente no fue implementado. No debí subirlo al repositorio.

- Tampoco debí subir el módulo `probando.py` pues solo lo usaba para experiementar con fragmentos de códigos. (Los eliminé en el último `commit`, pero deben aparacer en la recolección de la tarea)

- `longitudes.py`tiene una funcion para calcular las distancias en el programa.

- `simplificadores.py` y `manejo_csv.py` poseen clases, funciones y métodos que ayudan en algunas labores del programa, como la lectura de las bases de datos y la solicitud de `inputs`.

- `SuperLuchin` es el `main` del prorama.

* * *

#### No Implementado:

- No logré implementar las estrategias de extinción. No encontré la manera de relacionar las distintas bases de datos ni armar la linea temporal de la manera que se pedía. Hay algunos pedazos de intentos fallidos en `incendios.py`. 

- Como no hay *estrategias de extinción*, tampoco hay *incendios apagados*, *recursos más utilizados* ni *recursos más efectivos*

- El menú solo se muestra si el usuario es de la ANAF. No alcancé a copiar y pegar parte del código para los menús de los demás usuarios. Por favor **PIEDAD**  **:(**  

- No alcancé a hacer el diagrama de clases.

* * *

Agradezco cualquier feedback que me puedan dar para mejorar en mis próximas tareas. También cualquier consejo sobre la manera más eficiente de abordar la tarea o de manejar mi tiempo, que creo es lo que más me falló  **:(** 
