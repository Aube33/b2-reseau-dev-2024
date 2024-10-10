from psutil import net_if_addrs
import os

interfaces_data = net_if_addrs()

def isWifiInterface(interface:str)->bool:
    return os.path.exists(f"/sys/class/net/{interface}/wireless")

def maskToCIDR(mask:str)->int:
    maskSplit = [bin(int(x)) for x in mask.split(".")]
    maskCounter = "".join(maskSplit).replace("0b", "")
    return maskCounter.count("1")

ip = mask = ""

for name, addrs in interfaces_data.items():
    if(isWifiInterface(name)):
        ip = addrs[0].address
        mask = addrs[0].netmask
        break

cidr_mask = maskToCIDR(mask)
print(f"{ip}/{cidr_mask}")
print(2**(32-cidr_mask))
