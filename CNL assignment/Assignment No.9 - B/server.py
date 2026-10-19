
import socket
import os

HOST = "0.0.0.0"
PORT = 5000
BUFFER_SIZE = 4096


def receive_line(conn):
    data = bytearray()

    while True:
        char = conn.recv(1)

        if not char:
            raise ConnectionError("Client disconnected.")

        if char == b"\n":
            return data.decode("utf-8")

        data.extend(char)


def receive_file(conn, filename, size):
    os.makedirs("received_files", exist_ok=True)
    filename = os.path.basename(filename)
    path = os.path.join("received_files", filename)

    remaining = size

    with open(path, "wb") as file:
        while remaining > 0:
            chunk = conn.recv(min(BUFFER_SIZE, remaining))

            if not chunk:
                raise ConnectionError("File transfer interrupted.")

            file.write(chunk)
            remaining -= len(chunk)

    conn.sendall(b"File received successfully.\n")


def handle_client(conn, address):
    print("Connected:", address)

    with conn:
        while True:
            try:
                request = receive_line(conn)
                parts = request.split("|")

                if parts[0] == "HELLO":
                    print("Client says:", parts[1])
                    conn.sendall(b"Hello, client! Greetings from server.\n")

                elif parts[0] == "FILE":
                    filename = parts[1]
                    size = int(parts[2])

                    if size < 0 or size > 50 * 1024 * 1024:
                        conn.sendall(b"File size must be under 50 MB.\n")
                        continue

                    receive_file(conn, filename, size)
                    print("File saved:", filename)

                elif parts[0] == "CALC":
                    a = float(parts[2])
                    b = float(parts[3])
                    op = parts[1]

                    if op == "+":
                        result = a + b
                    elif op == "-":
                        result = a - b
                    elif op == "*":
                        result = a * b
                    elif op == "/":
                        if b == 0:
                            conn.sendall(b"Error: division by zero.\n")
                            continue
                        result = a / b
                    else:
                        conn.sendall(b"Invalid operation.\n")
                        continue

                    conn.sendall(f"Result: {result}\n".encode())

                elif parts[0] == "EXIT":
                    break

                else:
                    conn.sendall(b"Invalid request.\n")

            except (ValueError, IndexError):
                conn.sendall(b"Invalid input.\n")
            except (ConnectionError, OSError):
                break

    print("Disconnected:", address)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print(f"TCP Server running on port {PORT}...")
    print("Waiting for a client...")

    while True:
        conn, address = server.accept()
        handle_client(conn, address)
