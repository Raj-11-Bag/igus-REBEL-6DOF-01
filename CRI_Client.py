import socket
import time
import threading
CRI_CONNECT = "CRISTART 1000 CMD Connect CRIEND"
CRI_DISCONNECT = "CRISTART 1001 CMD Disconnect CRIEND"
CRI_ENABLE = "CRISTART 1002 CMD Enable CRIEND"
CRI_DISABLE = "CRISTART 1003 CMD Disable CRIEND"
CRI_PROGRAM_LOAD = " CRISTART 1004 CMD LoadProgram [ProgName] CRIEND"
CRI_PROGRAM_START = " CRISTART 1005 CMD StartProgram CRIEND"
#CRI_MOTION = "CRISTART 2000 CMD Move Cart 200.0 0.0 300.0 0.0 180.0 0.0 0.0 0.0 0.0 20.0 CRIEND"

sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

host = ('10.0.5.117',3920)   #ip adress of robot and pot number for cri

print(f"try to connect to host: {host[0]} on port: {host[1]}") 

sock.connect(host)  

print("Connected")

def read_msg(sock):
    with open("igus.log","w") as output:
        while True:
            response = sock.recv(1024).decode('utf-8')
            if "CMDACK" in response:
                print(response)

def send_msg(sock,msg):
    sock.sendall(bytearray(msg.encode('utf-8')))
    time.sleep(0.1)


thread_read_msd = threading.Thread(target=read_msg, args=(sock,))
thread_read_msd.start()

send_msg(sock, CRI_CONNECT)
send_msg(sock,CRI_ENABLE )
send_msg(sock, CRI_PROGRAM_LOAD.replace("[ProgName]", "ReBeL_MoveToZero.xml")) # try to bring it on 90 degrees
time.sleep(2)
#send_msg(sock, CRI_PROGRAM_START)
#send_msg(sock, "CRISTART 2000 CMD Move Joint 0.0 0.0 90.0 0.0 90.0 0.0 0.0 0.0 0.0 20.0 CRIEND") 
#send_msg(sock, "CRISTART 2000 CMD Move Joint 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 20.0 CRIEND") 

thread_read_msd.join()








"""        if payload == "START":
            mqtt_message_received = True
        else:
            tasks = payload.split(';')
            for task in tasks:
                if ',' in task:
                    pick, place = task.split(',')
                    task_list.append((pick, place))
            mqtt_message_received = False"""