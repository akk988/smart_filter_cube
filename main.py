# A MQTT Mockup Client that acts as a Sensor and sends demo values via MQTT
import time
import random
import paho.mqtt.client as mqtt

mqtt_broker_address = '172.21.5.116'
mqtt_broker_port = 1887
mqtt_client_id = 'MOCKUP_SensorValuePublisher'
send_delay_seconds = 2

filter_id = 'filter_123'
topic = '/filter/sensor/pressure1/' + filter_id


def on_connect(client, userdata, flags, rc):
    print('Successfully connected to MQTT Broker %s:%d' %
          (mqtt_broker_address, mqtt_broker_port))

def send_data(client):
    time.sleep(send_delay_seconds)
    while True:
        # Random value between 0 and 4 bar
        value = round(random.uniform(0.0, 4.0), 2)
        # msg = 'pressure,filter_id=' + str(filter_id) + ',sensor_type=pressure,sensor_unit=bar value=' + str(value) 
        # msg = '123'
        # msg = 'pressure value=' + str(value)

        print('Sending for topic %s message: %s' %(topic, str(value)))
        client.publish(topic=topic, payload=str(value))
        time.sleep(send_delay_seconds)

def main():
    print('Starting MQTT Client...')
    client = mqtt.Client(client_id=mqtt_client_id)
    client.on_connect = on_connect
    client.connect(mqtt_broker_address, mqtt_broker_port, 60)
    client.set

    client.loop_start()
    send_data(client)

if __name__ == '__main__':
    main()