# ticket-booking-system
This system consist of 4 Microservice: UserService, PaymentService, OrderService, TicketService

Before coding, please read this guidance:

1.prepare your docker, use this documents:
https://www.runoob.com/docker/windows-docker-install.html

2.install and run the register center:
docker pull rabbitmq:management
docker run -d --hostname my-rabbit --name rabbit -p 15672:15672 -p 5672:5672 rabbitmq:management

3.prepare your nameko, use
pip install nameko

4.prepare postman: https://www.postman.com/downloads/

5.prepare redis:
pip install redis
and use this document to run redis service:https://www.cnblogs.com/xiaodai0/p/9761192.html

6.ok, begin your coding:)
