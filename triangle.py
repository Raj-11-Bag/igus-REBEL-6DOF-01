import socket
import time
import threading
import MQTT_Handler

CRI_CONNECT = "CRISTART 1000 CMD Connect CRIEND"
CRI_DISCONNECT = "CRISTART 1001 CMD Disconnect CRIEND"
CRI_ENABLE = "CRISTART 1002 CMD Enable CRIEND"
CRI_DISABLE = "CRISTART 1003 CMD Disable CRIEND"
CRI_PROGRAM_LOAD = "CRISTART 1004 CMD LoadProgram [ProgName] CRIEND"
CRI_PROGRAM_START = "CRISTART 104 CMD StartProgram CRIEND"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = ('192.168.3.11', 3920)
print(f"Trying to connect to host: {host[0]} on port: {host[1]}")

sock.connect(host)
print("Connected!")


MQTT_Handler.client.connect("mqtt-dashboard.com", 1883)
MQTT_Handler.client.subscribe("robotics/robot1/#")
MQTT_Handler.client.loop_start()
print("MQTT client connected!")


def read_msg(sock):
    while True:
        response = sock.recv(1024).decode('utf-8')
        MQTT_Handler.client.publish("robotics/robot1/status", response)

def send_msg(sock, msg):
    print(msg)
    sock.sendall(bytearray(msg.encode('utf-8')))


def execute_movement(position_cmd, program_cmd):
    send_msg(sock, position_cmd)
    time.sleep(6)  
    send_msg(sock, CRI_PROGRAM_LOAD.replace("[ProgName]", program_cmd))
    time.sleep(2)  
    send_msg(sock, CRI_PROGRAM_START)
    print("Executed drill.")


def on_message(client, userdata, message):
    global mqtt_message_received, first_position_cmd
    if message.topic == "robotics/robot1/triangle":
        payload = message.payload.decode('utf-8')
        try:
            data = eval(payload)  
            if 'x' in data and 'y' in data and 'z' in data:
                x = float(data['x'])
                y = float(data['y'])
                z = float(data['z'])
                first_position_cmd = f"CRISTART 2001 CMD CartBase {x} {y} {z} 40.0 50.0 60.0 70.0 80.0 90.0 80.0 CRIEND" #CRISTART 2000 CMD Move Joint 90.0 0.0 90.0 0.0 90.0 0.0 0.0 0.0 0.0 20.0 CRIEND

                mqtt_message_received = True
            
        except Exception as e:
            print(f"Error processing MQTT message: {e} Please provide in this form X, Y, Z")

mqtt_message_received = False
first_position_cmd = True

MQTT_Handler.client.on_message = on_message

thread_read_msg = threading.Thread(target=read_msg, args=(sock,))
thread_read_msg.start()

send_msg(sock, CRI_CONNECT)
send_msg(sock, CRI_ENABLE)
time.sleep(2)

while not mqtt_message_received:
    time.sleep(1)

task_list = [
    (
        first_position_cmd,
        f"triangle.xml"  
    )
]

if task_list:
    for position_cmd, program_cmd in task_list:
        execute_movement(position_cmd, program_cmd)

thread_read_msg.join()
