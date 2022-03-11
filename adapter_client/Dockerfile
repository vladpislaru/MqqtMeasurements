FROM python:latest

RUN pip3 install paho-mqtt
RUN pip install influxdb
RUN apt-get update
ADD adapter.py /server/
WORKDIR /server

CMD ["python3" , "adapter.py"]