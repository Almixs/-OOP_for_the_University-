import requests
import websockets
import asyncio
import time
import paho.mqtt.client as mqtt


# ---------------- REST ----------------
class RestClient:
    def get(self, endpoint):
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            data = response.json()
            print("GET: перші 2 записи:")
            print(data[:2])
        except requests.RequestException as e:
            print("Помилка GET-запиту:", e)

    def post(self, endpoint, data):
        try:
            response = requests.post(endpoint, json=data)
            response.raise_for_status()
            print("POST: створено пост:", response.json())
        except requests.RequestException as e:
            print("Помилка POST-запиту:", e)


# ---------------- WebSocket ----------------
class WebSocketClient:
    def __init__(self):
        self.websocket = None

    async def connect(self, url):
        try:
            self.websocket = await websockets.connect(url)
            print("WebSocket: підключено до сервера")
        except Exception as e:
            print("Помилка підключення WebSocket:", e)

    async def send_message(self, message):
        if self.websocket:
            await self.websocket.send(message)
            print("WebSocket: повідомлення надіслано")

    async def receive_message(self):
        try:
            message = await asyncio.wait_for(self.websocket.recv(), timeout=5)
            print("WebSocket: сервер прислав:", message)
        except asyncio.TimeoutError:
            print("WebSocket: таймаут отримання повідомлення")
        except Exception as e:
            print("WebSocket: помилка при отриманні повідомлення:", e)

    async def close_connection(self):
        if self.websocket:
            await self.websocket.close()
            print("WebSocket: з'єднання закрито")


# ---------------- MQTT ----------------
class MQTTClient:
    def __init__(self, broker_address, broker_port, username=None, password=None):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.username = username
        self.password = password
        self.client = mqtt.Client()

        if username and password:
            self.client.username_pw_set(username, password)

        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish

    def on_connect(self, client, userdata, flags, rc):
        print("MQTT: підключено до брокера з кодом:", rc)

    def on_publish(self, client, userdata, mid):
        print("MQTT: повідомлення успішно опубліковано")

    def connect(self):
        try:
            self.client.connect(self.broker_address, self.broker_port, 60)
            self.client.loop_start()
        except Exception as e:
            print("MQTT: помилка підключення:", e)

    def publish(self, topic, message):
        try:
            self.client.publish(topic, message, qos=0, retain=False)
        except Exception as e:
            print("MQTT: помилка публікації:", e)

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()
        print("MQTT: з'єднання розірвано")


# ---------------- Розділені сценарії ----------------
def run_rest():
    print("-------------- REST ------------")
    rest = RestClient()
    rest.get("https://jsonplaceholder.typicode.com/posts")
    data = {
        "title": "Здача лаб2",
        "body": "лаб2 костиль ходячий ))",
        "userId": 2
    }
    rest.post("https://jsonplaceholder.typicode.com/posts", data)


async def run_websocket():
    print("-------------- WEB SOCKET ------------")
    ws = WebSocketClient()
    await ws.connect("wss://echo.websocket.events")
    await ws.send_message("перевірка echo websocket")
    await ws.receive_message()
    await ws.receive_message()
    await ws.close_connection()


def run_mqtt():
    print("-------------- MQTT ------------")
    mqtt_client = MQTTClient(broker_address="test.mosquitto.org", broker_port=1883)
    mqtt_client.connect()
    time.sleep(1)
    mqtt_client.publish("unik", "lab2")
    time.sleep(1)
    mqtt_client.disconnect()


# ---------------- Головна функція ----------------
async def main():
    run_rest()
    await run_websocket()
    run_mqtt()


if __name__ == "__main__":
    asyncio.run(main())