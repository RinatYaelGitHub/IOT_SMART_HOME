import sqlite3
from datetime import datetime
import paho.mqtt.client as mqtt

BROKER = "test.mosquitto.org"
PORT = 1883

BASE_TOPIC = "rinatyael/iot_smart_home"
TOPIC_TEMPERATURE = f"{BASE_TOPIC}/sensor/temperature"
TOPIC_ALARM_STATE = f"{BASE_TOPIC}/alarm/state"

TEMP_THRESHOLD = 28.0
DB_PATH = "iot.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS temperature_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            value REAL NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def save_temperature(value: float):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO temperature_readings (ts, value) VALUES (?, ?)",
        (datetime.utcnow().isoformat(), value),
    )
    conn.commit()
    conn.close()


def on_connect(client, userdata, flags, rc):
    print("DATA_MANAGER connected. rc =", rc)
    client.subscribe(TOPIC_TEMPERATURE)
    print("Subscribed to:", TOPIC_TEMPERATURE)


def on_message(client, userdata, msg):
    try:
        temp = float(msg.payload.decode().strip())
    except ValueError:
        print("Bad temperature payload:", msg.payload)
        return

    print("Received temperature:", temp)
    save_temperature(temp)

    alarm_on = temp >= TEMP_THRESHOLD
    client.publish(TOPIC_ALARM_STATE, "ON" if alarm_on else "OFF")
    print("Alarm state:", "ON" if alarm_on else "OFF")


def main():
    init_db()
    print("DB ready:", DB_PATH)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_forever()


if __name__ == "__main__":
    main()
