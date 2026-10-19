import os
import socket
import struct

HOST = "0.0.0.0"
PORT = 5000
BUFFER_SIZE = 60000
HEADER = struct.Struct("!II")


def receive_file(sock, addr):
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        if data == b"EXIT":
            print("Sender disconnected.")
            return
        if data.startswith(b"START|"):
            filename = os.path.basename(data[6:].decode())
            sock.sendto(b"READY", addr)
            break

    temp_name = "received_" + filename
    expected_seq = 0
    received = 0

    with open(temp_name, "wb") as file:
        while True:
            data, addr = sock.recvfrom(BUFFER_SIZE)

            if data == b"END":
                sock.sendto(b"DONE", addr)
                break

            if len(data) < HEADER.size:
                continue

            seq, length = HEADER.unpack(data[: HEADER.size])
            payload = data[HEADER.size :]

            if len(payload) != length:
                continue

            if seq == expected_seq:
                file.write(payload)
                received += len(payload)
                expected_seq += 1

            sock.sendto(struct.pack("!I", expected_seq), addr)

    print(f"Received: {temp_name} ({received} bytes)")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        print(f"UDP receiver listening on port {PORT}")

        while True:
            receive_file(sock, None)


if __name__ == "__main__":
    main()
