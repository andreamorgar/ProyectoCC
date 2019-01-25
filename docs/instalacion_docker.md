## Pasos para instalar Docker

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
<p align="center"><img alt="Docker Hello World" width="1000px" src="./images/hito6/docker_finger_print.png" /></p>

~~~

$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"


$ sudo apt-get update

$ sudo apt-get install docker-ce
~~~

~~~

$ sudo docker run hello-world

~~~

<p align="center"><img alt="Docker Hello World" width="1000px" src="./images/hito6/docker_hello_word.png" /></p>
