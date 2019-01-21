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
  - [Comprobación del provisionamiento de otro compañero en mi máquina](#id8)
  - [Avance en el proyecto](#id9)
- [Automatización de la creación de máquinas virtuales](#id10)  
  - [Avance en el proyecto](#id11)
- [Orquestación de máquinas virtuales](#id13)
  - [Comprobación de mi provisionamiento en otra máquina](#id15)
  - [Comprobación del provisionamiento de otro compañero en mi máquina](#id16)
  - [Últimos avances en el proyecto](#id14)
- [Licencia](#id12)



### Descripción del proyecto <a name="id1"></a>

En este proyecto, se pretende hacer un pequeño análisis de la información actualizada que nos proporciona la [API](https://opendata.aemet.es/centrodedescargas/inicio) de la **Agencia Estatal Española de Meteorología**. De esta forma, se pretende procesar la información de la misma, mostrando aquella más trascendental para los usuarios de Granada en distintas plataformas.

A través de la API de dicha plataforma, se va a acceder a la información más actualizada, y se irá almacenando, de entre dicha información, aquella que en términos generales interesa más a los usuarios.


Se pretende abordar dicho análisis de información en distintos ámbitos. Por una parte, la posibilidad de acceder a la temperatura actual, los centímetros cúbicos registrados, o la temperatura más alta/baja detectada durante ese día. En segundo lugar, proporcionar distintos análisis semanales y mensuales a partir de la información obtenida a partir de los datos actualizados que se van proporcionando a lo largo del tiempo. Este último análisis tiene su interés, ya que las estructuras de datos facilitadas a nivel semanal/mensual son menos específicas en cuanto a la información mostrada diariamente, y puede que haya aspectos de la información diaria de interés para el usuario a nivel semanal o mensual, y que actualmente vea restringido su acceso a dichos datos.


Los usuarios podrán acceder a toda la información que se analice mediante dos formas:
* A través de **Twitter**: se publicarán diversos tweets con la información más importante que se ha ido recabando.
* A través de un bot de **Telegram** también se podrá acceder a la información más relevante.


De esta forma, se pretende facilitar al usuario la consulta de la información más trascendental de una forma sencilla y rápida a través de plataformas utilizadas diariamente por millones de usuarios, como es el caso de las redes sociales mencionadas anteriormente.



#### Arquitectura <a name="id2"></a>
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



#### Testeo y pruebas <a name="id3"></a>
Cada microservicio se testeará de forma individual, antes de desplegarlo en la nube. La realización de los tests se llevará a cabo mediante [TRAVIS](https://travis-ci.org/), y dichos tests se implementarán en Python (ya que es el lenguaje utilizado en el microservicio) con ayuda de la librería [unittest](https://docs.python.org/3/library/unittest.html).


#### Framework y lenguaje a utilizar <a name="id4"></a>
Se va a utilizar como lenguaje de programación [Python](https://www.python.org) y [Flask](http://flask.pocoo.org/) como microservicio. Además, el proyecto será desplegado en Azure.


---



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


#### Avances en el proyecto <a name="id9"></a>
Para el hito 3, se ha avanzado el proyecto añadiendo persistencia a los datos que utiliza el servicio. Para ello, se ha añadido una base de datos con [mLab](https://mlab.com/). A la documentación de esta avance en el proyecto se puede acceder [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/docs/info_avance_basedatos.md).

Por supuesto, se han añadido todos los tests necesarios para asegurar el funcionamiento correcto de esta nueva funcionalidad.

---


### Automatización de la creación de máquinas virtuales desde línea de órdenes <a name="id10"></a>
MV2: 40.89.191.234

Se ha desarrollado un script de aprovisionamiento y creación de máquinas virtuales, con el objetivo de automatizar esta tarea. Para ello, se ha utilizado el cliente de Azure (para poder crear la máquina virtual desde línea de órdenes) y ansible (para el posterior provisionamiento).

Por otra parte, se han contemplado y justificado distintas posibilidades a la hora de elegir algunos parámetros clave en la creación de máquinas virtuales en Azure, como puede ser la región, la imagen o el tamaño de la propia máquina virtual.

Se puede acceder a la información detallada en [este fichero](https://github.com/andreamorgar/ProyectoCC/blob/master/docs/automatizacion.md).

#### Avance en el proyecto  <a name="id11"></a>

Para este hito, vamos a realizar un avance en el proyecto, que consiste en añadir la utilidad de logs a nuestra aplicación.

Para ello, vamos a utilizar la librería **logging** de Python, que nos permitirá poder gestionar los distintos mensajes que se deban enviar en nuestra aplicación. Se puede consultar más información acerca del avance [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/docs/info_avance_logs.md).


---

### Orquestación de máquinas virtuales <a name="id13"></a>

Despliegue Vagrant: 20.188.33.145

En este hito, se ha realizado la orquestación de dos máquinas virtuales en Azure, donde una de las máquinas alojará la base de datos, y la otra, el servicio REST que estamos desarrollando (el cuál hace uso de dicha base de datos, ya que es de donde adquiere la información). Para ello, haremos uso de [Vagrant](https://www.vagrantup.com/), una herramienta para la creación y configuración de entornos de desarrollo.

Se puede acceder a la documentación de todo lo llevado a cabo [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/docs/orquestacion_mv.md).

#### Comprobación de mi provisionamiento en otra máquina <a name="id15"></a>

Realizado por @AlejandroCN7, puede consultarse en [este enlace](https://github.com/andreamorgar/ProyectoCC/blob/master/docs/Prueba-Orquestaci%C3%B3n-%20Alejandro_Campoy_Nieves.md).

#### Comprobación del provisionamiento de otro compañero en mi máquina <a name="id16"></a>
Se ha comprobado que el provisionamiento realizado por @AlejandroCN7 funciona de manera correcta. Puede consultarse [en este enlace](https://github.com/AlejandroCN7/Proyecto-Cloud-Computing/blob/master/docs/comprobacionOrquestacion.md).

#### Últimos avances en el proyecto  <a name="id14"></a>

Se ha llevado a cabo el provisionamiento de una máquina para poder disponer de MongoBD en local:
- Hasta ahora se utilizaba MongoDB desde mLab, por lo que se ha adaptado para poder ejecutarlo desde cualquier IP, ya sea localhost, o una que nosotros establezcamos.

- También se ha realizado el provisionamiento con ansible correspondiente, junto con la configuración del servicio asociado, para que, una vez finalizado el provisionamiento, tengamos el servicio correctamente configurado y lanzado.

A la documentación correspondiente a este avance se puede acceder desde [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/docs/avance_mongoDbLocal.md).

---


### Licencia <a name="id12"></a>
Este software se desarrollará bajo la licencia GNU General Public License v3.0
