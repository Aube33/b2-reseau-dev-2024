from socket import gethostbyname
from sys import argv, exit
import re, os
from psutil import net_if_addrs


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
        return "Argument non valide !"
    return gethostbyname(target)


def ping(target:str)->str:
    """
        - python network.py ping <IPv4> : To ping an IPv4
    """
    if isIPv4(target):
        return "Argument non valide !"

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

result = ""
AVAILABLE_COMMAND = {
    "lookup": lookup,
    "ping": ping,
    "ip": ip
}
if len(argv)>=2:
    if(argv[1]) not in list(AVAILABLE_COMMAND.keys()):
        result = (f"'{argv[1]}' is not an available command. Déso.")
    else:
        if(argv[1]=="ip"):
            result = AVAILABLE_COMMAND[argv[1]]()

        elif len(argv)<=2:
            result =AVAILABLE_COMMAND[argv[1]].__doc__
        else:
            result = AVAILABLE_COMMAND[argv[1]](argv[2])
print(result)
