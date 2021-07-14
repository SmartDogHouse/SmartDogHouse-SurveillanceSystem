#!/usr/bin/env python3

from secret import PATH_TO_CERT, PATH_TO_ROOT, PATH_TO_KEY, MQTT_PORT, MQTT_CLIENT_ID, MQTT_HOST, MQTT_RECEIVE_TOPIC, MQTT_NOTIFY_TOPIC
from mqtt_manager import MQTTManager


mqtt_manager = MQTTManager(cert_path=PATH_TO_CERT, key_path=PATH_TO_KEY,  root_path=PATH_TO_ROOT, port=MQTT_PORT, client_id=MQTT_CLIENT_ID,
                           server=MQTT_HOST)


try:
    mqtt_manager.connect()
except Exception as e:
    print('Cannot connect MQTT: ' + str(e))

#mqtt_manager.add_topic(MQTT_NOTIFY_TOPIC)

msg = {"Notify": "test"}
mqtt_manager.send_msg(topic=MQTT_NOTIFY_TOPIC, msg=msg)
