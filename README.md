# Proyecto Cloud Computing 
## Autora: Andrea Morales Garzón

### Prácticas de la asignatura Cloud Computing del Máster de Ingeniería Informática para el curso 2018/2019

## Proyecto a desarrollar
Estudio de las condiciones meteorológicas en Granada a través de la información facilitada por la Agencia Estatal Española de Meteorología ([AEMET](http://www.aemet.es/es/portada))


### Descripción del proyecto 

En este proyecto, se pretende hacer un pequeño análisis de la información actualizada que nos proporciona la [API](https://opendata.aemet.es/centrodedescargas/inicio) de la **Agencia Estatal Española de Meteorología**. De esta forma, se pretende procesar la información de la misma, mostrando aquella más trascendental para los usuarios de Granada en distintas plataformas. 

A través de la API de dicha plataforma, se va a acceder a la información más actualizada, y se irá almacenando, de entre dicha información, aquella que en términos generales interesa más a los usuarios. 

[comment]: # (Esta información puede ser, la temperatura actual, los centímetros cúbicos registrados, o la temperatura más alta/baja detectada durante ese día). 

Se pretende abordar dicho análisis de información en distintos ámbitos. Por una parte, la posibilidad de acceder a la temperatura actual, los centímetros cúbicos registrados, o la temperatura más alta/baja detectada durante ese día. En segundo lugar, proporcionar distintos análisis semanales y mensuales a partir de la información obtenida a partir de los datos actualizados que se van proporcionando a lo largo del tiempo. Este último análisis tiene su interés, ya que las estructuras de datos facilitadas a nivel semanal/mensual son menos específicas en cuanto a la información mostrada diariamente, y puede que haya aspectos de la información diaria de interés para el usuario a nivel semanal o mensual, y que actualmente vea restringido su acceso a dichos datos. 


Los usuarios podrán acceder a toda la información que se analice mediante dos formas:
* A través de *Twitter*: se publicarán diversos tweets con la información más importante que se ha ido recabando. 
* A través de un bot de *Telegram* también se podrá acceder a la información más relevante. 

De esta forma, se pretende facilitar al usuario la consulta de la información más trascendental de una forma sencilla y rápida a través de plataformas utilizadas diariamente por millones de usuarios, como es el caso de las redes sociales mencionadas anteriormente. 



### Arquitectura 
Se va a utilizar una arquitectura basada en microservicios. De este modo, podremos realizar y modificar cambios en el software de forma sencilla e independiente, aprovechando las ventajas que nos aporta este tipo de arquitecturas, como puede ser la versatilidad y las facilidades de integración. 


### Framework y lenguaje a utilizar
Se va a utilizar como lenguaje de programación Python y Flask como microservicio. 


### Referencias 

* [Python](https://www.python.org)
* [Flask](http://flask.pocoo.org/)



### Licencia
Este software se desarrollará bajo la licencia GNU General Public License v3.0 
