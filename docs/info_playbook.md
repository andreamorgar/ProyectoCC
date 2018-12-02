
#### Fichero playbook.yml
Para entender bien el funcionamiento de un playbook de ansible, y sobretodo, qué hace exactamente y de qué forma, podemos consultar el apartado correspondiente en la guía oficial [aquí](https://docs.ansible.com/ansible/2.7/user_guide/playbooks_intro.html). Además, se sugiere consultar este otro [enlace](https://github.com/ansible/ansible-examples), pues contiene una serie de ejemplos y buenas prácticas que se pueden llevar a cabo. De estos dos enlaces, es de donde nos basaremos para llevar a cabo este apartado.

<!-- - Lo primero: python3 [aquí](https://medium.com/@perwagnernielsen/ansible-tutorial-part-2-installing-packages-41d3ab28337d) -->
De momento, tenemos hasta este punto un único playbook genérico. Para su creación, me he inspirado en el tutorial al que se puede acceder desde [aquí](https://medium.com/@perwagnernielsen/ansible-tutorial-part-2-installing-packages-41d3ab28337d).

Hemos utilizado una máquina Debian con Python 3, que ha sido escogida debido a que de esta forma, no solo contamos con Python instalado en la máquina, sino que por defecto ya trae consigo Python 3, tal y como se puede consultar [aquí](https://linuxconfig.org/how-to-change-default-python-version-on-debian-9-stretch-linux).

En primer lugar, el archivo playbook.yml va a representar únicamente a aquellas cosas genéricas que queramos instalar en una máquina virtual. Por tanto, tendríamos que instalar dos cosas indispensables para nuestro servicio web de la práctica anterior, las cuáles obtendremos a través del gestor de paquetes **apt**:
- **Git**: nos hace falta para poder acceder a nuestro proyecto desde la máquina virtual que hemos creado mediante Vagrant.. Sin git, entre otras cosas, no podremos hacer clone de nuestro repositorio, por lo que es esencial en este caso.

- **python-pip**: para poder hacer uso de pip. Se ha comprobado experimentalmente, que para el funcionamiento correcto de pip3 desde ansible, se debe instalar pip, y posteriormente, indicar el ejecutable concreto de pip con el que queremos funcionar.

- **python3-pip**: para poder utilizar pip3 y descargar aquello que necesitemos para la versión 3 de Python. Es necesario porque voy a instalar los requerimientos para poder ejecutar mi proyecto en la máquina de esa forma. Como estamos trabajando con Python 3, queremos pip 3 concretamente.

- **python-setuptools**: necesario para poder ejecutar los requirements. Este paquete fue añadido posteriormente, ya que uno de los errores obtenidos al intentar provisionar la máquina indicaba la necesidad de disponer de este paquete.

Hasta aquí tendríamos todas las utilidades generales necesarias que deben existir en la máquina virtual de forma que podamos ejecutar nuestra aplicación.



#### Siguiendo las buenas prácticas....

A pesar de que hay múltiples fuentes que defienden que un playbook debe ser un proceso cerrado (como por ejemplo [aquí](https://serverfault.com/questions/750856/how-to-run-multiple-playbooks-in-order-with-ansible)), esta afirmación no es compartida por el estándar de buenas prácticas de Ansible.

Si consultamos la guía de buenas prácticas de Ansible, podemos encontrar una sección llamada *Creating Reusable Playbooks*, a la cuál podemos acceder desde [aquí](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse.html). En ella podemos ver, que es preferible reutilizar distintos playbooks, en lugar de empezar con uno de la forma que vimos arriba. Por ello, la parte específica de lo que queremos ejecutar, la vamos a especificar en un segundo playbook, que contendrá todos aquellos específicos para poder ejecutar y desplegar nuestro proyecto:

- **git clone**: para poder descargar nuestro repositorio en la máquina virtual.

- **Dependencias específicas de la aplicación**: en este caso, aquello que sea imprescindible para el correcto funcionamiento del servicio web.


Por tanto utilizaremos un nuevo fichero, al que hemos llamado *especific_playbook.yml*,
el cuál se encargará de incorporar aquellos aspectos esenciales.

Nos quedaría por resolver cómo llevar a cabo la inclusión del playbook con el contenido específico que queremos incorporar. Para ello, hay múltiples formas, como podemos observar en la documentación oficial disponible [aquí](https://docs.ansible.com/ansible/2.4/playbooks_reuse_includes.html). La principal duda estaría en... ¿qué utilizar? ¿es preferible utilizar include  para incorporar otros playbooks al playbook principal?¿O es mejor si utilizamos import? Al final, ninguna de las opciones principales de la documentación es la solución, sino que lo preferible, en este momento, es hacer uso de *import_playbook*, ya que será la única disponible para futuras versiones de ansible. Esta información la podemos obtener si provisionamos la máquina indicando -v en la opción verbose de *VagrantFile*.

![Preferible usar import_playbook](https://raw.githubusercontent.com/andreamorgar/ejerciciosCC/master/images/razonImport.png)


Por tanto, el contenido final de nuestro playbook principal quedaría de la siguiente manera.

~~~
---
- hosts: all
  become: yes
  gather_facts: False
  tasks:
    - name: Install base packages
      apt: name={{ item }} state=present
      with_items:
        - git
        - python-pip
        - python3-pip
        - python-setuptools
      tags:
        - packages
- import_playbook: specific_playbook.yml
~~~

#### Fichero specific_playbook.yml

Como se ha indicado anteriormente, en este playbook nos encargaremos del provisionamiento que es específico a la aplicación que queremos desplegar. Por ello, tendrá dos cosas esenciales:

- **Clonación del proyecto**: tenemos que clonar nuestro proyecto en la máquina virtual en cuestión. Esta acción podemos llevarla a cabo sin problemas, ya que como vimos anteriormente, se ha instalado *git*. Podemos especificar el nombre con el que queremos que se nos guarde el repositorio, y además debemos especificar **clone: yes** en la clonación. Los pasos seguidos se pueden ver en la documentación de Ansible [aquí](https://docs.ansible.com/ansible/2.5/modules/git_module.html)

- **Instalación de los paquetes definidos en requirements.txt**. Este paso lo llevaremos a cabo mediante **pip**. Para ello, especificamos que instale en su última versión, el contenido que tenga el fichero *requirements.txt*. Para poder llegar hasta el contenido de este fichero, podemos poner la ruta concreta. En este caso, el usuario que estamos utilizando es *vagrant*, por lo que éste es el que debe estar en la ruta hasta llegar al fichero de requirements. Por último, debemos indicar de que, de los distintos ejecutables de pip que están instalados en el sistema, coja *pip3*.

- **Redirección del puerto 5000 al 80**. Como nuestra aplicación se ejecuta en el puerto 5000, pero para la correción debe ejecutarse en el 80, se ha realizado una redirección de forma que el tráfico del puerto 5000 sea dirigido al puerto 80, y así poder ejecutar nuestra aplicación por dicho puerto. Como vemos, este es un claro caso de la utilidad de usar ficheros específicos, ya que no tendría sentido ejecutar esta orden en un fichero genérico (estamos hablando de un cambio muy concreto referente a la ejecución del proyecto).

Para ver el contenido del fichero *specific_playbook.yml* pincha [aquí](https://github.com/andreamorgar/ProyectoCC/blob/master/provision/vagrant/specific_playbook.yml)
