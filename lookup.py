from socket import gethostbyname
from sys import argv, exit
import re

if len(argv)<=1 or not re.search("^[a-z]+(\\.[a-z]+)+$", argv[1]):
    print("Argument non valide !")
    exit(1)

print(gethostbyname(argv[1]))