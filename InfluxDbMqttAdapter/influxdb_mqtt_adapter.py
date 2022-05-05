import logging
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import datetime
from filehelper import FileHelper


class InfluxDbMqttAdapter:

    def __init__(self, config):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        logging.info("Starting InfluxDB - MQTT Adapter")
        self.config = config
        # Initialize the InfluxDB Client
        self.matches = self.config['matches']

        influxdb_host = self.config['influxdb']['host']
        influxdb_port = self.config['influxdb']['port']
        influxdb_user = self.config['influxdb']['user']
        influxdb_password = self.config['influxdb']['password']
        influxdb_db = self.config['influxdb']['database']
        logging.info('[InfluxDB] Connecting to InfluxDB ' + influxdb_host +
                     ':' + str(influxdb_port) + ' and associated database ' + influxdb_db)
        if influxdb_user and influxdb_password:
            self.influx_client = InfluxDBClient(
                host=influxdb_host, port=influxdb_port, username=influxdb_user, password=influxdb_password, database=influxdb_db)
        else:
            self.influx_client = InfluxDBClient(
                host=influxdb_host, port=influxdb_port, database=influxdb_db)

        # Initialize the MQTT Client
        mqtt_host = self.config['mqtt']['host']
        mqtt_port = self.config['mqtt']['port']
        mqtt_user = self.config['mqtt']['user']
        mqtt_password = self.config['mqtt']['password']

        logging.info('[MQTT] Connecting to MQTT Broker ' +
                     mqtt_host + ':' + str(mqtt_port))
        self.mqtt_client = mqtt.Client()
        if mqtt_user and mqtt_password:
            self.mqtt_client.username_pw_set(mqtt_user, mqtt_password)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(mqtt_host, mqtt_port, 60)
        self.mqtt_client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        for match in self.matches:
            logging.info('[MQTT] Subscribing to topic ' + match['from'])
            client.subscribe(match['from'])

    def persist(self, msg):
        handled = True
        payload = msg.payload.decode('utf-8')
        # TODO Some fancy parsing handling? Trying to parse and handle as accurate as possible
        payload_value = float(payload)

        for match in self.matches:
            # Try to match the topic
            if match['from'] == msg.topic:
                # Get the object to persist
                content = match['to']
                # Set the time if wanted
                if match['set_time']:
                    # TODO Check that this works
                    current_time = datetime.datetime.utcnow().isoformat()
                    content['time'] = current_time
                content['fields']['value'] = payload_value
                self.influx_client.write_points([content])
                handled = True
                break

        if not handled:
            logging.error('Could not handle message of topic ' +
                          msg.topic + ' with payload ' + str(msg.payload))

    def on_message(self, client, userdata, msg):
        self.persist(msg)


if __name__ == '__main__':
    config = FileHelper.load_config('config.json')
    adapter = InfluxDbMqttAdapter(config)
