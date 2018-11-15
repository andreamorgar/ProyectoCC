# DESPLIEGUE DE SERVICIO WEB EN UN PASS


## Objetivo y breve resumen del servicio web.

El objetivo principal de este hito era el desarrollo de un pequeño servicio web, y su posterior despliegue en un PaaS. Para ello, se ha desarrollado un pequeño servicio, donde se han implementado la funcionalidad para poder llevar a cabo los cuatro verbos de HTTP: GET, PUT, DELETE y POST.


La descripción del servicio desarrollado se puede encontrar [aquí]().



## Justificación del microframework elegido

La primera elección a la que nos enfrentamos es a la selección de un microframework
con el que trabajar. En mi caso, he elegido [Flask](http://flask.pocoo.org/).

En primer lugar, debemos mencionar que el lenguaje de programación elegido es Python. Haciendo una búsqueda sobre los distintos microframeworks a utilizar, se me planteaban dos posibilidades: elegir Flask, o elegir Django. Finalmente me he decantado por Flask por tres razones principales:
* Asistí al taller "De 0 a Cloud", recomendado por la asignatura, donde se hizo un breve despliegue, y por tanto estaba familiarizada con el microframework.
* Flask está orientado a la simplicidad, mientras que Django ofrece mucha mayor funcionalidad. Para desplegar un pequeño servicio, en realidad no me hacía falta utilizar algo muy complejo, sino al contrario, buscaba hacer las cosas de la manera más sencilla posible.
* No tengo muchos conocimientos respecto a despliegues en la nube, y según consulté en diversas páginas como [esta](https://www.codementor.io/garethdwyer/flask-vs-django-why-flask-might-be-better-4xs7mdf8v), Flask es más adecuado para mi caso, ya es más sencillo de entender su funcionamiento, también a nivel conceptual.


## Justificación del PaaS elegido

El PaaS que se ha elegido para el despliegue del servicio es Heroku, por las siguientes razones:
* Fue recomendado en clase el primer día de la explicación del Hito 2.
* Es gratuíto para aplicaciones sencillas y de bajo consumo, como es este caso.
* Es fácil de enlazar a Github y a Travis (donde se realizan los tests).
* Asistí al taller "De 0 a Cloud", recomendado por la asignatura, donde se hizo un breve despliegue, y por tanto estaba familiarizada.


## TRAVIS

Se ha elegido [Travis](https://travis-ci.org/) como plataforma en  la que testear el código.
Las razones para su elección han sido:
* Fue recomendado en clase el primer día de la explicación del Hito 2.
* Estaba familiarizada con su funcionamiento.
* Se puede enlazar fácilmente a Github y a Heroku
* Hay una amplia documentación acerca de como trabajar con Travis y Heroku de forma conjunta.


## Procedimiento
Por tanto, se ralizará un servicio web en Python con Flask, pasando los test desde Travis y desplegando a Heroku una vez pasados los tests. He documentado el proceso que he seguido para llevar a cabo estas acciones en un pequeño guión con la historia de pasos que he seguido para ello. Se puede ver [aquí]()
