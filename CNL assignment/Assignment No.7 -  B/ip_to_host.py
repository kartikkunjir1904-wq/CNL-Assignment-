
import socket

ip = input("Enter IP Address: ")

try:
    hostname = socket.gethostbyaddr(ip)[0]
    print("Host Name:", hostname)
except socket.herror:
    print("Host name not found.")
except socket.error:
    print("Invalid IP Address.")
