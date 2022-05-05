from enum import Enum
import logging
import paho.mqtt.client as mqtt
from filehelper import FileHelper
import time
# TODO Maybe InfluxDB if historical data is necessary?

CONFIG_FILENAME = 'config.json'

class FCM_Mode(Enum):
    # Initialize the average with the next n values
    INIT_AVG = 1
    # Monitor
    MONITOR = 2

class FilterConditionMonitor:

    def __init__(self, config):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s')
        self.config = config

        # The mode in which the FCM should start
        self.mode = self.config['monitor']['mode']
        self.init_index = 0
        self.avg_delta_pos = self.config['monitor']['condition']['avg_delta_pos']
        self.avg_delta_neg = self.config['monitor']['condition']['avg_delta_neg']

        logging.info('Starting FilterConditionMonitor in mode ' + self.mode)
        # Take the previously calculated average for monitoring
        if self.mode == FCM_Mode.MONITOR.name:
            self.avg = self.config['monitor']['condition']['avg']
            self.calculate_limits()
        elif self.mode == FCM_Mode.INIT_AVG.name:
            self.avg = 0
        # Initialize the MQTT Client
        mqtt_host = self.config['mqtt']['host']
        mqtt_port = self.config['mqtt']['port']
        logging.info('[MQTT] Connecting to MQTT Broker ' +
                     mqtt_host + ':' + str(mqtt_port))
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(mqtt_host, mqtt_port, 60)
        self.mqtt_client.loop_forever()
        # Call a new thread to loop for incoming MQTT messages
        # self.mqtt_client.loop_start()

    def calculate_limits(self):
        '''Calculates the upper and lower value boundaries (limits) based on the 
        average value and the positive and negative deltas defined in the configuration
        '''
        self.avg_limit_upper = self.avg + self.avg_delta_pos
        self.avg_limit_lower = self.avg - self.avg_delta_neg

    def on_connect(self, client, userdata, flags, rc):
        for topic in self.config['mqtt']['subs']:
            logging.info('[MQTT] Subscribing to topic ' + topic)
            client.subscribe(topic)

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        if self.mode == FCM_Mode.INIT_AVG.name:
            # Build the average over the next avg_n_samples samples
            avg_n_samples = self.config['monitor']['condition']['avg_n_samples']
            if self.init_index < avg_n_samples:
                logging.info('[CM] Adding value ' + payload + ' to average')
                self.avg += float(payload)
                self.init_index += 1
            if self.init_index == avg_n_samples:
                self.avg = self.avg / avg_n_samples
                logging.info(
                    '[CM] Initialized new average level with value: ' + str(self.avg))
                # Update config file with new avg value
                self.config['monitor']['condition']['avg'] = self.avg
                FileHelper.save_config(CONFIG_FILENAME, self.config)
                self.calculate_limits()
                self.mode = FCM_Mode.MONITOR.name
                self.init_index = 0

        elif self.mode == FCM_Mode.MONITOR.name:
            # TODO Switching condition modes here if necessary
            self.monitor(float(payload))
        else:
            logging.error('[CM] Unknown mode ' + self.mode)

    def monitor(self, val):
        '''Monitoring that checks the given value against the defined delta that is associated as normal value changes.
        Fires an alert if the value is above or below the defined delta.
        '''
        # Give an indication about how 'full' the filter is by giving a percentage to the max limits
        percentage = val/self.avg_limit_upper * 100
        if percentage > 100:
            percentage = 100
        elif percentage < 0:
            percentage = 0
        self.mqtt_client.publish('/conditionmonitor/filter_123/percentage', percentage)
        
        # TODO Do further handling of such an alter
        if val > self.avg_limit_upper:
            logging.info('[ALERT] Value ' + str(val) + ' is above the upper limit ' + str(self.avg_limit_upper) + '[ALERT]')
        elif val < self.avg_limit_lower:
            logging.info('[ALERT] Value ' + str(val) + ' is below the lower limit' + str(self.avg_limit_lower) + '[ALERT]')
        
if __name__ == '__main__':
    config = FileHelper.load_config(CONFIG_FILENAME)
    fcm = FilterConditionMonitor(config)