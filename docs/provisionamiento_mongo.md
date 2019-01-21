#Provisionamiento de una máquina virtual para MongoDB

Para aprovisionar la máquina virtual con MongoDB se ha llevado a cabo la realización de un *playbook* al que hemos denominado [playbook-mongodb.yml](https://github.com/andreamorgar/ProyectoCC/blob/master/orquestacion/playbook-mongodb.yml).

Inicialmente se realizaba el provisionamiento con un [rol de ansible para MongoDB](https://github.com/UnderGreen/ansible-role-mongodb). Sin embargo, a pesar del buen funcionamiento que se obtenía con dicho rol, se decidió descartar esta forma de provisionar por diversas razones:

1. El rol en cuestión provisionaba más cosas de las necesarias para el funcionamiento de la aplicación.

2. Este rol realiza una configuración extra sobre el/los servicio/s a utilizar, que impedía la correcta ejecución de nuestro proyecto, y que requería deshacer muchas de las acciones que llevaba a cabo de por sí en la provisión con dicho playbook.



Además, consultando la [información existente acerca de las buenas prácticas en Ansible](https://www.ncora.com/blog/como-se-usan-los-roles-y-playbooks-en-ansible/),  en muchos casos recomiendan usar configurar sin roles de este tipo si el playbook es para un único despliegue o la configuración que buscamos realizar es demasiado simple (y en casos complejos  utilizar roles, donde podremos adaptar las configuraciones ya predefinidas).

Por ello, finalmente me decanté por instalarlo manualmente desde ansible, con el gestor de paquetes  **apt**, y así realizar la simple y única configuración que necesito para mi proyecto, sin necesidad de realizar y deshacer configuraciones que realmente no son necesarias.

### Fichero *playbook-mongodb.yml*
El playbook resultante ([playbook-mongodb.yml](https://github.com/andreamorgar/ProyectoCC/blob/master/orquestacion/playbook-mongodb.yml)) se puede ver a continuación:
~~~
---
- name: Deploy MongoDB and configure the database
  hosts: all
  become: yes

  tasks:
    - name: Install mongodb package
      apt: pkg=mongodb state=latest

    - name: Allow remote connections
      lineinfile:
        dest: /etc/mongodb.conf
        regexp: "^\\s*bind_ip.*"
        line: "bind_ip = [127.0.0.1 10.0.0.4]"
        state: present

    - name: Restart mongodb service
      service: name=mongodb state=restarted

~~~

#### Aspectos a destacar del contenido del playbook
- En primer lugar, usamos apt para descargar la última versión que tenga disponible de *MongoDB*. Para ello, he partido de los ejemplos vistos [aquí](https://cloudmesh.github.io/introduction_to_cloud_computing/class/lesson/ansible_playbook.html).

- Por defecto, MongoDB tiene configurado que la única dirección IP desde la cuál escucha es **localhost**. Esta configuración es necesario modificarla, ya que queremos que escuche también desde la otra máquina en nuestra red interna. Para ello, necesitamos modificar el parámetro `bind_ip` del fichero de configuración de Mongo, que se encuentra en `/etc/mongodb.conf`.

  Sin embargo, no basta con modificar dicho valor a la IP que necesitemos, ya que también debe permitir escuchar desde localhost, ya que debe ejecutar el servicio. Para ello, hay dos opciones principales:

  - **Permitir escuchar desde localhost y desde la IP que queramos (en nuestro caso sería la IP interna de la otra máquina, que se corresponde con 10.0.0.4)**

  - Permitir escuchar desde todos los puertos (estableciendo `bind_ip = 0.0.0.0`) y configurar de alguna forma que solo se permita el acceso a la IP de la máquina que queremos(por ejemplo, mediante `iptables`)

  Me decanté por la primera opción, ya que es más sencilla y evita tener que modificar más configuraciones de la máquina. Para ello, indicaremos que pueda escuchar de esas dos direcciones estableciendo **bind_ip = [127.0.0.1 10.0.0.4]**, lo cuál podemos hacer desde Ansible, modificando la línea que contiene "bind_ip", como se puede ver en los [ficheros de Ansible](https://github.com/Ilyes512/ansible-role-mongodb/blob/master/tasks/main.yml) que utiliza uno de los roles que he encontrado en Github.

  ##### Problemas encontrados:
  Tal y como he podido ver intentando solucionar el error que obtenía al intentar escuchar desde dos IPs únicamente, la documentación de MongoDB no proporciona una solución válida única, sino que, además de fallar en una gran cantidad de casos, cada una de las posibles soluciones que encontré era distinta y no funcionaba bien. Mi solución realmente la encontré como mezcla de otras que formas que vi que habían sido la solución en otros casos, pero no la he encontrado documentada ni comentada en ninguna parte.

  **Dado que sin ver las soluciones de otros, nunca habría dado con la mía, he añadido mi solución en stackoverflow, como se puede ver en [esta duda de stackoverflow](https://stackoverflow.com/questions/30884021/mongodb-bind-ip-wont-work-unless-set-to-0-0-0-0/54281850#54281850).**


  - Por último, como se han realizado cambios en la configuración, hay que reiniciar el servicio, lo cuál también podemos llevarlo a cabo desde ansible como podemos ver [aquí](https://github.com/ansible/ansible/issues/5712).
