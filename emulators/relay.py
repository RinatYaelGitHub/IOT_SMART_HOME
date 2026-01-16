import time
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883

BASE_TOPIC = "rinatyael/iot_smart_home"
TOPIC_ALARM = f"{BASE_TOPIC}/alarm/state"


def on_connect(client, userdata, flags, rc):
    print(f"RELAY connected. rc = {rc}")
    client.subscribe(TOPIC_ALARM)
    print(f"Subscribed to: {TOPIC_ALARM}")


def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8").strip().upper()
    if payload == "ON":
        print("🚨 ALARM ON !!!")
    else:
        print("✅ ALARM OFF")


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping relay...")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
