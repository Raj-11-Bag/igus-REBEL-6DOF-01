import paho.mqtt.client as mqtt
import random
import string
import time 

# Creating random name (Client-ID)


random_name="".join(random.choices(string.ascii_letters + string.digits, k=8))

client = mqtt.Client(client_id=random_name, clean_session=True)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connection successful")
    elif rc ==1:
        print("connection refused - incorrect protocol version")
    elif rc ==2:
        print("connection refused - invalid client identifier")
    elif rc ==3:
        print("connection refused - server unavailable")
    elif rc ==4:
        print("connection refused - bad username and/or password")
    elif rc ==5:
        print("connection refused - not authorised")
    else:
        print(f"connection refused: {rc}")

def on_disconnect(client, userdata, rc):
    print(f"disconnected from broker with result code: {rc}")

client.on_connect = on_connect
client.on_disonnect = on_disconnect

if __name__ == "__main__":
    client.connect("mqtt-dashboard.com", 1883)
    client.loop_start()
    while True:
        client.publish("robotics/robot1/status","Hiiiiiiiiiiiiiiiiiiiiiii MY name is Raj")
        time.sleep(2)
 
