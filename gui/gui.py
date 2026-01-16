import tkinter as tk
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883

BASE_TOPIC = "rinatyael/iot_smart_home"
TOPIC_TEMPERATURE = f"{BASE_TOPIC}/sensor/temperature"
TOPIC_ALARM = f"{BASE_TOPIC}/alarm/state"
TOPIC_ARMED = f"{BASE_TOPIC}/system/armed"


# ---------- GUI ----------
root = tk.Tk()
root.title("Smart Home Monitor")

temp_label = tk.Label(root, text="Temperature: --", font=("Arial", 14))
temp_label.pack(pady=5)

alarm_label = tk.Label(root, text="Alarm: --", font=("Arial", 14))
alarm_label.pack(pady=5)

armed_label = tk.Label(root, text="System: --", font=("Arial", 14))
armed_label.pack(pady=5)


# ---------- MQTT ----------
def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC_TEMPERATURE)
    client.subscribe(TOPIC_ALARM)
    client.subscribe(TOPIC_ARMED)


def on_message(client, userdata, msg):
    payload = msg.payload.decode().strip()

    if msg.topic == TOPIC_TEMPERATURE:
        temp_label.config(text=f"Temperature: {payload} °C")

    elif msg.topic == TOPIC_ALARM:
        alarm_label.config(text=f"Alarm: {payload}")

    elif msg.topic == TOPIC_ARMED:
        armed_label.config(text=f"System: {payload}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_start()


root.mainloop()
client.loop_stop()
client.disconnect()
