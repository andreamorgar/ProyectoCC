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
  - [Avance en el proyecto](#id9)
- [Automatización de la creación de máquinas virtuales](#id10)  
- [Licencia](#id11)



### Descripción del proyecto <a name="id1"></a>

En este proyecto, se pretende hacer un pequeño análisis de la información actualizada que nos proporciona la [API](https://opendata.aemet.es/centrodedescargas/inicio) de la **Agencia Estatal Española de Meteorología**. De esta forma, se pretende procesar la información de la misma, mostrando aquella más trascendental para los usuarios de Granada en distintas plataformas.

A través de la API de dicha plataforma, se va a acceder a la información más actualizada, y se irá almacenando, de entre dicha información, aquella que en términos generales interesa más a los usuarios.


Se pretende abordar dicho análisis de información en distintos ámbitos. Por una parte, la posibilidad de acceder a la temperatura actual, los centímetros cúbicos registrados, o la temperatura más alta/baja detectada durante ese día. En segundo lugar, proporcionar distintos análisis semanales y mensuales a partir de la información obtenida a partir de los datos actualizados que se van proporcionando a lo largo del tiempo. Este último análisis tiene su interés, ya que las estructuras de datos facilitadas a nivel semanal/mensual son menos específicas en cuanto a la información mostrada diariamente, y puede que haya aspectos de la información diaria de interés para el usuario a nivel semanal o mensual, y que actualmente vea restringido su acceso a dichos datos.


Los usuarios podrán acceder a toda la información que se analice mediante dos formas:
* A través de **Twitter**: se publicarán diversos tweets con la información más importante que se ha ido recabando.
* A través de un bot de **Telegram** también se podrá acceder a la información más relevante.


De esta forma, se pretende facilitar al usuario la consulta de la información más trascendental de una forma sencilla y rápida a través de plataformas utilizadas diariamente por millones de usuarios, como es el caso de las redes sociales mencionadas anteriormente.



### Arquitectura <a name="id2"></a>
Se va a utilizar una arquitectura basada en microservicios en sustitución a una arquitectura monolítica. De este modo podremos realizar y modificar cambios en el software de forma sencilla e independiente, aprovechando las ventajas que nos aporta este tipo de arquitecturas, como pueden ser:
* Versatilidad
* Autonomía: podemos actualizar un microservicio sin que dependa de los demás
* Facilidades de integración
* Aislamiento de errores: un fallo en un microservicio afectará al funcionamiento del mismo, y no tiene por qué afectar a las demás funcionalidades.

Tendremos así, una colección de distintos microservicios, donde cada uno se encargará de implementar una funcionalidad dentro de la totalidad del proyecto.

Los microservicios que se van a utilizar son los siguientes:.
* Un microservicio que se encargue de **acceder a la API de la AEMET y se encargue de procesar la información obtenida**.

* Un microservicio para **almacenar toda la información a manejar en una base de datos**.

* Un microservicio para realizar el **análisis de datos**.  de los valores medidos a lo largo del día o la semana que puedan ser de interés.

* Tendremos un **microservicio que se encargue de publicar tweets**, con información relevante obtenida (a través de [tweepy](http://www.tweepy.org/), y **otro microservicio diferente que consistirá en un bot de telegram** en el cuál podamos también poner a disposición del usuario aquellos datos que puedan ser de mayor importancia (en principio a través de [telebot](https://geekytheory.com/telegram-programando-un-bot-en-python)).

* Por último, existirá un **microservicio LOG**, con el que se comuniquen todos los microservicios anteriores.

Para la comunicación entre los distintos microservicios, se realizará mediante brokers. En este caso, el broker a utilizar será [RabbitMQ](https://www.rabbitmq.com/).

A continuación, en la siguiente imagen, se puede ver un pequeño esquema de los microservicios a utilizar:
![Esquema de los microservicios](https://raw.githubusercontent.com/andreamorgar/ProyectoCC/master/docs/images/esquemaMicroservicios.png)

Puede consultar más información acerca de la arquitectura [aquí](./docs/info_arquitectura.md).



### Testeo y pruebas <a name="id3"></a>
Cada microservicio se testeará de forma individual, antes de desplegarlo en la nube. La realización de los tests se llevará a cabo mediante [TRAVIS](https://travis-ci.org/), y dichos tests se implementarán en Python (ya que es el lenguaje utilizado en el microservicio) con ayuda de la librería [unittest](https://docs.python.org/3/library/unittest.html).


### Framework y lenguaje a utilizar <a name="id4"></a>
Se va a utilizar como lenguaje de programación [Python](https://www.python.org) y [Flask](http://flask.pocoo.org/) como microservicio. Además, el proyecto será desplegado en Azure.



### Desplegar el proyecto <a name="id5"></a>

Despliegue: https://agile-mountain-82339.herokuapp.com/

Se ha realizado un despliegue del servicio web, realizada en el PaaS [Heroku](https://www.heroku.com/). Para ello se han seguido una serie de pasos, que se pueden encontrar [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/docs/info_despliegue.md), donde se hace un breve repaso de todo el procedimiento que se ha seguido desde el funcionamiento del servicio en _localhost_ hasta su despliegue en Heroku con las comprobaciones correspondientes. También se puede apreciar en ese fichero todas las decisiones tomadas para llevar a cabo el procedimiento.

---
### Provisionamiento de máquina virtuales <a name="id6"></a>

En este documento se detallan los distintos pasos seguidos hasta conseguir provisionar una máquina virtual (primero a nivel local y posteriormente en Azure), con todo lo necesario para poder ejecutar en ella nuestro proyecto. Para ello, se seguirán los siguientes pasos:

1. Uso de *Vagrant* y *Ansible* para provisionar una máquina virtual desde local.

2. Uso de *Ansible* para provisionar una máquina virtual en la plataforma *Azure*.

Más información [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/provision/README.md).

MV: 137.117.174.154


#### Comprobación del provisionamiento en otra máquina <a name="id7"></a>

Hecho por @adrianmorente, puede consultarse en [este fichero](./docs/comprobacion_provision.md).

#### Comprobación del provisionamiento de otro compañero en mi máquina <a name="id8"></a>
Se ha comprobado que el provisionamiento realizado por @adrianmorente funciona de manera correcta. Puede consultarse [aquí](./docs/comprobacion_otra_provision.md).


#### Últimos avances en el proyecto <a name="id9"></a>
Para el hito 3, se ha avanzado el proyecto añadiendo persistencia a los datos que utiliza el servicio. Para ello, se ha añadido una base de datos con [mLab](https://mlab.com/). A la documentación de esta avance en el proyecto se puede acceder [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/docs/info_avance_basedatos.md).

Por supuesto, se han añadido todos los tests necesarios para asegurar el funcionamiento correcto de esta nueva funcionalidad.

---


### Automatización de la creación de máquinas virtuales desde línea de órdenes <a name="id10"></a>


---


### Licencia <a name="id11"></a>
Este software se desarrollará bajo la licencia GNU General Public License v3.0
