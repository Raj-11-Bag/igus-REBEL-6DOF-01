import socket
import time
import threading
import MQTT_Handler

CRI_CONNECT = "CRISTART 1000 CMD Connect CRIEND"
CRI_DISCONNECT = "CRISTART 1001 CMD Disconnect CRIEND"
CRI_ENABLE = "CRISTART 1002 CMD Enable CRIEND" 
CRI_DISABLE = "CRISTART 1003 CMD Disable CRIEND"
CRI_PROGRAM_LOAD = "CRISTART 1004 CMD LoadProgram [ProgName] CRIEND"
CRI_PROGRAM_START = "CRISTART 1005 CMD StartProgram CRIEND"
    



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = ('192.168.3.11', 3920)

print(f"try to connect to host: {host[0]} on port: {host[1]}")

sock.connect(host)

print("connected!")

MQTT_Handler.client.connect("mqtt-dashboard.com", 1883)
MQTT_Handler.client.subscribe("robotics/robot1/#")
MQTT_Handler.client.loop_start()
print("mqtt client connected!")

def read_msg(sock):
    while True:
        response = sock.recv(1024).decode('utf-8')
        MQTT_Handler.client.publish("robotics/robot1/status", response)
       # if "CMDACK" in response:
          #  print(response)

def send_msg(sock, msg):
    print(msg)
    sock.sendall(bytearray(msg.encode('utf-8')))
    time.sleep(0.1)

def on_message_close(client, userdata, message):
    if message.topic == "robotics/robot1/drill":
        send_msg(sock, "CRISTART 2001 CMD Move CartBase 100.0 200.0 300.0 40.0 50.0 60.0 70.0 80.0 80.0 CRIEND")
        #send_msg(sock, CRI_PROGRAM_LOAD.replace("[ProgName]", "triangle.xml"))
        time.sleep(2)
        send_msg(sock, CRI_PROGRAM_START)
    if message.topic == "IGUS/robot1/app":
        data = message.payload.decode("utf-8").splite(",")
        print(data)
        send_msg(sock, )

MQTT_Handler.client.on_message = on_message_close

thread_read_msg = threading.Thread(target=read_msg, args=(sock,))
thread_read_msg.start()

send_msg(sock, CRI_CONNECT)
send_msg(sock, CRI_ENABLE)
time.sleep(2)
send_msg(sock, "CRISTART 2001 CMD Move CartBase 100.0 50.0 300.0 143.0 10.0 178.0 70.0 80.0 80.0 base CRIEND")
time.sleep(5)

#send_msg(sock, CRI_PROGRAM_START)
#send_msg(sock, "CRISTART 2000 CMD Move Joint 90.0 0.0 90.0 0.0 90.0 0.0 0.0 0.0 0.0 20.0 CRIEND")
#send_msg(sock, "CRISTART 2000 CMD Move Cart 200.0 0.0 300.0 0.0 180.0 0.0 0.0 0.0 0.0 20.0 CRIEND")
thread_read_msg.join()