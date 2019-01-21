# Máquina con MongoDB local

Hasta ahora, habíamos trabajado con MongoDB a través de mLab, de manera que no habíamos necesitado alojar la base de datos en una máquina virtual adicional ( o incluso en una máquina virtual que alojara tanto el servicio REST implementado hasta el momento como la base de datos).


En este hito, vamos a prescindir de mLab y utilizar una nueva máquina virtual, de forma que la provisionaremos con todo lo necesario para poder alojar MongoDB en ella. Para ello, lo principal es modificar la forma en la que realizamos la conexión con el cliente de MongoDB, ya que donde antes nos conectábamos con mLab, a partir de este momento podremos realizarlo de la siguiente manera:
~~~
client = MongoClient("mongodb://<direccion> :27017/predictions")
~~~
De esta forma, podremos conectarnos con la base de datos en la máquina cuya IP se corresponda con <direccion>, a través del puerto 27017(que es el puerto por defecto para MongoDB), y usar una base de datos llamada *predictions* (que se crearía automáticamente en el caso de que no existiese).

### Conectar con la base de datos en una máquina diferente de la del servicio REST.
En nuestro caso, tenemos dos máquinas:
- Una máquina `maquinaservicio` con el servicio rest (IP: 10.0.0.4)
- Una máquina `maquinamongo` con MongoDB (IP: 10.0.0.5)

Por tanto, queremos que la máquina con el servicio rest (`maquinaservicio`) se conecte a la base de datos alojada en la máquina `maquinamongo` a través de la red interna a la que ambas pertenecen.

De esta forma, la máquina con la IP 10.0.0.4 accederá a la información de la base de datos de la máquina con dirección IP 10.0.0.5, (ésta segunda escuchará a la dirección de la primera máquina (permitiendo escuchar peticiones de 10.0.0.4).


#### Conectar a la base de datos de la máquina con IP interna 10.0.0.5
Esta cuestión es sencilla, ya que simplemente indicamos, cuando creamos el cliente, dicha dirección.


El único "problema" que podríamos tener, sería a la hora de pasar los test de travis, ya que en ese momento, no tendremos una máquina con la IP 10.0.0.5 a la que conectarnos. Tenemos, así de primeras, dos posibles soluciones:

1. Utilizar **variables de entorno**, que permitan en Travis escuchar en *localhost*, yen nuestro servicio en la IP que queramos establecer en dicha variable de entorno (o valor por defecto, de no estar declarada dicha variable)

2. Modificar desde Ansible o Vagrant la línea del fichero que establece la conexión con la base de datos, cambiando la dirección a la que nos interese.

Por simplicidad, **se ha elegido la primera opción, por lo que declaramos en Travis una variable de entorno, que será la que contenga el valor de la IP a utilizar.**

Además, se ha declarado en Python, que a la hora de coger el valor de la variable de entorno, si esta no está definida, coja un valor por defecto  para todos aquellos casos en los que la variable de entorno no exista. Este valor por defecto, he especificado que sea `10.0.0.5`, de forma que, cuando ejecutemos el proyecto en la máquina virtual de Azure, coja directamente el valor por defecto y  nos ahorremos tener que declarar variables de entorno en la máquina virtual.

A continuación podemos ver el código en Python asociado a este cambio.
<p align="center"><img alt="Image" width="1000px" src="./images/hito5/11_mongoClient.png" /></p>

#### Fichero *.travis.yml*
Además de establecer el valor para la variable de entorno `IP` previamente comentada,  para la correcta ejecución del proyecto, tendremos que instalar también un [servicio de MongoDB en Travis](https://docs.travis-ci.com/user/database-setup/#mongodb), de forma que pueda ejecutar la aplicación y testearla. A continuación se puede ver el contenido del fichero [.travis.yml](https://github.com/andreamorgar/ProyectoCC/blob/master/.travis.yml) tras los cambios comentados.

~~~
language: python
python:
- '3.5'
- '3.6'
services:
  - mongodb
env:
- IP='127.0.0.1'
install:
- pip install -r requirements.txt
script:
- python -m unittest discover test/
~~~


### Configurar MongoDB en una máquina virtual

Por último, quedaría por provisionar una máquina con todo lo necesario para poder ejecutar el servicio de base de datos. Para ello, se ha utilizado un playbook de ansible, que se encarga de descargar MongoDB, y configurarlo para que permita escuchar únicamente de las IPs que nos interesan.

Para ver todo el procedimiento asociado al provisionamiento (junto a su configuración concreta para el proyecto) de una máquina virtual con MongoDB, se puede acceder mediante [este enlace](https://github.com/andreamorgar/ProyectoCC/blob/master/docs/provisionamiento_mongo.md).
