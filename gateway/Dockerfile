FROM python:3.6

COPY . /gateway

#RUN apt-get update -y && \
#    apt-get install python3-pip -y

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple  nameko==2.12.0
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple  flask==1.1.2
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple  werkzeug==1.0.1
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple  marshmallow==3.5.1

EXPOSE 8000
WORKDIR /gateway


CMD python /gateway/gateway/service.py

