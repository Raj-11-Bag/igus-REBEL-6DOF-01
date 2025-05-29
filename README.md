# Smartphone-Controlled Robotic Arm | MQTT + ROS2 | igus REBEL 6DOF Project

This repository contains the code and configurations for an automated pick-and-place system designed for the igus REBEL-6DOF robot. The system is built to handle complex object manipulation tasks, leveraging the MQTT protocol for real-time communication and control.

## 📽️ Demo Video

Watch the full video of the robotic arm in action (pick-and-place via smartphone MQTT control):

[![Watch the video](https://img.youtube.com/vi/3a9YwpJj9Qo/0.jpg)](https://youtu.be/3a9YwpJj9Qo)



## 🧠 Key Features
- Real hardware integration with igus REBEL 6DOF
- Real-time control via MQTT from smartphone interface
- Custom XML sequences and MQTT payload parsing
- Developed entirely in Python (VS Code) + igus software

## 🧱 Technologies Used
- Python (3.x)
- MQTT (paho-mqtt)
- igus Robot Control V14 (XML format)

## 📁 Project Structure
- `CRI_Client(1).py & CRI_Pick&Place.py`: Python script that receives commands and controls robot
- `xml.files/`: Contains .xml igus V14 programs
-  Demo of real pick-and-place process

## 🛠 Prerequisites
- igus Robot Control V14 installed and connected to REBEL robot
- MQTT broker (My MQTT) running
- Python 3.x with `paho-mqtt`
- Libraries threading, socket, random, time

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Raj-11-Bag/igus-REBEL-6DOF-01.git
```
### 2. **Install Necessary Dependencies **
   ```bash
   pip install -r paho-mqtt 
```
### 3. Configure MQTT Settings
Update the MQTT broker settings in `MQTT_Handler.py`.

### 4. Run the Main Control Script
```bash
python3.12.exe CRI_Client(1).py  #if you want  simple Pick&Place Operation
or
python3.12.exe CRI_Pick&Place.py  #if you want Customize Pick&Place Operation
```
### Architecture_diagram
```bash
Smartphone App
     ↓
MQTT Broker (My MQTT)
     ↓
CRI_Client(1).py (Python)
     ↓
igus REBEL via XML/Control API
     ↺
Feedback to CRI_Client(1).py
```

### Contributions
Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.

### Contact
For further questions or inquiries, please contact rajbag4321@gmail.com .

