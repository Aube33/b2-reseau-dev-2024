import socket
from sys import argv, exit
import re, os, socket
from psutil import net_if_addrs
from datetime import datetime


#===== VERIFS =====
def isURL(url:str)->bool:
    """
    Check if string is URL
    """
    return re.search("^[a-z]+(\\.[a-z]+)+$", url)

def isIPv4(address:str)->bool:
    """
    Check if IP is IPv4
    """
    try: 
        socket.inet_aton(address)
        return True
    except:
        return False

def isWifiInterface(interface:str)->bool:
    """
    Check if interface is WiFi (Linux ONLY!!)
    """
    return os.path.exists(f"/sys/class/net/{interface}/wireless")


#===== FUNCTIONS =====
def lookup(target:str)->str:
    """
        - python network.py lookup <URL> : To lookup over URL
    """
    if not isURL(target):
        raise ValueError("Bad argument !")
    return socket.gethostbyname(target)


def ping(target:str)->str:
    """
        - python network.py ping <IPv4> : To ping an IPv4
    """

    if not isIPv4(target):
        raise ValueError("Bad argument !")

    response = os.system(f"ping {target} -c 1 > /dev/null")
    return "UP !" if response == 0 else "DOWN !"


def maskToCIDR(mask:str)->int:
    """
    Get CIDR Mask from Netmask (255.255.255.0 -> 24)
    """
    maskSplit = [bin(int(x)) for x in mask.split(".")]
    maskCounter = "".join(maskSplit).replace("0b", "")
    return maskCounter.count("1")

def ip()->str:
    """
        - python network.py ip : To display current WiFi IP, Netmask and possible IP on the network
    """
    interfaces_data = net_if_addrs()
    ip = mask = ""

    for name, addrs in interfaces_data.items():
        if(isWifiInterface(name)):
            ip = addrs[0].address
            mask = addrs[0].netmask
            break
    cidr_mask = maskToCIDR(mask)
    return f"{ip}/{cidr_mask}\n{2**(32-cidr_mask)}"

def getLogMessage(cmd:str, arg:str, isError=False):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    if isError:
        return f"{dt_string} [ERROR] Command {cmd} called with bad arguments : {arg}.\n"
    
    if arg == None:
        return f"{dt_string} [INFO] Command {cmd} called successfully.\n"
    else:
        return f"{dt_string} [INFO] Command {cmd} called successfully [with argument {arg}].\n"


AVAILABLE_COMMAND = {
    "lookup": lookup,
    "ping": ping,
    "ip": ip
}
LOG_DIR = "/tmp/network_tp3"
LOG_FILE = "network.txt"

result = ""
log_file_path = os.path.join(LOG_DIR,LOG_FILE)
os.makedirs(LOG_DIR, exist_ok=True)

logFile = open(log_file_path, "a")

if len(argv)>=2:
    CMD = argv[1]
    ARG = argv[2] if len(argv)>=3 else None

    if(CMD) not in list(AVAILABLE_COMMAND.keys()):
        result = (f"'{CMD}' is not an available command. Déso.")
    else:
        try :
            if CMD == "ip":
                result = AVAILABLE_COMMAND[CMD]()
            else:
                result = AVAILABLE_COMMAND[CMD](ARG)
            logFile.write(getLogMessage(CMD, ARG))
        except Exception as error:
            result = error
            logFile.write(getLogMessage(CMD, ARG, True))
    
logFile.close()
print(result)
