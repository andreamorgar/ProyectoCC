
## Apache Bench para determinar la región en la que situar la máquina virtual

Para cada una de las regiones, hay que llevar a cabo los siguientes pasos.

1. *Creamos un grupo de recursos localizado en la región* en la que queramos realizar la medición. Para ello usamos la siguiente orden:
~~~
$ az group create --name <nombre-grupo-recurso> --location <region>
~~~

2. *Creamos una máquina virtual*, asociada a dicho grupo de recursos. Para ello, usamos la siguiente orden:
~~~
$ az vm create --resource-group <nombre-grupo-recurso> --admin-username andreamg \
--name <nombre-maquina> --image UbuntuLTS --size Basic_A0 --generate-ssh-keys \
--public-ip-address-allocation static
~~~

  Además, activamos el puerto 80, que como sabemos es necesario para poder arrancar el servicio:
  ~~~
  $ az vm open-port --resource-group resourceGroupAndrea --name vmAndrea --port 80
  ~~~

3. *Provisionamos la máquina* de la forma que venimos haciendo desde el hito 3, y arrancamos nuestra aplicación para poder realizar peticiones.

  ~~~
  $ ansible-playbook -i ansible_hosts -b playbook.yml
  ~~~



4. Realizamos la medición de la URL asociada a nuestro servicio.

  Para realizar una medición, bastaría con ejecutar la siguiente orden, donde *<numero_peticiones>* son el número de peticiones totales que se llevan a cabo, *<numero_peticiones_concurrentes>* el número de peticiones que se realizan de forma concurrente y <URL> la URL que vamos a testear, que en este caso coincidirá con http://IP/, donde la IP coincidirá con la de la máquina virtual que hemos creado por línea de órdenes. Podemos consultar más información acerca de cómo realizar una petición con Apache Bench [aquí](https://blog.diacode.com/testeando-el-rendimiento-de-tu-aplicacion-con-apache-bench).

  ~~~
  $ ab -n <numero_peticiones> -c <numero_peticiones_concurrentes> <URL>
  ~~~

  Ejecutamos la orden de *Apache Bench* previamente comentada, especificando un número de peticiones y la concurrencia de las mismas. Para una mayor robusted de los resultados, se ha ejecutado la misma orden en distintos instantes de tiempo, y posteriormente, se ha calculado el resultado medio de dichas peticiones.


Por tanto, repetiremos este procedimiento para todas las regiones que se han contemplado a la hora de tomar esta decisión: **Norte de Europa**, **Oeste de Europa**, **Centro de Francia**, **Sur de Francia** y **Oeste de UK**.

### Oeste de Europa


### Norte de Europa


### Centro de Francia

### Sur de Francia

### Oeste de UK
