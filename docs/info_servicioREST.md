# SERVICIO REST PARA UNA APLICACIÓN DE PREDICCIONES METEOROLÓGICAS

### Descripción del servicio
Vamos a realizar un pequeño servicio rest, donde se podrá acceder e incorporar distinta información meteorológica para distintas localizaciones. De esta forma, podremos acceder a una serie de predicciones tomadas, donde para cada una de ellas tendremos un valor de temperatura y la localización asociada a dicha predicción. También almacenaremos información como puede ser un ID, que nos permita gestionar las consultas a las predicciones, y un valor fecha que indique la fecha en la que se registra dicha predicción.

#### RUTAS UTILIZADAS:
* En primer lugar, tendremos una ruta raíz "/". En esta ruta se mostrará un simple {status : ok} para ver que el servicio funciona correctamente.

* También disponemos de la ruta "/predictions", que nos permitirá:
1. Visualizar (GET) una lista de las predicciones tomadas hasta el momento. Inicialmente esta ruta estará vacía.
~~~
$ curl -i https://agile-mountain-82339.herokuapp.com/predictions
~~~
2. Añadir (PUT) una nueva predicción. A pesar de que se testea el funcionamiento correcto de esta funcionalidad, podríamos desde la terminal introducirlo manualmente, por ejemplo, mediante una orden como la siguiente:
~~~
$ curl -i -H "Content-Type: application/json" -X PUT -d '{"city":"Malaga", "temperature":"16"}' https://agile-mountain-82339.herokuapp.com/predictions
~~~
3. Modificar (POST) una predicción concreta, en función del ID introducido:
~~~
$ curl -i -H "Content-Type: application/json" -X POST -d '{"city":"Malaga", "temperature":"40", "ID":1}' https://agile-mountain-82339.herokuapp.com/predictions
~~~
4. Borrar (DELETE) una predicción concreta introduciendo el ID correspondiente:
~~~
$ curl -i -H "Content-Type: application/json" -X DELETE -d '{"ID":1}' https://agile-mountain-82339.herokuapp.com/predictions
~~~


* Por último, la ruta "/predictions/<id>", que permitirá consultar una predicción en concreto introduciendo su ID.

En todos los casos se devolverá contenido en forma de fichero json.

### Ficheros utilizados
Para la implementación se han utiizado dos ficheros:

* app_flask.py: contiene la funcionalidad del servicio comentada en la sección anterior.
* weather_class.py: fichero con la especificación de la clase Prediction, la estructura de datos utilizada para los recursos. Su documentación se puede ver también [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/weather_docs.txt)


### Testeo del servicio
Se utilizan dos ficheros distintos para realizar el testeo, uno para cada fichero:

* test_class.py: fichero para testear el funcionamiento de la clase, con cobertura 100%, tal y como podemos ver:
![Resultado covertura weather_class](https://github.com/andreamorgar/ProyectoCC/blob/master/docs/images/coverageclase.png)

* test_app_flask.py: fichero para testear el funcionamiento del servicio, con cobertura 100%, tal y como podemos ver:
![Resultado covertura app_flask](https://github.com/andreamorgar/ProyectoCC/blob/master/docs/images/coverageflask.png)

Tal y como se puede ver en las capturas anteriores, se ha testeado todo la funcionalidad del servicio. Además, se ha hecho especial hincapié en comprobar que el estado, content-type y contenido devuelto por las peticiones realizadas es el correcto. Además, se han realizado también otros testeos adicionales al funcionamiento correcto de lo implementado, como por ejemplo, el hecho de que realizar dos GET a la misma ruta devuelva el mismo resultado, o la consistencia de DELETE cuando pretendamos borrar dos veces el mismo recurso.


Para testear con python, hemos hecho uso de [unittest](https://docs.python.org/3/library/unittest.html), ya que cubre todo lo que necesitamos testear y estaba familiarizada con su funcionamiento, ya que lo he utilizado previamente.

### Anotaciones finales

Para el desarrollo del servicio se han seguido dos guías principales, que se pueden consultar [aquí](http://flask.pocoo.org/docs/1.0/quickstart/) y [aquí](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask).

Para ver la cobertura se ha hecho uso del paquete [coverage](https://coverage.readthedocs.io/en/v4.5.x/) de python.
Además, se han excluido algunos aspectos del testeo, como la prueba de un print del contenido de la clase utilizada, y el testeo de la función app.run() de Flask (la que obviamente funciona porque se testean todas sus funcionalidades)
