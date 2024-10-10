from os import system
from sys import argv
import socket

IP_ARG = argv[1]
response = -1

def valid_ip(address):
    try: 
        socket.inet_aton(address)
        return True
    except:
        return False

if valid_ip(IP_ARG):
    response = system(f"ping {IP_ARG} -c 1 > /dev/null")

print("UP !") if response == 0 else print("DOWN !")
