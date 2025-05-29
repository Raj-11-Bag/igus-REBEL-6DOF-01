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
GRIPPER_OPEN = "CRISTART 3000 CMD DO 31 1; DO 32 0 CRIEND"  # High on port 31, Low on port 32
GRIPPER_CLOSE = "CRISTART 3000 CMD DO 31 0; DO 32 1 CRIEND" # Low on port 31, High on port 32

pick_positions = {
    'x': "CRISTART 2000 CMD Move Joint 111.8 -1.3 113.7 0.0 67.7 111.8 0.0 0.0 0.0 100.0 CRIEND",
    'x1': "CRISTART 2000 CMD Move Joint 111.8 3.2 117.3 0.0 59.5 111.8 0.0 0.0 0.0 100.0 CRIEND",
    'y': "CRISTART 2000 CMD Move Joint 90.0 -6.1 118.2 0.0 67.9 108.2 0.0 0.0 0.0 100.0 CRIEND",
    'y1': "CRISTART 2000 CMD Move Joint 90.0 -1.4 121.9 0.0 59.5 108.2 0.0 0.0 0.0 100.0 CRIEND",
    'z': "CRISTART 2000 CMD Move Joint 68.1 -1.1 113.7 0.0 67.7 98.60 0.0 0.0 0.0 100.0 CRIEND",
    'z1': "CRISTART 2000 CMD Move Joint 68.1 3.3 117.2 0.0 59.5 98.60 0.0 0.0 0.0 100.0 CRIEND"
}

place_positions = {
    'a': "CRISTART 2000 CMD Move Joint -111.8 -1.1 113.4 0.0 67.7 86.7 0.0 0.0 0.0 100.0 CRIEND",    
    'a1': "CRISTART 2000 CMD Move Joint -111.8 2.2 116.6 0.0 61.3 87.1 0.0 0.0 0.0 100.0 CRIEND",
    'b': "CRISTART 2000 CMD Move Joint -89.8 -6.1 118.1 -0.01 68.0 16.2 0.0 0.0 0.0 100.0 CRIEND",
    'b1': "CRISTART 2000 CMD Move Joint -90.0 -2.5 121.3 0.0 61.3 101.3 0.0 0.0 0.0 100.0 CRIEND",
    'c': "CRISTART 2000 CMD Move Joint -68.2 -0.9 113.2 0.0 68.3 98.48 0.0 0.0 0.0 100.0 CRIEND",
    'c1': "CRISTART 2000 CMD Move Joint -68.2 2.3 116.4 0.0 61.3 98.5 0.0 0.0 0.0 100.0 CRIEND"
}

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

def ask_for_pick():
    while True:
        pick_position = input("Where would you like to pick the object from? (x, y, z): ")
        if pick_position in ['x', 'y', 'z'] and pick_position not in picked_positions:
            return pick_position
        else:
            print("Invalid or already picked position. Please choose again.")

def ask_for_placement():
    while True:
        place_position = input("Where would you like to place the object? (a, b, c): ")
        if place_position in ['a', 'b', 'c'] and place_position not in filled_positions:
            return place_position
        else:
            print("Invalid or already filled position. Please choose again.")

def open_gripper():
    send_msg(sock, GRIPPER_OPEN)
    time.sleep(2) 

def close_gripper():
    send_msg(sock, GRIPPER_CLOSE)
    time.sleep(2)  

def execute_movement(pick, place):
    send_msg(sock, pick_positions[pick])
    time.sleep(9)
    send_msg(sock, pick_positions[pick + '1'])
    picked_positions.append(pick)
    time.sleep(4)
    open_gripper()

    send_msg(sock, place_positions[place])
    time.sleep(9)
    send_msg(sock, place_positions[place + '1'])
    filled_positions.append(place)
    time.sleep(4)
    close_gripper()
    print(f"Picked from position {pick} and placed at {place}")

picked_positions = []
filled_positions = []

def on_message(client, userdata, message):
    global mqtt_message_received, task_list
    if message.topic == "robotics/robot1/mqttcri":
        payload = message.payload.decode('utf-8')
        mqtt_message_received = True

mqtt_message_received = False
task_list = []

MQTT_Handler.client.on_message = on_message

thread_read_msg = threading.Thread(target=read_msg, args=(sock,))
thread_read_msg.start()
send_msg(sock, CRI_CONNECT)
send_msg(sock, CRI_ENABLE)
time.sleep(2)


while not mqtt_message_received:
    time.sleep(1)


if task_list:
    for pick, place in task_list:
        if pick in pick_positions and place in place_positions:
            execute_movement(pick, place)
else:
    while len(filled_positions) < 3:
        pick_position = ask_for_pick()
        place_position = ask_for_placement()
        execute_movement(pick_position, place_position)

thread_read_msg.join()
