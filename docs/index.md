# Proyecto Cloud Computing
## Autora: Andrea Morales Garzón

### Prácticas de la asignatura Cloud Computing del Máster de Ingeniería Informática para el curso 2018/2019

## Proyecto a desarrollar
Estudio de las condiciones meteorológicas en Granada a través de la información facilitada por la Agencia Estatal Española de Meteorología ([AEMET](http://www.aemet.es/es/portada))


### Descripción del proyecto

En este proyecto, se pretende hacer un pequeño análisis de la información actualizada que nos proporciona la [API](https://opendata.aemet.es/centrodedescargas/inicio) de la **Agencia Estatal Española de Meteorología**. De esta forma, se pretende procesar la información de la misma, mostrando aquella más trascendental para los usuarios de Granada en distintas plataformas.

A través de la API de dicha plataforma, se va a acceder a la información más actualizada, y se irá almacenando, de entre dicha información, aquella que en términos generales interesa más a los usuarios.


Se pretende abordar dicho análisis de información en distintos ámbitos. Por una parte, la posibilidad de acceder a la temperatura actual, los centímetros cúbicos registrados, o la temperatura más alta/baja detectada durante ese día. En segundo lugar, proporcionar distintos análisis semanales y mensuales a partir de la información obtenida a partir de los datos actualizados que se van proporcionando a lo largo del tiempo. Este último análisis tiene su interés, ya que las estructuras de datos facilitadas a nivel semanal/mensual son menos específicas en cuanto a la información mostrada diariamente, y puede que haya aspectos de la información diaria de interés para el usuario a nivel semanal o mensual, y que actualmente vea restringido su acceso a dichos datos.


Los usuarios podrán acceder a toda la información que se analice mediante dos formas:
* A través de **Twitter**: se publicarán diversos tweets con la información más importante que se ha ido recabando.
* A través de un bot de **Telegram** también se podrá acceder a la información más relevante.


De esta forma, se pretende facilitar al usuario la consulta de la información más trascendental de una forma sencilla y rápida a través de plataformas utilizadas diariamente por millones de usuarios, como es el caso de las redes sociales mencionadas anteriormente.



### Arquitectura
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

#### Testeo y pruebas
Cada microservicio se testeará de forma individual, previo a su despliegue en la nube. La realización de los tests se llevará a cabo mediante [TRAVIS](https://travis-ci.org/), y dichos tests se implementarán en Python (ya que es el lenguaje utilizado en el microservicio) con ayuda de la librería [unittest]https://docs.python.org/3/library/unittest.html).

### Framework y lenguaje a utilizar
Se va a utilizar como lenguaje de programación [Python](https://www.python.org) y [Flask](http://flask.pocoo.org/) como microservicio. Además, el proyecto será desplegado en Azure.


### Despliegue
Se ha realizado un despliegue del servicio web, realizada en el PaaS [Heroku](https://www.heroku.com/). Para ello se han seguido una serie de pasos, que se pueden encontrar [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/docs/info_despliegue.md), donde se hace un breve repaso de todo el procedimiento que se ha seguido desde el funcionamiento del servicio en _localhost_ hasta su despliegue en Heroku con las comprobaciones correspondientes. También se puede apreciar en ese fichero todas las decisiones tomadas para llevar a cabo el procedimiento.

despliegue https://agile-mountain-82339.herokuapp.com/

### Licencia
Este software se desarrollará bajo la licencia GNU General Public License v3.0
