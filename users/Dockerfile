FROM python:3.6

COPY . /service

#RUN apt-get update -y && \
#    apt-get install python3-pip -y

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple  nameko==2.12.0
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple  pymysql==0.9.3
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple  marshmallow==3.5.1
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple  sqlalchemy==1.3.4

EXPOSE 8000
WORKDIR /service

RUN chmod +x /service/run.sh

CMD /service/run.sh

