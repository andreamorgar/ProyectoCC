# Contenedores para despliegue en la nube

## Instalación
El primer paso a seguir es instalar Docker en caso de que no lo hayamos hecho ya previamente. Los pasos que tenemos que seguir para ello se pueden encontrar en la [documentación oficial](https://docs.docker.com/install/linux/docker-ce/ubuntu/), y se encuentran realizados paso por paso [aquí](./instalacion_docker.md)



## Fichero Dockerfile

Para definir las imágenes con las que queremos trabajar, necesitaremos definirlas en el fichero [Dockerfile](https://github.com/andreamorgar/ProyectoCC/blob/master/Dockerfile). En este fichero, partimos de una imagen base (que podemos coger por ejemplo de Docker Hub), y la personalizamos añadiendo todo lo necesario para que nuestro proyecto pueda ejecutarse, con normalidad, posteriormente en un contenedor. Además, se indicará todo aquello necesario para ejecutar nuestro proyecto, como puede ser, lanzarlo directamente desde Dockerfile.


### Organización de los microservicios
En nuestro caso, cabe destacar que, en primer lugar, únicamente necesitaremos trabajar con una imagen, la cuál será la que se encargue de ejecutar el servicio. Desde este servicio, accederemos a la base de datos, que dispone del contenido asociado a las distintas rutas con las que trabajamos en este proyecto. Para la base de datos, utilizamos **mLab**, de forma que únicamente tendremos que conectarnos, de la manera adecuada, desde el fichero que realiza toda la gestión de la base de datos.

### Selección de la imagen
Entonces, la primera decisión importante que tenemos que tomar en este punto, es la elección de una imagen adecuada para dicho contenedor. En este caso, tal y como hemos visto en clase, estamos buscando una imagen que sea ligera, y a ser posible, que se asemeje en cuanto a provisionamiento inicial, a aquello que necesito en el proyecto. En mi caso, voy a buscar máquinas que tengan *python3* instalado.

Como he comentado en el párrafo anterior, nos vamos a centrar en imágenes que sean ligeras, por lo que limité mi elección en dos que cumpliesen dicha característica: **Alpine** y **Debian Slim**.

En la siguiente imagen se puede ver la lista de algunas de las imágenes que he descargado o generado, con algunas características como es el caso del tamaño que ocupa cada una de ellas. Tal y como puede observarse, en la imagen (concretamente la fila señalada), podemos ver, que en el caso de la imagen que hemos utilizado con Debian Slim (y Python3 incluido) el tamaño es muy superior al resto, sobretodo si lo comparamos con las imágenes Alpine en dicha lista. Podemos acceder al enlace de dicho hito [aquí](https://hub.docker.com/r/ecoron/python36-jessie-slim).

Además, podemos ver cómo hay una gran diferencia entre la imagen Alpine (con Python3), respecto a Debian Slim, por ello, la decisión de la imagen ha venido influenciada mayoritariamente por este factor. Además, se han tenido en cuenta otras razones, como puede ser, las cuestiones de seguridad, que no han sido realmente controladas a nivel de imagen a utilizar hasta este momento. Una de las ventajas de ocupar poco, es que hay menos donde atacar. En nuestro caso, con un servicio tan simple, lo que proporciona Alpine es más que suficiente ([ver](https://nickjanetakis.com/blog/the-3-biggest-wins-when-using-alpine-as-a-base-docker-image)). Todas estos aspectos en conjunto, han derivado en que finalmente utilice una imagen Alpine con Python3, descargada desde Docker hub.


<p align="center"><img alt="Tamaño Debian Slim" width="1000px" src="./images/hito6/12_tamanios_maquinas.png" /></p>



## Ejecutar un contenedor

- Tal y como podemos ver en la [documentación oficial](https://docs.docker.com/install/linux/docker-ce/ubuntu/), como los recursos de red están virtualizados dentro del entorno que definimos, tendremos que mapear los puertos utilizados a aquellos desde los que queramos trabajar en nuestra máquina local.


### Pruebo debianSlim:

Cojo la imagen de [aquí](https://hub.docker.com/r/ecoron/python36-jessie-slim).

<p align="center"><img alt="Docker Debian Slim" width="1000px" src="./images/hito6/prueba_debian_slim.png" /></p>



<p align="center"><img alt="Tamaño Debian Slim" width="1000px" src="./images/hito6/ver_tam_imagen_debianslim.png" /></p>



---

### Comandos utilizados importantes

`sudo docker images`: para listar las imágenes que tenemos instaladas

`sudo docker run -it alpine sh`:  

`docker image rm ID`: para borrar una imagen [ver]https://linuxize.com/post/how-to-remove-docker-images-containers-volumes-and-networks/


### Algunos conceptos sobre Docker
- Con el dockerfile defines una imagen
- Desde docker podemos usar imágenes ya publicadas. Nosotras buscamos crear nuestra imagen propia.
- En el dockerfile se puede hacer la provisión como ansible.


Dockerfile -> imagen -> contenedor

Imagen: el SO con lo que definimos en dockerfile

Contenedor: es la ejecución de una imagen. CUando ejecutas una imagen se crea un contenedor.



### dockerfile
https://docs.docker.com/get-started/part2/


### Test Dockerfile


https://medium.com/@aelsabbahy/tutorial-how-to-test-your-docker-image-in-half-a-second-bbd13e06a4a9



## Alpine + MongoDB

He cogido la imagen de [aqui](https://hub.docker.com/r/mvertes/alpine-mongo/). Ahi viene como usar MongoDB

### Justificación
