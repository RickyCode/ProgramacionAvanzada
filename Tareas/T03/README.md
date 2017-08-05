# RQL
Lenguaje de Acceso a Bases de Datos

*Autor: Ricardo Del Río G*
*Estudiate de Pedagogía Media en Matemáticas de la Pontificia Universidad Católica de Chile*

* * *

### Nociones Globales

- El programa solamente tiene implementada la parte de las consultas.
- El interprete solo funciona para consultas simples, la parte de las consultas anidadas no está implementada.

___

### Estructura de los Módulos:

- Hay 5 módulos que comienzan con el nombre "comandos". En cada uno de ellos están implementadas las funciones que estarán posteriormente asociadas a los comandos que se ingresan a través dela interfaz de RQL.
- En el módulo `distribuciones_probabilidad` estan las funciones que representarán las distribucines de probabilidad. Estas funciones serán posteriormente usadas por la funcion `crear_funcion`del módulo `comandos_basicos`. Esta función entregará todos los parámetros que reciben las funciones de las distribiciones salvo el parametro 'x' que deberá ser ingresado por el usuario al momento de llamar a la nueva función creada.
- El módulo `variables_y_comandos` contiene diccionarios que almacenan las funciones y los nombres de variables del programa, tantos los que son propios de RQL como los que el usuario crea durante la ejecución del programa.
- Como el nombre lo dice, el módulo `interpreteRQL` contiene las funciones que permiten interpretar los comandos de RQL.
- En el módulo `comandos_basicos`no logré implementar la función `graficar`dado a que no entendí bien como usar la librería matplotlib.

___

### Error en la Modulación:

Hay un error que se genera dado a que el módulo `comandos_basicos` importa `variables_y_comandos`, pero a su vez `variables_y_comandos` importa `comandos_basicos`. Para solucionarlo pensaba eliminar `variables_y_comandos` y guardar todos los diccionarios que contiene en `comandos_basicos`. Luego habría tenido que cambiar en los otros módulos desde donde debían extraer dichos diccionarios. No alcancé a hacerlo, por lo que comente todas las partes conflictivas de `comandos_basicos` para evitar que el programa se caiga.


***

**Quería aprovechar de hacer un comentario aparte:**

Me tomó bastante tiempo lograr entender como funcionaba la interfaz grafica. Tal vez si hubieran añadido algunos comentarios en las funciones que debíamos modificar habría sido un poco más rápido de entender. Agradecería mucho que lo tengan en consideración para las futuras tareas.

***
