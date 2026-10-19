
import socket
import os

HOST = input("Enter server IP (127.0.0.1 for same PC): ").strip()
PORT = 5000
BUFFER_SIZE = 4096


def receive_line(sock):
    data = bytearray()

    while True:
        char = sock.recv(1)

        if not char:
            raise ConnectionError("Server disconnected.")

        if char == b"\n":
            return data.decode("utf-8")

        data.extend(char)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    print("Connected to server!")

    while True:
        print("\n--- TCP CLIENT MENU ---")
        print("1. Say Hello")
        print("2. Send File")
        print("3. Calculator")
        print("4. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            message = input("Enter greeting: ")
            client.sendall(f"HELLO|{message}\n".encode())
            print("Server:", receive_line(client))

        elif choice == "2":
            path = input("Enter full file path: ").strip().strip('"')

            if not os.path.isfile(path):
                print("File not found.")
                continue

            filename = os.path.basename(path)
            size = os.path.getsize(path)

            if size > 50 * 1024 * 1024:
                print("Please select a file under 50 MB.")
                continue

            client.sendall(f"FILE|{filename}|{size}\n".encode())

            with open(path, "rb") as file:
                while True:
                    chunk = file.read(BUFFER_SIZE)
                    if not chunk:
                        break
                    client.sendall(chunk)

            print("Server:", receive_line(client))

        elif choice == "3":
            a = input("Enter first number: ")
            op = input("Enter operation (+, -, *, /): ").strip()
            b = input("Enter second number: ")

            client.sendall(f"CALC|{op}|{a}|{b}\n".encode())
            print("Server:", receive_line(client))

        elif choice == "4":
            client.sendall(b"EXIT\n")
            print("Client disconnected.")
            break

        else:
            print("Invalid choice. Try again.")
