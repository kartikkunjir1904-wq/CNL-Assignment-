import os
import socket
import struct

SERVER_IP = "127.0.0.1"
PORT = 5000
CHUNK_SIZE = 30000
HEADER = struct.Struct("!II")
TIMEOUT = 1
MAX_RETRIES = 10


def send_reliably(sock, address, packet, expected):
    for _ in range(MAX_RETRIES):
        sock.sendto(packet, address)
        sock.settimeout(TIMEOUT)

        try:
            response, _ = sock.recvfrom(1024)
            if response == expected:
                return True
        except socket.timeout:
            continue

    return False


def send_file(sock, address, filepath):
    filename = os.path.basename(filepath)
    sock.sendto(("START|" + filename).encode(), address)
    sock.settimeout(TIMEOUT)

    for _ in range(MAX_RETRIES):
        try:
            response, _ = sock.recvfrom(1024)
            if response == b"READY":
                break
        except socket.timeout:
            sock.sendto(("START|" + filename).encode(), address)
    else:
        print("Receiver did not respond.")
        return

    seq = 0

    with open(filepath, "rb") as file:
        while True:
            chunk = file.read(CHUNK_SIZE)
            if not chunk:
                break

            packet = HEADER.pack(seq, len(chunk)) + chunk
            success = False

            for _ in range(MAX_RETRIES):
                sock.sendto(packet, address)

                try:
                    response, _ = sock.recvfrom(1024)
                    if len(response) == 4:
                        ack = struct.unpack("!I", response)[0]
                        if ack == seq + 1:
                            success = True
                            break
                except socket.timeout:
                    continue

            if not success:
                print("Transfer failed at packet", seq)
                return

            seq += 1

    for _ in range(MAX_RETRIES):
        sock.sendto(b"END", address)
        try:
            response, _ = sock.recvfrom(1024)
            if response == b"DONE":
                print(f"Successfully sent: {filename}")
                return
        except socket.timeout:
            continue

    print("Receiver did not confirm completion.")


def main():
    print("1. Script file")
    print("2. Text file")
    print("3. Audio file")
    print("4. Video file")

    choice = input("Choose file type: ").strip()
    filepath = input("Enter file path: ").strip()

    extensions = {
        "1": (".py", ".js", ".sh"),
        "2": (".txt", ".csv", ".md"),
        "3": (".mp3", ".wav", ".ogg"),
        "4": (".mp4", ".avi", ".mkv", ".mov"),
    }

    if choice not in extensions:
        print("Invalid choice.")
        return

    if not os.path.isfile(filepath):
        print("File not found.")
        return

    if not filepath.lower().endswith(extensions[choice]):
        print("File extension does not match the selected type.")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        send_file(sock, (SERVER_IP, PORT), filepath)


if __name__ == "__main__":
    main()
