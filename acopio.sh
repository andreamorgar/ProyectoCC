#!/bin/bash

# En primer lugar, creamos el grupo de recursos para la máquina virtual, usando
# para ello la localización elegida
az group create --name myResourceGroupAndrea --location francecentral

# Creamos la máquina virtual, indicando número de recursos, usuario, nombre de la máquina, imagen, ssh y claves estáticas para la IP
az vm create --resource-group myResourceGroupAndrea --admin-username andreamg --name mvAndrea --image UbuntuLTS --generate-ssh-keys --public-ip-address-allocation static

# Activamos el puerto para poder tener la aplicación lista para que funcione la app
az vm open-port --resource-group myResourceGroupAndrea --name mvAndrea --port 80


# Faltaría provisionar, pero hay que pasarle el nombre del host al playbook

# La IP podemos obtenerla con la siguiente orden, que, aunque es lenta, permite
# obtener la IP pública de la máquina, entre otros valores
mv_ip=$(az vm show -d --resource-group myResourceGroupAndrea --name mvAndrea | jq -r '.publicIps')

echo $mv_ip
ansible-playbook -i "$mv_ip," -b playbook.yml --user andreamg
