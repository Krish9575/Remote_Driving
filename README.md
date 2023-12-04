# Remote-Controlled System Framework

These scripts form a basic framework for a remote-controlled system where the remote user can view video streams from multiple cameras and control the machine using commands.

## Technologies Used

### Remote User.py:

- **Socket Programming:** The script utilizes Python's socket module to establish network connections between the remote user and the machine.

- **OpenCV:** The cv2 library is used for capturing and displaying video frames.

- **Threading:** Threading is employed to simultaneously handle receiving video streams and sending commands.

- **Struct and Pickle:** These modules are used for serializing and deserializing data to transmit video frames efficiently.

### Machine.py:

- **Socket Programming:** The script utilizes Python's socket module for network communication between the machine and the remote user.

- **OpenCV:** The cv2 library is used for capturing video frames.

- **Threading:** Threading is used to handle video streaming and command reception concurrently.

## Working

### Remote User.py:

#### Receiving Video:

1. The script connects to left and right camera servers using separate sockets.
2. Two threads are created: one for receiving video frames (`receive_video`) and another for sending commands (`send_command`).
3. The `receive_video` thread continuously receives video frames from the left and right cameras and displays them using OpenCV.

#### Sending Commands:

1. The `send_command` thread allows the user to input machine commands.
2. It sends the commands to the machine via a separate socket.

#### Connecting to Cameras:

- The script establishes connections to left and right camera servers using different ports.

### Machine.py:

#### Streaming Video:

1. The script creates separate threads (`ser_soc_left` and `ser_soc_right`) to stream video from the left and right cameras.
2. Video frames are captured using OpenCV, serialized using Pickle, and transmitted to the remote user.

#### Receiving Commands:

1. The script creates a separate thread (`ser_soc_rece`) to listen for commands from the remote user.
2. It listens on a separate port and executes machine movements based on the received commands.

## Additional Information

- **Dynamic IP Address:** The scripts use the machine's dynamic IP address to establish connections. For a production environment, a static IP address or a domain name may be preferred.

- **Keyboard Interrupt Handling:** Both scripts handle keyboard interrupts gracefully, ensuring proper closure of sockets and releasing resources.

- **Thread Safety:** Threading is used to allow the remote user to receive video and send commands simultaneously, enhancing the responsiveness of the application.

- **Command List:** The machine script recognizes various machine commands such as left, right, backward, forward, lift, put, and quit.

- **Local Testing:** The IP addresses (192.168.1.3) and ports are set for local testing. In a real-world scenario, they would be replaced with the actual IP address and ports.
