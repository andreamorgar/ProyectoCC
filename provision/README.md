# Provisionamiento de máquina virtuales
---

En este documento se detallan los distintos pasos seguidos hasta conseguir provisionar tanto una máquina virtual local como una en Azure, con todo lo necesario para poder ejecutar en ella nuestro proyecto. Para ello, se seguirán los siguientes pasos:

1. Uso de *Vagrant* y *Ansible* para provisionar una máquina virtual desde local.
2. Uso de *Ansible* para provisionar una máquina virtual en la plataforma *Azure*.

---
## *Vagrant* y *Ansible* para provisionar una máquina virtual desde local.
### Instalación de las herramientas necesarias

#### Instalación de Vagrant
En primer lugar, vamos a trabajar con máquinas virtuales locales. Para ello, necesitamos instalar una herramienta que nos permita gestionar máquinas virtuales, de forma que podamos arrancarlas, provisionarlas y destruirlas fácilmente.

Por ello, se ha hecho uso de [Vagrant](https://www.vagrantup.com/). Se ha utilizado esta herramienta por dos razones principales:
- Se explicó en el seminario de Ansible impartido en la asignatura, por lo que ya estaba familiarizada.
- Vagrant permite configurar máquinas virtuales de una manera sencilla, además de ser muy fácil de cambiar esa configuración para trabajar con máquinas virtuales en la nube.

El primer paso por tanto, es instalar la herramienta. Para ello, hemos seguido los pasos vistos [aquí](https://howtoprogram.xyz/2016/07/23/install-vagrant-ubuntu-16-04/). Para un correcto funcionamiento de la herramienta, es esencial tener en cuenta dos aspectos:
- Necesitamos una herramienta como VirtualBox, donde podamos gestionar las máquinas virtuales que se están creando y acceder a las mismas.

- Hay que tener cuidado con la versión de Vagrant que instalamos. Si instalamos la herramienta mediante el gestor de paquetes, tal y como se indica en el enlace de descarga anterior, la versión que se descarga por defecto es *Vagrant 1.8.1*. Suponiendo que queremos trabajar con *VirtualBox* (como es mi caso), es importante saber que dicha versión de Vagrant no trabaja con las últimas versiones de *VirtualBox*, por lo que debemos actualizar, como mínimo, a la versión 2.0.2. Para ello, se pueden seguir los pasos vistos [aquí](https://github.com/openebs/openebs/issues/32).


#### Instalación de Ansible
El primer paso es instalar ansible en la máquina con la que estemos trabajando. Para poder disponer de ansible podemos instalarla desde dos formas principales:
- Utilizar el gestor de paquetes *apt-get*, tal y como se puede ver indicado [aquí](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-ansible-on-ubuntu-16-04).

- Instalar Ansible mediante *pip*. En este caso, vamos a seguir esta segunda forma, ya que como se vio en el seminario de Ansible de la asignatura, el instalar Ansible mediante *pip* tiene sus ventajas. Esto se debe a que te instala, de forma automática, otros modulos necesarios, como por ejemplo para trabajar con YAML (lo necesitaremos más tarde). Podemos ver cómo realizar la instalación [aquí](https://docs.ansible.com/ansible/2.7/installation_guide/intro_installation.html#latest-releases-via-pip).



### Creación de una máquina virtual con Vagrant

#### 1. Crear un entorno Vagrant
Una vez que tenemos Vagrant correctamente instalado, nos situamos en un directorio sobre el que trabajar. En mi caso, todo este proceso lo he realizado desde mi repositorio de ejercicios, por lo que una vez situada en la carpeta correspondiente, ejecutamos lo siguiente.
~~~
$ vagrant init
~~~
Con esta orden, estamos inicializando el directorio actual, de forma que sea un entorno *Vagrant*. Una vez ejecutada dicha orden, se crea un archivo *VagrantFile* en caso de que no exista anteriormente.
Este fichero recién creado, tenemos que modificarlo para adaptarlo a aquello que queramos hacer.


#### 2. Crear una máquina virtual
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
#### Provisionamiento de la máquina virtual

Vamos a instalar en la máquina virtual todo aquello que necesitemos. Para ello, podemos consultar la guía oficial [aquí](https://docs.ansible.com/ansible/2.7/scenario_guides/guide_vagrant.html), concretamente el apartado *Vagrant Setup*. Aquí se muestra un ejemplo de cómo podemos modificar el fichero VagrantFile para provisionar una única máquina. Para ello, haremos uso de Ansible.

Para poder llevar a cabo el provisionamiento con Ansible, necesitaremos dos ficheros:
- Fichero [ansible.cfg](https://github.com/andreamorgar/ProyectoCC/blob/master/provision/vagrant/ansible.cfg), en el que indicademos dos aspectos principales. En primer lugar, ponemos a False la comprobación de claves del host, para evitar problemas como Man in the Middle, tal y como se explicón en el seminario de Ansible. En segundo lugar, le estamos especificando cuál es el fichero (ansible_hosts) con el que vamos a trabajar y definir las máquinas en cuestión.

- Fichero [ansible_hosts](https://github.com/andreamorgar/ProyectoCC/blob/master/provision/vagrant/ansible_hosts), donde hacemos dos cosas principales. Por una parte, establecemos el puerto (en nuestro caso el 2222) y establecemos la clave SSH con la que vamos a trabajar. En segundo lugar, establecemos la IP y el usuario que tendrá la máquina (en nuestro caso lo hemos llamado *vagrant*).


Por otra parte, en el fichero *VagrantFile*, debemos **indicar el provisionamiento para dicha máquina**. Para ello, le indicamos el fichero *playbook* que queremos ejecutar, el cuál contiene el provisionamiento que queremos que tenga la máquina virtual que hemos especificado anteriormente. Como vemos en el contenido del fichero *VagrantFile* (mostrado a continuación), ya estamos haciendo uso de Ansible para poder llevar a cabo dicha tarea.

#### Contenido final del fichero *VagrantFile*:
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
- La sección de provisionamiento hace referencia a un playbook de ansible al que en el fichero *VagrantFile* hemos llamado *playbook.yml*. Podemos ver el contenido y la funcionalidad de este fichero [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/docs/info_playbook.md).
- Vagrant ejecutará el fichero de provisionamiento  que hemos definido una vez que la máquina virtual arranca y tiene acceso a SSH (o bien cuando ejecutemos explícitamente el provisionamiento).
- El hecho de tener activada la opción verbose va a provocar que se nos muestre más información del comando del Ansible playbook que utilicemos. Todavía no sabemos qué nos mostrará, entonces la voy a dejar de momento, y más adelante ya veremos si se quita del fichero o no.


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


#### Comprobación del provisionamiento.
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
