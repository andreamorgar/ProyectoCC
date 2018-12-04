# Proyecto Cloud Computing
## Autora: Andrea Morales Garzón

### Prácticas de la asignatura Cloud Computing del Máster de Ingeniería Informática para el curso 2018/2019

## Proyecto a desarrollar
Estudio de las condiciones meteorológicas en Granada a través de la información facilitada por la Agencia Estatal Española de Meteorología ([AEMET](http://www.aemet.es/es/portada))



**Contenido**
- [Descripción del proyecto](#id1)
- [Arquitectura](#id2)
- [Testeo y pruebas](#id3)
- [Framework y lenguaje a utilizar](#id4)
- [Desplegar el proyecto](#id5)
- [Provisionamiento de máquinas virtuales](#id6)
- [Comprobación del provisionamiento en otra máquina](#id7)
- [Comprobación del provisionamiento de otro compañero](#id8)
- [Últimos avances en el proyecto](#id9)
- [Licencia](#id10)


### Descripción del proyecto  <a name="id1"></a>

En este proyecto, se pretende hacer un pequeño análisis de la información actualizada que nos proporciona la [API](https://opendata.aemet.es/centrodedescargas/inicio) de la **Agencia Estatal Española de Meteorología**. De esta forma, se pretende procesar la información de la misma, mostrando aquella más trascendental para los usuarios de Granada en distintas plataformas.

A través de la API de dicha plataforma, se va a acceder a la información más actualizada, y se irá almacenando, de entre dicha información, aquella que en términos generales interesa más a los usuarios.

Se pretende abordar dicho análisis de información en distintos ámbitos. Por una parte, la posibilidad de acceder a la temperatura actual, los centímetros cúbicos registrados, o la temperatura más alta/baja detectada durante ese día. En segundo lugar, proporcionar distintos análisis semanales y mensuales a partir de la información obtenida a partir de los datos actualizados que se van proporcionando a lo largo del tiempo. Este último análisis tiene su interés, ya que las estructuras de datos facilitadas a nivel semanal/mensual son menos específicas en cuanto a la información mostrada diariamente, y puede que haya aspectos de la información diaria de interés para el usuario a nivel semanal o mensual, y que actualmente vea restringido su acceso a dichos datos.


Los usuarios podrán acceder a toda la información que se analice mediante dos formas:
* A través de **Twitter**: se publicarán diversos tweets con la información más importante que se ha ido recabando.
* A través de un bot de **Telegram** también se podrá acceder a la información más relevante.


De esta forma, se pretende facilitar al usuario la consulta de la información más trascendental de una forma sencilla y rápida a través de plataformas utilizadas diariamente por millones de usuarios, como es el caso de las redes sociales mencionadas anteriormente.



### Arquitectura  <a name="id2"></a>
Se va a utilizar una arquitectura basada en microservicios en sustitución a una arquitectura monolítica. De este modo podremos realizar y modificar cambios en el software de forma sencilla e independiente, aprovechando las ventajas que nos aporta este tipo de arquitecturas, como pueden ser:
* Versatilidad
* Autonomía: podemos actualizar un microservicio sin que dependa de los demás
* Facilidades de integración
* Aislamiento de errores: un fallo en un microservicio afectará al funcionamiento del mismo, y no tiene por qué afectar a las demás funcionalidades.
* ...

Tendremos así, una colección de distintos microservicios, donde cada uno se encargará de implementar una funcionalidad dentro de la totalidad del proyecto.

Los microservicios que se van a utilizar son los siguientes:.
* Un microservicio que se encargue de **acceder a la API de la AEMET y se encargue de procesar la información obtenida**. La API de la AEMET funciona con distintos ficheros JSON, dependiendo de las características a consultar: datos mensuales, datos de observación actualizados, etc... Se escogeran aquellos que sean de interés para el proyecto, que en principio serán los *datos de observación* y los *valores climatológicos*.

* Un microservicio para **almacenar toda la información a manejar en una base de datos**. Debido a que el lenguaje principal que se va a utilizar va a ser Python, escogeremos una Base de Datos que funcione bien con dicho lenguaje. De entre las diversas [alternativas](https://www.quora.com/What-is-the-best-database-suitable-with-Python-for-web-applications) encontradas, en principio, se utilizará la base de datos NoSQL MongoDB. Se ha decidido esta base de datos por dos razones principales. La primera de ellas, por su facilidad de trabajo con Python (utilizaremos [pymongo](http://api.mongodb.com/python/3.6.0/tutorial.html) para acceder a un cliente de MongoDB y trabajar desde ahí), y en segundo lugar por ser una base de datos con la que ya he trabajado previamente.

* Un microservicio para realizar el **análisis de datos**. En este microservicio, se realizará un análisis de los valores medidos a lo largo del día o la semana que puedan ser de interés. Por ejemplo, como se comentaba anteriormente, poder adquirir valores máximos y mínimos diarios en lo que se lleva de día.

* Quedaría por ver cómo publicar la información. En este caso, estamos hablando de dos microservicios distintos, cada uno encargado de publicar la información a través de una red social diferente. Tendremos un **microservicio que se encargue de publicar tweets**, con información relevante obtenida (a través de [tweepy](http://www.tweepy.org/), y **otro microservicio diferente que consistirá en un bot de telegram** en el cuál podamos también poner a disposición del usuario aquellos datos que puedan ser de mayor importancia (en principio a través de [telebot](https://geekytheory.com/telegram-programando-un-bot-en-python). Se intentarán llevar a cabo ambos microservicios, pero en caso de haber falta de tiempo, se priorizará la publicación de la información a través de Twitter. El tipo de arquitectura utilizado, nos permite esta diferenciación a la hora de publicar la información, ya que podríamos añadir todas las plataformas que quisiésemos para mostrar los datos, sin depender del resto de microservicios que forman el proyecto.

* Por último, existirá un **microservicio LOG**, con el que se comuniquen todos los microservicios anteriores, para informar de las acciones que se están llevando a cabo, almacenarlas y así brindar la posibilidad de poder realizar análisis y monitorizar nuestra aplicación.

Para la comunicación entre los distintos microservicios, se realizará mediante brokers. En este caso, el broker a utilizar será [RabbitMQ](https://www.rabbitmq.com/).

A continuación, en la siguiente imagen, se puede ver un pequeño esquema de los microservicios a utilizar:

![Esquema de los microservicios](https://raw.githubusercontent.com/andreamorgar/ProyectoCC/master/docs/images/esquemaMicroservicios.png)



De momento, estos son todos los microservicios y comunicaciones que se realizarán. En el futuro, con el avance del proyecto, se irán incorporando los distintos cambios que vayan surgiendo durante la implementación.




#### Testeo y pruebas  <a name="id3"></a>
Cada microservicio se testeará de forma individual, antes de desplegarlo en la nube. La realización de los tests se llevará a cabo mediante [TRAVIS](https://travis-ci.org/), y dichos tests se implementarán en Python (ya que es el lenguaje utilizado en el microservicio) con ayuda de la librería [unittest](https://docs.python.org/3/library/unittest.html).

### Framework y lenguaje a utilizar  <a name="id4"></a>
Se va a utilizar como lenguaje de programación [Python](https://www.python.org) y [Flask](http://flask.pocoo.org/) como microservicio. Además, el proyecto será desplegado en Azure.



### Desplegar el proyecto  <a name="id5"></a>
Despliegue: https://agile-mountain-82339.herokuapp.com/

Se ha realizado un despliegue del servicio web, realizada en el PaaS [Heroku](https://www.heroku.com/). Para ello se han seguido una serie de pasos, que cubren todo el procedimiento que se ha seguido desde el funcionamiento del servicio en _localhost_ hasta su despliegue en Heroku con las comprobaciones correspondientes. También se puede apreciar en ese fichero todas las decisiones tomadas para llevar a cabo el procedimiento.



#### DESPLIEGUE DE SERVICIO WEB EN UN PASS


##### Objetivo y breve resumen del servicio web.

El objetivo principal de este hito era el desarrollo de un pequeño servicio web, y su posterior despliegue en un PaaS. Para ello, se ha desarrollado un pequeño servicio, donde se han implementado la funcionalidad para poder llevar a cabo los cuatro verbos de HTTP: GET, PUT, DELETE y POST.


##### Descripción del servicio desarrollado

SERVICIO REST PARA UNA APLICACIÓN DE PREDICCIONES METEOROLÓGICAS.

**Descripción del servicio**
Vamos a realizar un pequeño servicio rest, donde se podrá acceder e incorporar distinta información meteorológica para distintas localizaciones. De esta forma, podremos acceder a una serie de predicciones tomadas, donde para cada una de ellas tendremos un valor de temperatura y la localización asociada a dicha predicción. También almacenaremos información como puede ser un ID, que nos permita gestionar las consultas a las predicciones, y un valor fecha que indique la fecha en la que se registra dicha predicción.

**RUTAS UTILIZADAS:**
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

**Ficheros utilizados**
Para la implementación se han utiizado dos ficheros:

* app_flask.py: contiene la funcionalidad del servicio comentada en la sección anterior.
* weather_class.py: fichero con la especificación de la clase Prediction, la estructura de datos utilizada para los recursos. Su documentación se puede ver también [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/weather_docs.txt).

**Estructura de datos para el recurso**
En el apartado anterior se ha mencionado que estamos utilizando un fichero que define la estructura de datos de los recursos con los que vamos a trabajar. Se trata de una clase a la que hemos llamado Prediction, la cuál representa una predicción meteorológica de la temperatura en una ciudad. Tiene cuatro atributos básicos.

* Atributo _city_: hace referencia a la ciudad sobre la que se ha tomado la predicción
* Atributo _temperature_: hace referencia a la temperatura existente en la ciudad _city_ en el momento en el que se toma la predicción
* Atributo _date_: hace referencia a la fecha en la que se registra la predicción tomada.
* Atributo _ID_: es el identificador del recurso, que se genera automáticamente al crear el objeto de la clase.

En cuanto a los métodos implementados para la clase, son los básicos para el funcionamiento de la misma
* Métodos que permitan modificar la temperatura (_temperature_) y la ciudad (_city_) de la clase-
* Métodos para acceder a los atributos de la clase
* Método para representar el objeto de la clase.


**Testeo del servicio**
Se utilizan dos ficheros distintos para realizar el testeo, uno para cada fichero:

* test_class.py: fichero para testear el funcionamiento de la clase, con cobertura 100%, tal y como podemos ver:
![Resultado covertura weather_class](https://github.com/andreamorgar/ProyectoCC/blob/master/docs/images/coverageclase.png)

* test_app_flask.py: fichero para testear el funcionamiento del servicio, con cobertura 100%, tal y como podemos ver:
![Resultado covertura app_flask](https://github.com/andreamorgar/ProyectoCC/blob/master/docs/images/coverageflask.png)

Tal y como se puede ver en las capturas anteriores, se ha testeado todo la funcionalidad del servicio. Además, se ha hecho especial hincapié en comprobar que el estado, content-type y contenido devuelto por las peticiones realizadas es el correcto. Además, se han realizado también otros testeos adicionales al funcionamiento correcto de lo implementado, como por ejemplo, el hecho de que realizar dos GET a la misma ruta devuelva el mismo resultado, o la consistencia de DELETE cuando pretendamos borrar dos veces el mismo recurso.


Para testear con python, hemos hecho uso de [unittest](https://docs.python.org/3/library/unittest.html), ya que cubre todo lo que necesitamos testear y estaba familiarizada con su funcionamiento, ya que lo he utilizado previamente.

**Anotaciones finales**

Para el desarrollo del servicio se han seguido dos guías principales, que se pueden consultar [aquí](http://flask.pocoo.org/docs/1.0/quickstart/) y [aquí](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask).

Para ver la cobertura se ha hecho uso del paquete [coverage](https://coverage.readthedocs.io/en/v4.5.x/) de python.
Además, se han excluido algunos aspectos del testeo, como la prueba de un print del contenido de la clase utilizada, y el testeo de la función app.run() de Flask (la que obviamente funciona porque se testean todas sus funcionalidades)



##### Justificación del microframework elegido

La primera elección a la que nos enfrentamos es a la selección de un microframework
con el que trabajar. En mi caso, he elegido [Flask](http://flask.pocoo.org/).

En primer lugar, debemos mencionar que el lenguaje de programación elegido es Python. Haciendo una búsqueda sobre los distintos microframeworks a utilizar, se me planteaban dos posibilidades: elegir Flask, o elegir Django. Finalmente me he decantado por Flask por tres razones principales:
* Asistí al taller "De 0 a Cloud", recomendado por la asignatura, donde se hizo un breve despliegue, y por tanto estaba familiarizada con el microframework.
* Flask está orientado a la simplicidad, mientras que Django ofrece mucha mayor funcionalidad. Para desplegar un pequeño servicio, en realidad no me hacía falta utilizar algo muy complejo, sino al contrario, buscaba hacer las cosas de la manera más sencilla posible.
* No tengo muchos conocimientos respecto a despliegues en la nube, y según consulté en diversas páginas como [esta](https://www.codementor.io/garethdwyer/flask-vs-django-why-flask-might-be-better-4xs7mdf8v), Flask es más adecuado para mi caso, ya es más sencillo de entender su funcionamiento, también a nivel conceptual.


##### Justificación del PaaS elegido

El PaaS que se ha elegido para el despliegue del servicio es Heroku, por las siguientes razones:
* Fue recomendado en clase el primer día de la explicación del Hito 2.
* Es gratuíto para aplicaciones sencillas y de bajo consumo, como es este caso.
* Es fácil de enlazar a Github y a Travis (donde se realizan los tests).
* Asistí al taller "De 0 a Cloud", recomendado por la asignatura, donde se hizo un breve despliegue, y por tanto estaba familiarizada.


##### TRAVIS

Se ha elegido [Travis](https://travis-ci.org/) como plataforma en  la que testear el código.
Las razones para su elección han sido:
* Fue recomendado en clase el primer día de la explicación del Hito 2.
* Estaba familiarizada con su funcionamiento.
* Se puede enlazar fácilmente a Github y a Heroku
* Hay una amplia documentación acerca de como trabajar con Travis y Heroku de forma conjunta.


##### Procedimiento
Por tanto, se ralizará un servicio web en Python con Flask, pasando los test desde Travis y desplegando a Heroku una vez pasados los tests. He documentado el proceso que he seguido para llevar a cabo estas acciones en un pequeño guión con la historia de pasos que he seguido para ello. Se puede ver [aquí](https://github.com/andreamorgar/ejerciciosCC/blob/master/Objetivos/procedimiento_despliegue.md)



A continuación se encuentran enumerados los pasos que he seguido para realizar el despliegue.

**1. Registro en Travis**
El primer paso necesario es disponer de ua cuenta en Travis. Podemos iniciar sesión directamente con nuestro usuario de Github. De esta forma, podremos gestionar el testeo de los repositorios que tengamos en dicha cuenta.

**2. Activar el repositorio de nuestro proyecto en Travis, para poder pasar los tests.**
Simplemente buscamos desde la plataforma Travis el repositorio que queremos testear, y lo seleccionamos.

**3. Crear .travis.yml**
Para poder hacer el testeo del repositorio, necesitamos crear el archivo [.travis.yml](https://github.com/andreamorgar/ProyectoCC/blob/master/.travis.yml) y completarlo con mis especificaciones. Para ello he seguido los pasos de la [documentación](https://docs.travis-ci.com/user/languages/python/). Este fichero, lo ponemos en la ruta raiz de nuestro repositorio.

**4. Tenemos que ver como se despliega en HEROKU**
Para ello, seguimos la [documentación](https://docs.travis-ci.com/user/deployment/heroku/) oficial que encontramos en Travis.

**5. Instalo los clientes.**
 - [Cliente heroku](https://devcenter.heroku.com/articles/heroku-cli)
 - [Cliente travis](https://github.com/travis-ci/travis.rb#installation). En este caso, hay que tener en cuenta que debemos tener instalado [Ruby](https://www.ruby-lang.org/es/) en nuestro ordenador. En mi caso, no lo tenía, por lo que tuve que proceder con la [instalación](http://www.ruby-lang.org/en/downloads/). Para ello, simplemente lo instalamos desde el gestor de paquetes. Además, para un correcto funcionamiento, hay que asegurarse de que la versión utilizada sea superior a la 2.0.

**6.  Instalo Cliente travis**
Una vez tenemos instalado Ruby, podemos proceder con la instalación de Travis. Para ello intentamos la orden que viene en la documentación:
~~~
$ gem install travis -v 1.8.9 --no-rdoc --no-ri
~~~
Sin embargo, no funciona, y siguiendo las correcciones [aquí](https://github.com/travis-ci/travis.rb/issues/391) y [aquí](https://github.com/travis-ci/travis.rb#ubuntu), vemos que hay un problema con las dependencias, y por ello instalo la siguiente versión de Ruby.
~~~
$ sudo apt-get install ruby2.3-dev (porque yo tengo ruby2.3)
~~~

Al repetir la orden correspondiente, podemos continuar la instalación.

**7. Intento realizar encriptación mediante Travis**

Para ello, utilizamos la siguiente orden, tal y como viene indicado en los pasos de la documentación de Travis que estamos siguiendo.
~~~
encrypt $(heroku auth:token) --add deploy.api_key
~~~
Sin embargo, por alguna razón, no consigo que funcione este método, por lo que intento una forma automática de lanzar los test antes del despliegue en heroku. Por tanto, ya no hace falta que introduzca dicha encriptación en .travis.yml, tal y como se indica en la documentación.


**8. Creo el fichero requeriments.txt**
Con este fichero, podremos instalar mediante pip todo lo necesario para que funcione nuestro servicio. Evitando usar la orden "pip freeze", he utilizado el paquete [pipreqs](https://github.com/bndr/pipreqs), que genera el fichero _requeriments.txt_ que se puede ver [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/requirements.txt). De esta forma instalaremos únicamente lo estrictamente necesario para nuestra versión actual del proyecto.


**9. Fichero Procfile**
Para redactar el contenido de este fichero, sigo las indicaciones de [aquí](https://devcenter.heroku.com/articles/python-gunicorn). Como se está indicando que utilicemos guinicorn, debemos instalarlo propiamente, para un correcto funcionamiento del proyecto. [Guincorn](https://gunicorn.org/) es un servidor HTTP para Python, que es compatible con Flask, lo que me permite su utilización. Este hecho provoca que tenga que volver a actualizar mi fichero _requeriments.txt_, ya que debe añadir esta nueva incorporación.

El contenido del fichero Procfile se puede ver [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/Procfile). Como se observa, únicamente contiene una línea en la que indicamos el servidor HTTP utilizado y el nombre del fichero en el que se implementa nuestro servicio.

**10. Fichero runtime.txt**
Necesitamos también crear un fichero [runtime.txt](https://github.com/andreamorgar/ProyectoCC/blob/master/runtime.txt), para especificarle a Heroku la versión de Python con la que debe ejecutar los ficheros. En este caso, es importante destacar un error que tuve, ya que Heroku solo es compatible con las versiones de Python 3.6.6. y 3.7.0. En mi caso, yo trabajaba con la versión 3.5.2, lo que impedía que se realizara de forma correcta el despliegue. Viendo las posibilidades de corrección que me proporcionaba Heroku mediante la terminal, simplemente tenía que cambiar la versión en runtime.txt para poder continuar, teniendo en cuenta que después debería comprobar que los tests seguían funcionando a pesar de este cambio en la versión. De esta forma, he podido comprobar, cómo los tests no solo comprobaban que el código estaba correcto, sino que también sirve para asegurar el funcionamiento de mi proyecto en el despliegue.
Esta es la razón por la que runtime.txt contiene la versión 3.6.6 de python.

Se puede acceder a mi fichero runtime.txt desde [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/runtime.txt). Como se puede observar en el fichero, únicamente contiene la versión de Python con la que vamos a funcionar.

**11. Desplegar en heroku**
Para ello, seguimos los pasos indicados [aquí](https://devcenter.heroku.com/articles/getting-started-with-python#deploy-the-app). Las tres órdenes importantes a realizar son las siguientes:
~~~
heroke create
git push heroku master
~~~
Con dichas órdenes, estamos creando un proyecto de despliegue en Heroku cuando hacemos push del repositorio que queremos desplegar. Es muy útil que te permita ver los [logs](https://devcenter.heroku.com/articles/getting-started-with-python#view-logs), porque te das cuenta de lo que realmente está pasando, de si se ha realizado correctamente el despliegue y, en caso de que no, qué es lo que ha ocurrido. Por ejemplo, a mí me ha servido para poder averiguar problemas que me daba al desplegar, como puede ser que hayas ocupado todas las facilidades de la cuenta gratuita de Heroku.


**12. Conexión con travis, para que nuestro proyecto no se despliegue antes de pasar los tests**
Desde nuestra cuenta en Heroku, nos vamos a la pestaña de Deploy, y seleccionamos la opción de *Enable automatic deploys*, para que con cada push a nuestro repositorio, se pueda desplegar automáticamente en Heroku. Para que los test se realicen previo al despliegue, tenemos que seleccionar la opción de no desplegar hasta que se ejecuten de forma correcta los tests de travis. Todo este proceso lo realizo siguiendo las instrucciones de [aqui](https://medium.com/@felipeluizsoares/automatically-deploy-with-travis-ci-and-heroku-ddba1361647f)

**13. Hacemos heroku login, que nos manda a la web a hacer login**
~~~
$ heroku git:remote -a <nombre proyecto>
~~~

[Aquí](https://devcenter.heroku.com/articles/git) se puede ver más o menos todos los pasos que hemos ido siguiendo a lo largo del proceso.


**14. Otros errores**
Por último faltaría un problema con la distribución en directorios de mis archivos, que impide que se ejecuten mis tests al no estar en la misma ruta que los ficheros a testear.
Este problema lo he solucionado como se indica [aquí](https://stackoverflow.com/questions/1732438/how-do-i-run-all-python-unit-tests-in-a-directory), con la orden:
~~~
python -m unittest discover test/
~~~


Una vez seguidos todos estos pasos, se obtiene un correcto despliegue del servicio REST que hemos realizado.







---
### Provisionamiento de máquina virtuales  <a name="id6"></a>

MV: 137.117.174.154

En este documento se detallan los distintos pasos seguidos hasta conseguir provisionar una máquina virtual (primero a nivel local y posteriormente en Azure), con todo lo necesario para poder ejecutar en ella nuestro proyecto. Para ello, se seguirán los siguientes pasos:

1. Uso de *Vagrant* y *Ansible* para provisionar una máquina virtual desde local.

2. Uso de *Ansible* para provisionar una máquina virtual en la plataforma *Azure*.



#### *Vagrant* y *Ansible* para provisionar una máquina virtual desde local.
##### Instalación de las herramientas necesarias

**Instalación de Vagrant**
En primer lugar, vamos a trabajar con máquinas virtuales locales. Para ello, necesitamos instalar una herramienta que nos permita gestionar máquinas virtuales, de forma que podamos arrancarlas, provisionarlas y destruirlas fácilmente.

Por ello, se ha hecho uso de [Vagrant](https://www.vagrantup.com/). Se ha utilizado esta herramienta por dos razones principales:
- Se explicó en el seminario de Ansible impartido en la asignatura, por lo que ya estaba familiarizada.
- Vagrant permite configurar máquinas virtuales de una manera sencilla, además de ser muy fácil de cambiar esa configuración para trabajar con máquinas virtuales en la nube.

El primer paso por tanto, es instalar la herramienta. Para ello, hemos seguido los pasos vistos [aquí](https://howtoprogram.xyz/2016/07/23/install-vagrant-ubuntu-16-04/). Para un correcto funcionamiento de la herramienta, es esencial tener en cuenta dos aspectos:
- Necesitamos una herramienta como VirtualBox, donde podamos gestionar las máquinas virtuales que se están creando y acceder a las mismas.

- Hay que tener cuidado con la versión de Vagrant que instalamos. Si instalamos la herramienta mediante el gestor de paquetes, tal y como se indica en el enlace de descarga anterior, la versión que se descarga por defecto es *Vagrant 1.8.1*. Suponiendo que queremos trabajar con *VirtualBox* (como es mi caso), es importante saber que dicha versión de Vagrant no trabaja con las últimas versiones de *VirtualBox*, por lo que debemos actualizar, como mínimo, a la versión 2.0.2. Para ello, se pueden seguir los pasos vistos [aquí](https://github.com/openebs/openebs/issues/32).


**Instalación de Ansible**
El primer paso es instalar ansible en la máquina con la que estemos trabajando. Para poder disponer de ansible podemos instalarla desde dos formas principales:
- Utilizar el gestor de paquetes *apt-get*, tal y como se puede ver indicado [aquí](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-ansible-on-ubuntu-16-04).

- Instalar Ansible mediante *pip*. En este caso, vamos a seguir esta segunda forma, ya que como se vio en el seminario de Ansible de la asignatura, el instalar Ansible mediante *pip* tiene sus ventajas. Esto se debe a que te instala, de forma automática, otros modulos necesarios, como por ejemplo para trabajar con YAML (lo necesitaremos más tarde). Podemos ver cómo realizar la instalación [aquí](https://docs.ansible.com/ansible/2.7/installation_guide/intro_installation.html#latest-releases-via-pip).



##### Creación de una máquina virtual con Vagrant

**1. Crear un entorno Vagrant**
Una vez que tenemos Vagrant correctamente instalado, nos situamos en un directorio sobre el que trabajar. En mi caso, todo este proceso lo he realizado desde mi repositorio de ejercicios, por lo que una vez situada en la carpeta correspondiente, ejecutamos lo siguiente.
~~~
$ vagrant init
~~~
Con esta orden, estamos inicializando el directorio actual, de forma que sea un entorno *Vagrant*. Una vez ejecutada dicha orden, se crea un archivo *VagrantFile* en caso de que no exista anteriormente.
Este fichero recién creado, tenemos que modificarlo para adaptarlo a aquello que queramos hacer.


**2. Crear una máquina virtual**
En primer lugar, **especificamos la máquina que queremos crear**. Para ello, podemos buscar [aquí](https://app.vagrantup.com/boxes/search?utf8=%E2%9C%93&sort=downloads&provider=&q=ubuntu) el nombre asociado al sistema operativo que queremos que tenga la máquina virtual que vamos a crear. Este nombre, será el que debemos asociar a "config.vm.box" en el fichero VagrantFile. En mi caso, he especificado que la máquina que quiero crear tenga como sistema operativo *Debian 9*. Las razones de esta decisión son:

- En primer lugar, que cuenta con una versión de Python3 ya instalada, sobre la cuál podemos trabajar directamente.

- En segundo lugar, porque además de lo anterior, se puede ver aquí que estamos trabajando con un sistema operativo proporcionado por la página oficial, y no por algún usuario de la plataforma (razón por la que se prescindió de Ubuntu Server 16.04).


En este punto, el contenido del fichero VagrantFile sería el que se muestra a continuación.

**Contenido del fichero *VagrantFile* hasta el momento:**
~~~
Vagrant.configure("2") do |config|
  config.vm.box = "debian/contrib-stretch64"
  config.vm.hostname = "ubuntuAndrea"

end
~~~

Por tanto, vamos a crear la máquina. Para ello ejecutamos la siguiente orden:
~~~
$ vagrant up
~~~
Una vez finalice la creación de dicha máquina, podemos abrir *VirtualBox*, y comprobar que, efectivamente se ha creado dicha máquina. Lo podemos ver en la siguiente imagen.
![Creación de la máquina virtual con Vagrant](https://raw.githubusercontent.com/andreamorgar/ejerciciosCC/master/images/hito3/mv.png)


Como podemos observar en el fichero de VagrantFile anteriormente mostrado, en este punto aún no hemos realizado ningún provisionamiento con *Ansible*.
Sin embargo, para ver si la máquina virtual que hemos creado a través de *Vagrant* está operativa, podemos hacer un simple **ping**, y de esta forma comprobarlo. En la siguiente figura, podemos ver cómo realmente funciona. En la primera orden ejecutada, podemos ver cómo estamos haciendo ping a todas las máquinas virtuales. En nuestro caso, tenemos únicamente una, por lo tanto la orden ejecutada es equivalente a hacer ping directamente de nuestra máquina. Lo hacemos también, y vemos como efectivamente obtenemos igual resultado.

![Ping a la máquina que hemos creado](https://raw.githubusercontent.com/andreamorgar/ejerciciosCC/master/images/hito3/ping.png)


Además, podemos acceder a la máquina mediante ssh, tal y como se puede ver a continuación. Como podemos observar en la imagen, hemos podido conectarnos de forma correcta mediante SSH. Además, he ejecutado algunas órdenes para poder conocer mejor el estado en el que se encuentra la máquina:
- En primer lugar, podemos comprobar que el sistema operativo de la máquina es el que queríamos, mediante la ejecución del comando **hostnamectl**. Podemos ver también, que se ha creado con el nombre que especificamos en el fichero *VagrantFile*.

- Por otra parte, podemos ver cómo las utilidades que pretendemos instalar con el provisionamiento (como **git** o **pip3**), no están. Esto nos servirá para que, cuando ejecutemos la orden asociada al provisionamiento, veamos cómo realmente hemos hecho un provisionamiento correcto, y están instalados todos los paquetes y librerías que especifiquemos.

![Acceso por ssh a la máquina que hemos creado](https://raw.githubusercontent.com/andreamorgar/ejerciciosCC/master/images/hito3/pruebaSSH.png)

---
**Provisionamiento de la máquina virtual**

Vamos a instalar en la máquina virtual todo aquello que necesitemos. Para ello, podemos consultar la guía oficial [aquí](https://docs.ansible.com/ansible/2.7/scenario_guides/guide_vagrant.html), concretamente el apartado *Vagrant Setup*. Aquí se muestra un ejemplo de cómo podemos modificar el fichero VagrantFile para provisionar una única máquina. Para ello, haremos uso de Ansible.

Para poder llevar a cabo el provisionamiento con Ansible, necesitaremos dos ficheros:
- Fichero [ansible.cfg](https://github.com/andreamorgar/ProyectoCC/blob/master/provision/vagrant/ansible.cfg), en el que indicademos dos aspectos principales. En primer lugar, ponemos a False la comprobación de claves del host, para evitar problemas como Man in the Middle, tal y como se explicón en el seminario de Ansible. En segundo lugar, le estamos especificando cuál es el fichero (ansible_hosts) con el que vamos a trabajar y definir las máquinas en cuestión.

- Fichero [ansible_hosts](https://github.com/andreamorgar/ProyectoCC/blob/master/provision/vagrant/ansible_hosts), donde hacemos dos cosas principales. Por una parte, establecemos el puerto (en nuestro caso el 2222) y establecemos la clave SSH con la que vamos a trabajar. En segundo lugar, establecemos la IP y el usuario que tendrá la máquina (en nuestro caso lo hemos llamado *vagrant*).


Por otra parte, en el fichero *VagrantFile*, debemos **indicar el provisionamiento para dicha máquina**. Para ello, le indicamos el fichero *playbook* que queremos ejecutar, el cuál contiene el provisionamiento que queremos que tenga la máquina virtual que hemos especificado anteriormente. Como vemos en el contenido del fichero *VagrantFile* (mostrado a continuación), ya estamos haciendo uso de Ansible para poder llevar a cabo dicha tarea.

**Contenido final del fichero *VagrantFile*:**
~~~
Vagrant.configure("2") do |config|
  config.vm.box = "debian/contrib-stretch64"
  config.vm.hostname = "ubuntuAndrea"

  config.vm.provision "ansible" do |ansible|
    ansible.verbose = "v"
    ansible.playbook = "playbook.yml"
  end
end
~~~


Podemos destacar, del fichero anterior, tres aspectos principales:
- La sección de provisionamiento hace referencia a un playbook de ansible al que en el fichero *VagrantFile* hemos llamado *playbook.yml*.
- Vagrant ejecutará el fichero de provisionamiento  que hemos definido una vez que la máquina virtual arranca y tiene acceso a SSH (o bien cuando ejecutemos explícitamente el provisionamiento).
- El hecho de tener activada la opción verbose va a provocar que se nos muestre más información del comando del Ansible playbook que utilicemos. Todavía no sabemos qué nos mostrará, entonces la voy a dejar de momento, y más adelante ya veremos si se quita del fichero o no.



**Fichero playbook.yml**
Para entender bien el funcionamiento de un playbook de ansible, y sobretodo, qué hace exactamente y de qué forma, podemos consultar el apartado correspondiente en la guía oficial [aquí](https://docs.ansible.com/ansible/2.7/user_guide/playbooks_intro.html). Además, se sugiere consultar este otro [enlace](https://github.com/ansible/ansible-examples), pues contiene una serie de ejemplos y buenas prácticas que se pueden llevar a cabo. De estos dos enlaces, es de donde nos basaremos para llevar a cabo este apartado.

<!-- - Lo primero: python3 [aquí](https://medium.com/@perwagnernielsen/ansible-tutorial-part-2-installing-packages-41d3ab28337d) -->
Para la creación del playbook, y su contenido, me he inspirado en el tutorial al que se puede acceder desde [aquí](https://medium.com/@perwagnernielsen/ansible-tutorial-part-2-installing-packages-41d3ab28337d).

Como ya hemos comentado, para crear la máquina virtual hemos utilizado una máquina Debian con Python 3, que ha sido escogida debido a que de esta forma, no solo contamos con Python instalado en la máquina, sino que por defecto ya trae consigo Python 3, tal y como se puede consultar [aquí](https://linuxconfig.org/how-to-change-default-python-version-on-debian-9-stretch-linux).

En primer lugar, el archivo playbook.yml va a representar únicamente a aquellas cosas genéricas que queramos instalar en una máquina virtual. Por tanto, tendríamos que instalar varios módulos indispensables para nuestro servicio web de la práctica anterior, las cuáles obtendremos a través del gestor de paquetes **apt**:
- **Git**: nos hace falta para poder acceder a nuestro proyecto desde la máquina virtual que hemos creado mediante Vagrant.. Sin git, entre otras cosas, no podremos hacer clone de nuestro repositorio, por lo que es esencial en este caso.

- **python-pip**: para poder hacer uso de pip. Se ha comprobado experimentalmente, que para el funcionamiento correcto de pip3 desde ansible, se debe instalar pip, y posteriormente, indicar el ejecutable concreto de pip con el que queremos funcionar.

- **python3-pip**: para poder utilizar pip3 y descargar aquello que necesitemos para la versión 3 de Python. Es necesario porque voy a instalar los requerimientos para poder ejecutar mi proyecto en la máquina de esa forma. Como estamos trabajando con Python 3, queremos pip 3 concretamente.

- **python-setuptools**: necesario para poder ejecutar el fichero *requirements.txt*. Este paquete fue añadido posteriormente, ya que uno de los errores obtenidos al intentar provisionar la máquina indicaba la necesidad de disponer de este paquete.

- **upgrade pip**: al probar el funcionamiento del playbook en la máquina de Azure, se sugiere que los mensajes de Warning actualizar a la última versión de Pip. Por ello, se ha añadido esta última orden al playbook.


Hasta aquí tendríamos todas las utilidades generales necesarias que deben existir en la máquina virtual de forma que podamos ejecutar nuestra aplicación.



**Siguiendo las buenas prácticas....**

A pesar de que hay múltiples fuentes que defienden que un playbook debe ser un proceso cerrado (como por ejemplo [aquí](https://serverfault.com/questions/750856/how-to-run-multiple-playbooks-in-order-with-ansible)), esta afirmación no es compartida por el estándar de buenas prácticas de Ansible.

Si consultamos la guía de buenas prácticas de Ansible, podemos encontrar una sección llamada *Creating Reusable Playbooks*, a la cuál podemos acceder desde [aquí](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse.html). En ella podemos ver, que es preferible reutilizar distintos playbooks, en lugar de empezar con uno de la forma que vimos arriba. Por ello, la parte específica de lo que queremos ejecutar, la vamos a especificar en un segundo playbook, que contendrá todos aquello que sea específico para poder ejecutar y desplegar nuestro proyecto:

- **git clone**: para poder descargar nuestro repositorio en la máquina virtual.

- **Dependencias específicas de la aplicación**: en este caso, aquello que sea imprescindible para el correcto funcionamiento del servicio web.


Por tanto utilizaremos un nuevo fichero, al que hemos llamado *especific_playbook.yml*,
el cuál se encargará de incorporar aquellos aspectos esenciales.

Nos quedaría por resolver cómo llevar a cabo la inclusión del playbook con el contenido específico que queremos incorporar. Para ello, hay múltiples formas, como podemos observar en la documentación oficial disponible [aquí](https://docs.ansible.com/ansible/2.4/playbooks_reuse_includes.html). La principal duda estaría en... ¿qué utilizar? ¿es preferible utilizar *include*  para incorporar otros playbooks al playbook principal?¿O es mejor si utilizamos *import*? Al final, ninguna de las opciones principales de la documentación es la solución, sino que lo preferible, en este momento, es hacer uso de *import_playbook*, pensada para poder ser utilizada en las futuras versiones de ansible. Esta información la podemos obtener si provisionamos la máquina indicando -v en la opción verbose de *VagrantFile*.

![Preferible usar import_playbook](https://raw.githubusercontent.com/andreamorgar/ejerciciosCC/master/images/razonImport.png)


Por tanto, el contenido final de nuestro playbook principal quedaría de la siguiente manera. Como se puede observar, este playbook principal, importa al playbook con la configuración específica relativa a mi proyecto, por lo tanto, es suficiente con llamar a este fichero desde *VagrantFile*.

~~~
---
- hosts: all
  become: yes
  gather_facts: False
  tasks:
    - name: Install base packages
      apt:
        name: ['git', 'python-pip', 'python3-pip', 'python-setuptools']
        state: present
      tags:
        - packages

    - name: Upgrade pip
      pip: name=pip state=latest
      tags:
        - packages

- import_playbook: specific_playbook.yml

~~~

**Fichero specific_playbook.yml**

Como se ha indicado anteriormente, en este playbook nos encargaremos del provisionamiento que es específico a la aplicación que queremos desplegar. Por ello, tendrá dos cosas esenciales:

- **Clonación del proyecto**: tenemos que clonar nuestro proyecto en la máquina virtual en cuestión. Esta acción podemos llevarla a cabo sin problemas, ya que como vimos anteriormente, se ha instalado *git*. Podemos especificar el nombre con el que queremos que se nos guarde el repositorio, y además debemos especificar **clone: yes** en la clonación. Los pasos seguidos se pueden ver en la documentación de Ansible [aquí](https://docs.ansible.com/ansible/2.5/modules/git_module.html).

- **Instalación de los paquetes definidos en requirements.txt**. Este paso lo llevaremos a cabo mediante **pip**. Para ello, especificamos que instale en su última versión, el contenido que tenga el fichero *requirements.txt*. Para poder llegar hasta el contenido de este fichero, podemos poner la ruta concreta. En este caso, el usuario que estamos utilizando es *vagrant*, por lo que éste es el que debe estar en la ruta hasta llegar al fichero de requirements. Por último, debemos indicar de que, de los distintos ejecutables de pip que están instalados en el sistema, coja *pip3*.

- **Redirección del puerto 5000 al 80**. Como nuestra aplicación se ejecuta en el puerto 5000, pero para la correción debe ejecutarse en el 80, se ha realizado una redirección de forma que el tráfico del puerto 5000 sea dirigido al puerto 80, y así poder ejecutar nuestra aplicación por dicho puerto. Como vemos, este es un claro caso de la utilidad de usar ficheros específicos, ya que no tendría sentido ejecutar esta orden en un fichero genérico (estamos hablando de un cambio muy concreto referente a la ejecución del proyecto).

Para ver el contenido del fichero *specific_playbook.yml* pincha [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/provision/vagrant/specific_playbook.yml)








Una vez completado el fichero *VagrantFile*, podemos provisionar la máquina virtual  con la siguiente orden:
~~~
$ vagrant provision
~~~
Ejecutamos dicha orden para provisionar la máquina que previamente hemos creado, y podemos comprobar que efectivamente se ha llevado a cabo el provisionamiento en la siguiente imagen. Como la información que se muestra por la terminal es muy extensa, solo voy a mostrar el resultado final, donde se observa que ha finalizado de forma correcta.

![Acceso por ssh a la máquina que hemos creado](https://raw.githubusercontent.com/andreamorgar/ejerciciosCC/master/images/hito3/provision.png)

De hecho, si accedemos de nuevo a la máquina mediante SSH, y volvemos a consultar la versión de aquello con lo que hemos provisionado la máquina, podemos ver cómo ahora sí está instalado todo lo necesario. Podemos apreciar este hecho en la siguiente imagen.  Como se observa, ahora sí está **git** instalado, al igual que **pip3**. Si hacemos ls, podemos ver cómo el proyecto se ha clonado en el directorio actual.
![Acceso por ssh a la máquina que hemos creado](https://raw.githubusercontent.com/andreamorgar/ejerciciosCC/master/images/hito3/nuevaProvision.png)




Por último mencionar, que de la forma que ha quedado el fichero *VagrantFile*, ya se provisionaría cualquier máquina que se crease mediante la orden:
~~~
$ vagrant up
~~~

**Es decir, se ha configurado el fichero VagrantFile de forma que cualquier máquina que creemos utilizando el mismo, se provisionará con lo que especificado en el fichero *playbook.yml*.**


**Comprobación del provisionamiento.**
Finalmente, nos quedaría por comprobar si finalmente se ha realizado el provisionamiento de manera correcta. Para ello, vamos a acceder al proyecto, el cuál hemos clonado en la máquina virtual, y vamos a comprobar el funcionamiento del servicio.  

En primer lugar, mediante SSH, nos situamos en el repositorio local del proyecto (en la máquina virtual), y encendemos el servicio. Desde otra terminal, volvemos a conectarnos a la máquina virtual mediante SSH y realizamos una petición al mismo. Podemos ver que funciona de manera correcta en la siguiente imagen.


![Funcionamiento del servicio](https://raw.githubusercontent.com/andreamorgar/ProyectoCC/master/docs/images/ejecucion_servicio.png)




---


## *Ansible* para provisionar una máquina virtual en Azure

### Instalación de las herramientas necesarias
En primer lugar, nos instalamos el cliente de Azure tal y como viene indicado en la documentación oficial, que se puede consultar [aquí](https://docs.microsoft.com/es-es/cli/azure/install-azure-cli?view=azure-cli-latest). Una vez que lo instalemos, ya podremos crear la máquina virtual desde la terminal. El realizarlo desde la terminal simplifica mucho el proceso, además de ser mucho más rápido, ya que podemos directamente especificar todo lo que queremos en nuestra máquina virtual, en lugar de ir recorriendo una gran cantidad de pasos sobre los que al final no se realiza ninguna modificación.


### Creación de la máquina virtual
Para crear una máquina virtual, se han seguido los pasos indicados en la documentación oficial, la cuál se puede consultar [aquí](https://docs.microsoft.com/es-es/azure/virtual-network/quick-create-cli?toc=%2Fazure%2Fvirtual-machines%2Flinux%2Ftoc.json). De forma resumida, hay que ejecutar tres órdenes:
1. Una orden que nos permita conectarnos a nuestra cuenta. Al ejecutar dicha orden, se nos abre el navegador en la página de inicio de sesión de Azure.

2. Una orden para poder crear una máquina virtual. En ella especificamos varios aspectos: el grupo de recursos, el usuario que existirá en dicha máquina, especificar que se utilice clave SSH y por último, la imagen de SO que queremos utilizar. En este caso, se ha cogido Ubuntu Server, ya que era la que inicialmente se pretendía utilizar (ya se ha comentado anteriormente).

3. Una orden para poder hacer uso del puerto 80, tal y como viene indicado en la documentación oficial, que se puede consultar [aquí](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/nsg-quickstart). Además, si recordamos,  la aplicación se programó para ejecutarse inicialmente en el puerto 5000. Si queremos que se ejecute en este puerto, deberíamos ejecutar de nuevo la orden correspondiente, pero esta vez para el puerto 5000.

Para ello, ejecutamos lo siguiente:
~~~
$ az login
$ az vm create --resource-group myResourceGroup --admin-username andreamg --name ubuntuAndrea --image UbuntuLTS --generate-ssh-keys
$ az vm open-port --resource-group myResourceGroup --name ubuntuAndrea --port 80
~~~

Por último, debemos realizar un pequeño cambio, y es que la IP, por defecto, se configura de manera dinámica. Debemos especificar, en la configuración de la máquina en Azure, que queremos que sea estática para que no varíe cada vez que se inicie la máquina.

Con esto, tendríamos ya creada la máquina virtual con las especificaciones anteriores. Podemos ver en la siguiente imagen cómo efectivamente se ha creado dicha máquina.
![Creación de una máquina virtual](https://raw.githubusercontent.com/andreamorgar/ProyectoCC/master/docs/images/maquina_azure.png)


### Provisionamiento de la máquina virtual

Una vez que tenemos la máquina creada, procedemos a provisionarla. El proceso llevado a cabo para la creación del playbook, es igual al caso de Vagrant, anteriormente documentado, por lo que para mayor detalle, podemos consultar directamente dicha documentación, a la que podemos acceder desde [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/docs/info_playbook.md).

En realidad, las modificaciones llevadas a cabo para poder provisionar la máquina virtual en Azure se encuentran en el fichero  [ansible_hosts](https://github.com/andreamorgar/ProyectoCC/blob/master/provision/azure/ansible_hosts).

En él, debemos realizar los siguientes cambios:
- Modificar el puerto al 22, para poder hacer uso de SSH.
- Modificar el valor de la variable **ansible_ssh_host** a la IP de nuestra máquina (en mi caso sería 137.117.174.154)
- Modificar el valor de la variable **ansible_ssh_user** al del usuario que hemos creado para la máquina (en mi caso, andreamg).

Tras realizar estos cambios, podemos ejecutar la siguiente orden para provisionar la máquina:
~~~
$ ansible-playbook -i ansible_hosts -b playbook.yml

~~~

Podemos ver, en la siguiente imagen, como algunas de las funcionalidades que no se instalan por defecto en la imagen utilizada, se han instalado. Además, se ha clonado el proyecto desde Github de forma correcta, lo que nos indica que se ha realizado la provisión de manera adecuada.
![Comprobación Provisionamiento máquina virtual de Azure](https://raw.githubusercontent.com/andreamorgar/ProyectoCC/master/docs/images/compr_prov_azure.png)


A continuación, podemos ver cómo efectivamente funciona. Además, si nos fijamos, está funcionando a través del puerto 80, tal y como se requiere en las especificaciones de este hito.

![Prueba del servicio en la máquina virtual de Azure](https://raw.githubusercontent.com/andreamorgar/ProyectoCC/master/docs/images/prueba_azure.png)





### Comprobación del provisionamiento en otra máquina  <a name="id7"></a>

Hecho por @adrianmorente, puede consultarse en [este fichero](./docs/comprobacion_provision.md).

### Comprobación del provisionamiento de otro compañero en mi máquina <a name="id8"></a>
Se ha comprobado que el provisionamiento realizado por @adrianmorente funciona de manera correcta. Puede consultarse [aquí](./docs/comprobacion_otra_provision.md).

---


### Últimos avances en el proyecto <a name="id9"></a>
Para el hito 3, se ha avanzado el proyecto añadiendo persistencia a los datos que utiliza el servicio. Para ello, se ha añadido una base de datos con [mLab](https://mlab.com/).

#### Base de datos para el servicio

##### Instalación de las herramientas necesarias
Como avance del proyecto, se ha añadido una base de datos donde guardar las predicciones que se van añadiendo al servicio mediante PUT. Obviamente, también se permitirá el acceso, modificación y borrado de dichas predicciones. Para ello, se ha hecho uso de [mLab](https://mlab.com/), una  *Database-as-a-Service* para *MongoDB* (la herramienta que se decidió utilizar para ello).


Como estamos programando el proyecto en Python, debemos instalar *pymongo* para poder trabajar con mLab. Esto podemos hacerlo ejecutando la siguiente orden.


~~~
$ pip3 install pymongo
~~~

Sin embargo, hay que tener en cuenta un detalle, y es que le hemos añadido una nueva librería a nuestro servicio. Esto implica, que debe ir añadida en *requirements.txt* para que nuestra aplicación pueda pasar los tests y desplegarse de forma correcta. [Aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/requirements.txt) se puede acceder al fichero *requirements.txt* ya actualizado.

##### Funcionalidad añadida

Para poder llevar a cabo el añadido de una base de datos, lo primero es crearse una cuenta en mLab, y crear la base de datos con la que se va a trabajar. Una vez completado estos pasos, podemos pasar a la parte de programación.

Se ha hecho uso de un fichero, al que se le ha denominado [predictionDB.py](https://github.com/andreamorgar/ProyectoCC/blob/master/predictionDB.py), en el cuál se han añadido todas las funciones necesarias para poder utilizar la base de datos que hemos creado. Las funciones creadas, son las siguientes:

- **getDocument(ID)**: devuelve un documento de la base de datos, cuyo ID coincida con el pasado por parámetro. Este documento se corresponde con una predicción concreta con la que puede trabajar nuestro servicio.
- **pushDocument(document)**: añade el documento (predicción) *document* a la base de datos.
- **updateDocument(document,update)**: actualiza el documento (predicción) *document* con la información en *update*.
- **delete_document(document)**: borra de forma permanente el documento (predicción) *document* la base de datos.
- **get_all_predictions()**: devuelve un elemento de tipo cursor con todos los documentos (predicciones) almacenados en la base de datos en ese momento.
- **get_number_documents()**: devuelve el número de predicciones que hay actualmente en la base de datos
- **delete_all_documents()**: borra de forma permanente todos los documentos (predicciones) de la base de datos

Con las funciones anteriores, es suficiente para mantener la funcionalidad que teníamos en el hito anterior, con la diferencia de que ahora existe persistencia en los datos.




##### Modificación del fichero que implementa Flask
Se han modificado las distintas funciones utilizadas en el fichero que implementa el servicio Rest para que éste se comunique con la base de datos, mediante las funciones detalladas en la sección anterior. De esta forma, se ha prescindido de la estructura de tipo vector que almacenaba de forma temporal las predicciones de la base de datos en las ejecuciones del servicio previas al avance. Se puede ver el contenido actual del fichero que implementa el servicio de la aplicación [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/app_flask.py)


##### Funcionamiento de la base de datos
Podemos ver en la siguiente imagen cómo se vería la base de datos y sus documentos (que como ya hemos mencionado, representan las distintas predicciones). En dicha imagen podemos ver cómo se ha hecho PUT de dos predicciones, las cuáles, (tras refrescar mLab), podemos ver que están en una colección de la base de datos.
![Vista de la base de datos utilizada](./images/vista_mongo.png)

Podemos ahora intentar modificar la segunda predicción, mediante POST. Tal y como vemos en la siguiente imagen, el funcionamiento es correcto.
![Vista de la base de datos utilizada](./images/vistamongo_post.png)


De igual forma podemos ver el funcionamiento para DELETE. Vamos a probar a eliminar la primera predicción. En la imagen siguiente se puede ver cómo la acción es llevada a cabo de forma correcta.
![Vista de la base de datos utilizada](./images/vistamongo_delete.png)

Por último, vamos a imprimir las distintas predicciones que se encuentran en la base de datos, para comprobar que el acceso a la información de la base de datos se lleva a cabo de manera correcta. De nuevo, en la siguiente imagen, podemos ver que se lleva a cabo de manera correcta.
![Vista de la base de datos utilizada](./images/vista_mongo_get.png)



##### Testeo de la nueva funcionalidad
Se ha añadido al directorio *Test*, el fichero [test_database.py](https://github.com/andreamorgar/ProyectoCC/blob/master/test/test_database.py), un test que se encarga de probar el funcionamiento correcto de cada una de las funciones de la base de datos detalladas anteriormente. Este test, se añade a todos los que teníamos anteriormente, a la hora de desplegar el proyecto.

Como se ha dicho, comprueba que la gestión de la base de datos se realiza de forma adecuada. Ello implica, que la inserción, borrado, modificación y acceso a las predicciones se hace correctamente, además de otros aspectos como que el número de documentos en la base de datos sea correcto, que la información insertada sea la correcta y de la forma correcta, etc.

##### Información útil para este avance del proyecto
[Tutorial para usar mongo](https://datawookie.netlify.com/blog/2016/09/python-first-steps-with-mongodb/)


[Tutorial para usar mLab](https://gist.github.com/nikhilkumarsingh/a50def43d8d425b4108c2f76edc1398e)





---
### Licencia <a name="id10"></a>
Este software se desarrollará bajo la licencia GNU General Public License v3.0
