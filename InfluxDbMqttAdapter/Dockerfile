FROM python:3.7.0-alpine3.8
ADD . /adapter
WORKDIR /adapter
RUN pip install -r requirements.txt
CMD ["python", "-u", "influxdb_mqtt_adapter.py"]