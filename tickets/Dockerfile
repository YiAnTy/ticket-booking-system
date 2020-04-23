FROM python:3.6

COPY . /service

#RUN apt-get update -y && \
#    apt-get install python3-pip -y

RUN pip3 install nameko==2.12.0
RUN pip3 install marshmallow==3.5.1
RUN pip3 install redis==3.4.1

EXPOSE 8000
WORKDIR /service

RUN chmod +x /service/run.sh

CMD /service/run.sh

