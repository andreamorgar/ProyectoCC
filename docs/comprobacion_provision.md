# Comprobación del provisionamiento en otra máquina

Hecho por @adrianmorente.

Para probar el provisionamiento en mi máquina virtual, basta con modificar el archivo [ansible_hosts](../provision/azure/ansible_hosts) que alude a las diferentes máquinas que Ansible debe tener en cuenta, añadiendo en el apartado `vars` mis credenciales correspondientes (IP pública de la máquina y nombre de usuario con permisos de súper usuario):

```
[vagrantboxes:vars]
ansible_ssh_host=13.80.98.209
ansible_ssh_user=azure
```

Como bien ha hecho Andrea, la autora de este proyecto, la fase de provisionamiento de la máquina virtual se divide en dos partes. La primera consiste en la instalación de los paquetes más esenciales (como `git`, `python` y `pip`) a través del gestor de paquetes `apt`. Se puede ver este código en [este fichero](../provision/azure/playbook.yml).

Por otro lado, la segunda parte del provisionamiento clona el código de este repositorio, accede al directorio descargado, instala las dependencias de Python y habilita el puerto 80 para dar acceso web. Esta configuración está accesible en [este fichero](../provision/azure/specific_playbook.yml).

Como el primer script importa al segundo, basta con ejecutar el primero, que en mi máquina virtual de Azure genera la siguiente salida, notando que todos los pasos han sido bien realizados:

<p align="center"><img alt="Comando de creación de un grupo de recursos virtuales en Azure" width="500px" src="./images/comprobacion-ansible-playbook.png" /></p>

A continuación, veamos una comprobación de la puesta en ejecución manual del servicio. Aunque la aplicación se habilita en el puerto 5000, como hemos comentado antes, Ansible ordena una redirección del puerto 5000 al 80 para la máquina virtual, por lo que las solicitudes HTTP al puerto 80 son atendidas por dicho servicio:

<p align="center"><img alt="Comando de creación de un grupo de recursos virtuales en Azure" width="650px" src="./images/comprobacion-ejecucion.png" /></p>
