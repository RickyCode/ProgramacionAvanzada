# Avanzación Programada
Simulación de un curso de un universo paralelo.

***Autor: Ricardo Del Río G.***
*Estudiate de Pedagogía Media en Matemáticas de la Pontificia Universidad Católica de Chile*

* * *

## Nociones Globales:
Está implementada practicamente toda la pate de la simulación salvo lo correspondiente a los eventos no programados, que están parcialmente implementados y a la nota del exámen (se pone a todos una nota 4 simplemente para mostrar que se programa correctamente la fecha del examen, la entrega de notas y que no se aplican descuentos a este).
La mayotía de los datos generados a lo largo del programa son almacenados en listas, pero me faltó crear las funciones que recopilan toda la información para hacer las estadísticas y los gráficos.

## Estructura de los Modulos:
- **Módulo `contenidos.py`:**
Tiene una clase que recopila y almacena todos los datos referido a los contenidos del curso, que se encuentran en el archivo `contenidos.dsap` en el directorio `info` de la carpeta de la tarea. Todos los demás módulos importan este.

- **Módulo `evento.py`:**
Posee  la clase `Evento` y otras dos clases que heredan de esta. En conjunto representan a los posibles eventos de la simulación y proveen atributos utilizados en su ejecución.
Además la clase `Evento` es la encargada de llevar el orden de ejecución de los eventos y discriminar culaes ya se han realizado y cual es el que debe ejecutarse.

- **Módulo `integrantes.py`:**
Aquí hay clses que representan a cada uno de los tipos de integrantes del curso. Todas estas clases heredan de `Integrantes`. Se utilizan varias properties para mantener actualizados ciertos atributos.

- **Módulo `main.py`:**
En clase `Simulación` se agrupan las funciones que permiten la ejecución de cada uno de los eventos y se muestran en pantalla a través de la consola los datos correspondientes a cada 1. Además se cargan al inicio del programa todos los datos del archivo `integrantes.csv`.

## Funcionalidades:

### Integrantes del  Curso
Se crean en el método `cargar_integrantes` de la clase`Simulación`  y se almacenan como objetos de ditintas clases que heredan de 'Integrantes'
- **Alumnos**
Las cantidad de horas de estudio, la confuanza, manejo de contenidos, cantidad de creditos, nivel de programación y el progreso y nota esperada de las evaluaciones estan implementados con properties que cada vez que se llaman verifican que los valores se encuentren actualizados. Los valores pueden actualizarse dado a un periodo determinado de tiempo o por que se está ejecuntando cierto evento.
La personalidad y la cantidad de creditos tomados son atributos a los que se asigna un valor cada vez que se crea un objeto Alumno.
Pese a que se asignan las personalidades, no están implementados los cambios que estos generan en las distintas actividades del curso.

- **Profesor**
Implementado pero no se ejecuta. Estan creadas las funciones que permiten determinar a que estudiantes atender cada semana y los alumnos tienen atributos que se modifican con la visita al profesor. Además estos atributos son tomados en consideración para definir el nivel de programacion de los estudiantes. Solo me faltó verificar que estos valores se reestablecieran semanalmente a trevés de properties y por despistado me olvidó crear el metodo `reunion_profesor` para ejecutar estas funciones con el evento.
Lo mismo con los tips, en `Alumno` está creada una función y un atributo para evaluar si escuchó o no los tips del profesor, pero no aregué la función al metodo `catedra` de la simulación.

- **Ayudante**
Para efectos prácticos de la simulación no era relevante si la exigencia era definida por el objeto `Ayudante` y/o `Profesor` sino que puede simplemente ser establecida en cada evaluación. Los mismo con el acto de pasar las notas al coordinador. Aunque ahora me doy cuenta que cometí un error, pues la exigencia se establece en `Alumno` y por lo tanto es distinta para cada uno. También la establecí en la clase `Evaluacion` como correspondía, pero algún algoritmo cerebral erroneo me llevó a cometer la barbaridad de no usar eso y usarlo desde cada alumno.
Creé la clase `AyudanteTarea` en caso de necesitar tenerlos diferenciados y agrupados, pero finalmente no la utilicé.
La clase `AyudanteDocencia`posee metodos estáticos que permiten definir que ayudantes participarán en las catedras y quien hará la ayudantía de la semana. Nuevamente por despistado y el estrés de las últimas horas de programación olvidé poner las funciones en la simulación en los metodos `catedra` y  `ayudantia` respectivamente. También se lleva el conteo de las dudas resueltas por un ayudante en catedra con una property.
En cuanto al coordinador posee una función que simula el acto de recibir las notas y properties que definen si habrá descuento o reraso en la entrega. Esto si está implementado.

### **Evaluaciones**
Los aspectos a evaluar de cada evaluacion se revisan en los metodos especificos de cada evaluación en `Alumno`. Las notas se asignan inmediatamente al realizarse la evaluación y se almacenan en listas de cada alumno (No afecta los propositos de la simulación). Cada uno de las listas mencionadas posee tuplas de la forma (nota esperada, nota final) por cada evaluación.
Los controles se crean todos al comienzo de la simulación siguiendo las reglas establecidas.
En cuanto a las demás, cuando ocurre una evaluación se establece la fecha de la siguiente evaluación del mismo tipo.
El calculo de la nota del exámen no esta implementado.

### **Eventos**
Todos los eventos imprescindibles se ejecutan.
En cuanto a los no programados no estan implementados.

### **Estadísticas**
No implementado.

### **Gráficos**
No implementado.

### **Análisis de Resultados**
No implementado.

### **Bases de Datos**
Se lee correctamente `integrantes.csv` pero no se crea el archivo `parametros.csv`.

### **Requisitos, Notas, Restricciones y Alcances**
Creo que todos se cumplen correctamente.







