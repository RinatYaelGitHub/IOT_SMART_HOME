import paho.mqtt.client as mqtt
import time

BROKER = "test.mosquitto.org"
TOPIC = "rinat/iot/test"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print("Received:", msg.payload.decode())

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_start()

# לתת זמן להתחבר ולהירשם ל-topic
time.sleep(1)

print("Publishing message...")
client.publish(TOPIC, "Hello MQTT from Rinat")

# לתת זמן לקבל את ההודעה
time.sleep(4)

client.loop_stop()
client.disconnect()
print("Done")
