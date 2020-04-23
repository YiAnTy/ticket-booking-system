# ticket-booking-system
This system consist of 3 Microservice: UserService, PaymentService, OrderService

Before coding, please read this guidance:

1.prepare your docker, use this documents:
https://www.runoob.com/docker/windows-docker-install.html

2.install and run the register center:

```shell
docker pull rabbitmq:management
docker run -d --hostname my-rabbit --name rabbit -p 15672:15672 -p 5672:5672 rabbitmq:management
```

3.prepare your nameko, use

```shell
pip install nameko
```

4.prepare postman: https://www.postman.com/downloads/

5.prepare redis:

```shell
pip install redis
```

and use this document to run redis service:https://www.cnblogs.com/xiaodai0/p/9761192.html

and use this document to run redis service:https://www.cnblogs.com/xiaodai0/p/9761192.html

6.ok, begin your coding:)

# Deployment into Docker

**1.Download docker desktop or use terminal to get docker**

**2. Pull rabbitmq and run it through the container via docker**

RabbitMQ docker install command

```shell
docker search rabbitmq
docker pull rabbitmq:3.7-rc-management
```



Run RabbitMQ in the container at port 5672

```shell
docker run -d --hostname my-rabbit --name some-rabbit -p 15672:15672 -p
```

**3. Make Dockerfile**

userService dockerfile example

```dockerfile
 FROM python:3.6
 COPY . /service
 RUN apt-get update -y && \ apt-get install python3-pip -y

 RUN pip3 install nameko==2.12.0
 RUN pip3 install pymysql==0.9.3
 RUN pip3 install marshmallow==3.5.1
 RUN pip3 install redis==3.4.1
 RUN pip3 install sqlalchemy==1.3.4

 EXPOSE 8000
 WORKDIR /service

 RUN chmod +x /service/run.sh

 CMD /service/run.sh
```
**4.Go to the microservices subdirectory under the project directory and use dockerfile to generate docker image**

Enter the microservice root directory

```shell
cd /ticket-booing-system/users
```



build docker image

```shell
docker build -t nameko/nameko-userservice:1.0.0 .
```

**5. Start mysql and redis, and start the microservice through the generated image**

run docker container service

```shell
docker run --name=user-service --network=host nameko/nameko-userservice:1.0.0
```

![](/Users/fring/Desktop/docker container.png)
