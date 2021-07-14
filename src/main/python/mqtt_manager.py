from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import json


class MQTTManager:
    """Keeps the connections to MQTT, used for sending and receiving messages."""
    mqtt_connection = None

    def __init__(self, cert_path: str, key_path: str, root_path: str, port: int, client_id: str, server: str):
        """ constructor.
        """
        self.cert_path = cert_path
        self.key_path = key_path
        self.root_path = root_path
        self.port = port
        self.client_id = client_id
        self.server = server

    def __str__(self):
        """prints the object."""
        return "MQTT Manager"

    def connect(self):
        """connects to the default values given."""
        event_loop_group = io.EventLoopGroup(1)
        host_resolver = io.DefaultHostResolver(event_loop_group)
        client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
        self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
            # check https://aws.github.io/aws-iot-device-sdk-python-v2/awsiot/mqtt_connection_builder.html
            client_bootstrap=client_bootstrap,  # variable build above
            cert_filepath=self.cert_path,
            pri_key_filepath=self.key_path,
            ca_filepath=self.root_path,
            #port=self.port,
            client_id=self.client_id,
            endpoint=self.server,  # AWS IoT Core custom endpoint URL
            clean_session=False,
            keep_alive_secs=60
        )
        print("Connecting to {} with client ID '{}'...".format(
            self.server, self.client_id))
        # Make the connect() call
        connect_future = self.mqtt_connection.connect()
        # Future.result() waits until a result is available
        res = connect_future.result()
        print(res)
        print("Connected!")

    def disconnect(self):
        disconnect_future = self.mqtt_connection.disconnect()
        disconnect_future.result()

    def on_message(self, callback):
        """callback should take the following arguments and return nothing:
        topic (str): Topic receiving message.
        payload (bytes): Payload of message.
        dup (bool): DUP flag. If True, this might be re-delivery of an earlier attempt to send the message.
        qos (QoS): Quality of Service used to deliver the message.
        retain (bool): Retain flag. If True, the message was sent as a result of a new subscription being made by the client.
        **kwargs (dict): Forward-compatibility kwargs."""
        self.mqtt_connection.on_message(callback)

    def add_topic(self, topic, on_message_received=None):
        """adds a topic to the mqtt client."""
        print("Subscribing to topic '{}'...".format(topic))
        subscribe_future, packet_id = self.mqtt_connection.subscribe(
            topic=topic,
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=on_message_received)
        subscribe_result = subscribe_future.result()
        print("Subscribed with {}".format(str(subscribe_result['qos'])))

    def send_msg(self, topic, msg):
        """sends a message on the topic."""
        print("Sending MQTT message: " + json.dumps(msg))
        self.mqtt_connection.publish(topic=topic, payload=json.dumps(msg), qos=mqtt.QoS.AT_LEAST_ONCE)
        print("Published: '" + json.dumps(msg) + "' to the topic: " + topic)
