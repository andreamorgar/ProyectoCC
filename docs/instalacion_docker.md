## Pasos para instalar Docker

En primer lugar actualizamos e instalamos todo lo necesario, de la forma que viene a continuación. Además, añadimos la clave necesaria.

~~~
$ sudo apt-get update

$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common

$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

$ sudo apt-key fingerprint 0EBFCD88

~~~
<!--
<p align="center"><img alt="Docker Hello World" width="1000px" src="./images/hito6/docker_finger_print.png" /></p> -->

~~~

$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"


$ sudo apt-get update

$ sudo apt-get install docker-ce
~~~


Por último, vamos a verificar que Docker se ha instalado de forma correcta con la imagen `hello-world`. Para ello, ejecutamos la orden que se muestra a continuación.
~~~

$ sudo docker run hello-world

~~~

En esta imagen podemos ver, cómo efectivamente funciona y hemos creado un contenedor con dicha imagen, cuya ejecución se puede ver en la siguiente captura de pantalla.
<p align="center"><img alt="Docker Hello World" width="1000px" src="./images/hito6/docker_hello_word.png" /></p>
