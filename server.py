
import socket
import cv2, pickle, struct, threading

ser_soc_left = None
ser_soc_right = None
ser_soc_rece=None
def stream_video(cam_id, server_socket):
    if server_socket is not None:
        server_socket.close()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    # print(host_ip)
    port = 9999 if cam_id == 0 else 9977  # Use different ports for left and right cameras
    print(f'HOST IP:', host_ip)
    socket_address = (host_ip, port)

    server_socket.bind(socket_address)
    server_socket.listen(5)
    print("Listening At:", socket_address)

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Got connection from {addr} for Camera {cam_id}")
        if client_socket:
            print(cam_id)
            vid = cv2.VideoCapture(cam_id)
            while vid.isOpened():
                img, frame = vid.read()
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    client_socket.close()
                    vid.release()
                    cv2.destroyAllWindows()
                    break

def received_command(client_socket):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    port = 9988
    client_socket.bind((host_ip, port))
    client_socket.listen(5)
    try:
        client, _ = client_socket.accept()
        print("<============== Machine Start Working ==================> ")
        while True:
            command = client.recv(1024).decode()
            if command == 'quit':
                raise KeyboardInterrupt()
            elif command == 'left':
                print('Machine Move left')
            elif command == 'right':
                print('Machine Move right')
            elif command == 'backward':
                print('Machine Move backward')
            elif command == 'forward':
                print('Machine Move forward')
            elif command == 'lift':
                print('Machine Move lift')
            elif command == 'put':
                print('Machine Move put')
            else:
                break
    except KeyboardInterrupt:
        client_socket.close()

def run():
    global ser_soc_left, ser_soc_right,ser_soc_rece

    ser_soc_left = threading.Thread(target=stream_video, args=(0, ser_soc_left))
    ser_soc_right  = threading.Thread(target=stream_video, args=(1, ser_soc_right))
    ser_soc_rece = threading.Thread(target=received_command,args=(ser_soc_rece,))
    ser_soc_left.start()
    ser_soc_right.start()
    ser_soc_rece.start()

    ser_soc_left.join()
    ser_soc_right .join()
    ser_soc_rece.join()

if __name__ == "__main__":
    run()






