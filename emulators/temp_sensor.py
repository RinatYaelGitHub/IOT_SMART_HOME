import time
import random
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883

BASE_TOPIC = "rinatyael/iot_smart_home"
TOPIC_TEMPERATURE = f"{BASE_TOPIC}/sensor/temperature"

PUBLISH_EVERY_SECONDS = 5


def on_connect(client, userdata, flags, rc):
    print("TEMP_SENSOR connected. rc =", rc)


def main():
    client = mqtt.Client()
    client.on_connect = on_connect

    client.connect(BROKER, PORT, 60)
    client.loop_start()

    print("TEMP_SENSOR publishing to:", TOPIC_TEMPERATURE)

    try:
        while True:
            temp = round(random.uniform(18.0, 33.0), 1)
            client.publish(TOPIC_TEMPERATURE, str(temp))
            print("Published temperature:", temp)
            time.sleep(PUBLISH_EVERY_SECONDS)
    except KeyboardInterrupt:
        print("TEMP_SENSOR stopping...")

    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    main()
