from socket import gethostbyname
from sys import argv, exit
import re, os
from psutil import net_if_addrs


#===== VERIFS =====
def isURL(url:str)->bool:
    return re.search("^[a-z]+(\\.[a-z]+)+$", url)

def isIPv4(address:str)->bool:
    try: 
        socket.inet_aton(address)
        return True
    except:
        return False

def isWifiInterface(interface:str)->bool:
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


if len(argv)<=1:
    print(f"""
    Usage:
        {lookup.__doc__}
        {ping.__doc__}
        {ip.__doc__}
    """)
elif len(argv)>=2:
    ARG_FUNC = argv[1]
    if(ARG_FUNC == "ip"):
        print(ip())

    elif(ARG_FUNC == "lookup"):
        if(len(argv)==2):
            print(f"Usage:\n{lookup.__doc__}")
        else:
            print(lookup(argv[2]))

    elif(ARG_FUNC == "ping"):
        if(len(argv)==2):
            print(f"Usage:\n{ping.__doc__}")
        else:
            print(ping(argv[2]))
    else:
        print(f"'{ARG_FUNC}' is not an available command. Déso.")

