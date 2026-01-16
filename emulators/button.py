import time
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883

BASE_TOPIC = "rinatyael/iot_smart_home"
TOPIC_ARMED = f"{BASE_TOPIC}/system/armed"   # הכפתור שולח לכאן: ON/OFF


def on_connect(client, userdata, flags, rc):
    print("BUTTON connected. rc =", rc)


def main():
    client = mqtt.Client()
    client.on_connect = on_connect

    client.connect(BROKER, PORT, 60)
    client.loop_start()

    armed = False
    print("BUTTON emulator ready.")
    print("כל פעם Enter -> משנה מצב ON/OFF")
    print("כדי לצאת: Ctrl+C")
    print("Publishing to:", TOPIC_ARMED)

    try:
        while True:
            input()  # מחכה ל-Enter
            armed = not armed
            payload = "ON" if armed else "OFF"
            client.publish(TOPIC_ARMED, payload)
            print("Button state:", payload)
    except KeyboardInterrupt:
        print("Stopping button...")

    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    main()
