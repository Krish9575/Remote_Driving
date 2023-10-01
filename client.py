
import socket,cv2, pickle,struct,threading
left_camera = True
right_camera = True
def receive_video(left_socket, right_socket):
    global left_camera, right_camera

    data_left = b''
    data_right = b''

    payload_size = struct.calcsize('Q')

    while True:
        # Receive frames from the left camera
        while len(data_left) < payload_size:
            packet = left_socket.recv(4 * 1024)  # 4-kilobyte buffer
            if not packet:
                break
            data_left += packet

        packed_msg_size = data_left[:payload_size]
        data_left = data_left[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data_left) < msg_size:
            data_left += left_socket.recv(4 * 1024)
        frame_data = data_left[:msg_size]
        data_left = data_left[msg_size:]
        frame_left = pickle.loads(frame_data)

        # Receive frames from the right camera
        while len(data_right) < payload_size:
            packet = right_socket.recv(4 * 1024)  # 4-kilobyte buffer
            if not packet:
                break
            data_right += packet

        packed_msg_size = data_right[:payload_size]
        data_right = data_right[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data_right) < msg_size:
            data_right += right_socket.recv(4 * 1024)
        frame_data = data_right[:msg_size]
        data_right = data_right[msg_size:]
        frame_right = pickle.loads(frame_data)

        # Display frames in separate windows
        if left_camera:
            cv2.imshow('Left Camera', frame_left)
        if right_camera:
            cv2.imshow('Right Camera', frame_right)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    # Close the sockets at the end
    left_socket.close()
    right_socket.close()

def send_command(client_socket):
    global left_camera, right_camera

    while True:
        try:
            command = input("Enter Machine command:").strip()
            client_socket.sendall(command.encode("utf-8"))
            if command == 'quit':
                break
            elif command == 'right camera':
                left_camera = False
                right_camera = True
            elif command == 'left camera':
                right_camera = False
                left_camera = True

        except KeyboardInterrupt:
            break

def run():
    global left_camera, right_camera

    # Connect to the left and right camera server
    left_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    right_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    host_ip = '192.168.1.3'
    left_port,right_port, send_port = 9999,9977,9988
    left_socket.connect((host_ip, left_port))
    right_socket.connect((host_ip, right_port))
    send_socket.connect((host_ip,send_port))
    # Create threads for receiving video and sending commands
    receive_video_thread = threading.Thread(target=receive_video, args=(left_socket, right_socket))
    send_command_thread = threading.Thread(target=send_command, args=(send_socket,))

    receive_video_thread.start()
    send_command_thread.start()

    receive_video_thread.join()
    send_command_thread.join()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()
