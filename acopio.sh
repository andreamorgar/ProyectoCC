#!/bin/bash

# En primer lugar, creamos el grupo de recursos para la máquina virtual
az group create --name myResourceGroupAndrea --location francecentral
# Creamos la máquina virtual
az vm create --resource-group myResourceGroupAndrea --admin-username andreamg --name mvAndrea --image UbuntuLTS --generate-ssh-keys --public-ip-address-allocation static

# Activamos el puerto para poder tener la aplicación lista para que funcione la app
# no estoy segura de que esto vaya aquí
az vm open-port --resource-group myResourceGroupAndrea --name mvAndrea --port 80


# Faltaría provisionar, pero hay que pasarle el nombre de la IP, de la máquina, y del usuario
# La IP podemos obtenerla consultando esta información
mv_ip=$(az vm show -d --resource-group myResourceGroupAndrea --name mvAndrea | jq -r '.publicIps')

echo $mv_ip
ansible-playbook -i "$mv_ip," -b playbook.yml --user andreamg
