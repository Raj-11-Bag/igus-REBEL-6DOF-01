# igus-REBEL-6DOF-01-Pick-and-Place-System

This repository contains the code and configurations for an automated pick-and-place system designed for the igus REBEL-6DOF robot. The system is built to handle complex object manipulation tasks, leveraging the MQTT protocol for real-time communication and control.

## Repository Contents

### 1. Main Control Script
The core Python script that orchestrates the robot's operations, including:
- Connecting to the robot.
- Handling MQTT messages.
- Executing pick-and-place tasks.
- Commands for connecting and disconnecting the robot, enabling/disabling it, loading programs, and controlling the gripper.

### 2. MQTT Handler Module
A custom Python module (`MQTT_Handler.py`) responsible for:
- Managing MQTT communications.
- Subscribing to topics, parsing messages, and publishing robot status updates.
- Enabling seamless integration with IoT platforms.

### 3. Robot Motion Programs
XML configuration files (`mqtt+cri.xml` and `assignment4final.xml`) that define:
- The robot's joint and linear movements.
- Gripper actions and wait times.
- Essential configurations for executing precise and coordinated pick-and-place actions.

### 4. Pick and Place Logic
Pre-defined joint positions for picking and placing objects in various locations. The script supports:
- Dynamic selection of pick and place positions based on user input or task list.
- Flexible and adaptable operations.

### 5. Multithreading for Asynchronous Operations
The script uses multithreading to handle:
- Simultaneous tasks such as reading messages from the robot.
- Processing MQTT commands and executing movements without blocking the main execution flow.

## Key Features
- **Real-Time Communication:** Utilizes MQTT protocol for real-time communication between the robot and external devices, allowing dynamic task assignments and status monitoring.
- **Flexible Motion Control:** Supports both joint and linear movements with precise control over velocity, acceleration, and smoothness.
- **Customizable Pick-and-Place Positions:** Easily configurable pick-and-place positions with the ability to add or modify target locations.
- **Gripper Control:** Implements commands for opening and closing the gripper, integrated into the motion sequence for seamless object handling.
- **Error Handling and Recovery:** Includes basic error handling to ensure robust operations in unpredictable environments.

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/igus-REBEL-6DOF-Pick-and-Place-System.git
```
### 2. **Install Necessary Dependencies (if any)**
   ```bash
   pip install -r requirements.txt
```
### 3. Configure MQTT Settings
Update the MQTT broker settings in `MQTT_Handler.py`.

### 4. Run the Main Control Script
```bash
python main_control_script.py
```

### Usage
- Modify the XML configuration files to adjust robot movement paths.
- Customize MQTT topics and broker settings as needed.
- Use the provided Python functions to integrate additional sensors or control logic.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

### Contributions
Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.

### Contact
For further questions or inquiries, please contact rajbag4321@gmail.com .

