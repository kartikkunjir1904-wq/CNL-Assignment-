
import socket

hostname = input("Enter Host Name: ")

try:
    ip = socket.gethostbyname(hostname)
    print("IP Address:", ip)
except socket.gaierror:
    print("Invalid Host Name.")
