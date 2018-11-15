### PASOS SEGUIDOS PARA EL DESPLIEGUE

A continuación se encuentran enumerados los pasos que he seguido para realizar el despliegue.

### 1. Primero nos registramos en travis
### 3. Crear .travis.yml y completarlo con mis especificaciones. Para eso he usado:
### 2. Activar el repositorio de nuestro proyecto en travis, para poder pasar los tests.
 - https://docs.travis-ci.com/user/languages/python/
 - https://github.com/JJ/servicio-web-docker-platzi/blob/master/.travis.yml

### 4. Tenemos que ver como se despliega en HEROKU
  - https://docs.travis-ci.com/user/deployment/heroku/

### 5. Instalo los clientes. Primero Heroku
 - Cliente heroku https://devcenter.heroku.com/articles/heroku-cli
 - Cliente travis https://github.com/travis-ci/travis.rb#installation
   - Hace falta ruby http://www.ruby-lang.org/en/downloads/

### 6. Instalo ruby en el enviroment con apt install ruby y me aseguro que la version
sea mayor que 2.0 ($ ruby -v)
$ sudo apt-get install ruby

### 7. Instalo Cliente travis
$ gem install travis -v 1.8.9 --no-rdoc --no-ri
No funciona, y siguiendo las correcciones [aquí](https://github.com/travis-ci/travis.rb/issues/391) y [aquí](https://github.com/travis-ci/travis.rb#ubuntu),por ello instalo:
$ sudo apt-get install ruby2.3-dev (porque yo tengo ruby2.3)

Al repetir la siguiente orden ya si funciona.
$ gem install travis -v 1.8.9 --no-rdoc --no-ri


### 8. Intento encriptar travis encrypt $(heroku auth:token) --add deploy.api_key
De esta forma me dan errores, pero podemos hacerlo de forma automática desde heroku uniéndolo a github desde ahi, asi que voy a quitar esa parte del .travis.yml

### Creo el fichero requeriments.txt.
Esto me permite poder instalar mediante pip todo lo necesario. Para ello, evitando usar la orden "pip freeze", he utilizado el paquete [pipreqs](https://github.com/bndr/pipreqs)


### 9. Hacer procfile (hay que instalar guinicorn con pip)
Para ello sigo las indicaciones de [aquí](https://devcenter.heroku.com/articles/python-gunicorn)

### 10. Hacer runtime.txt y añadir a requeriments guinicorn ya que hace falta: (ya que yo tenía el requirements hecho de antes, pero igualmente he probado a volver a generarlo y sale)

### 11. Desplegar en heroku
https://devcenter.heroku.com/articles/getting-started-with-python#deploy-the-app
Es muy útil que te permita ver los [logs](https://devcenter.heroku.com/articles/getting-started-with-python#view-logs), porque te das cuenta de lo que realmente está pasando.


### 12. Desde heroku, nos vamos a deploy.
Aunque ya tenemos seleccionada la opción de ENABLE AUTOMATIC DEPLOYS, tenemos que seleccionar la opción de no desplegar hasta que se ejecuten de forma correcta los tests de travis. Estoy siguiendo las instrucciones de [aqui](https://medium.com/@felipeluizsoares/automatically-deploy-with-travis-ci-and-heroku-ddba1361647f)

### 13. Hacemos $ heroku login, que nos manda a la web a hacer login.
$ heroku git:remote -a <nombre proyecto>

y al hacer eso se nos muestra:
set git remote heroku to https://git.heroku.com/secure-reef-19619.git

- https://devcenter.heroku.com/articles/git aquí viene más o menos la misma
información.


### Otros errores
Por último faltaría un problema con la distribución en directorios de mis archivos, que impide que se ejecuten mis tests al no estar en la misma ruta que los ficheros a testear.
Este problema lo he solucionado como se indica [aquí](https://stackoverflow.com/questions/1732438/how-do-i-run-all-python-unit-tests-in-a-directory), con la orden:
$python -m unittest discover test/
