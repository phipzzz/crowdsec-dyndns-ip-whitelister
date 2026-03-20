import requests
import subprocess
import ipaddress
from datetime import datetime

crowdsecContainer = False
crowdsecContainerName = "crowdsec"
whitelistsFilePath = "/etc/crowdsec/parsers/s02-enrich/publicIpWhitelist.yaml"
curPubIpFilePathV4 = "./currentIPv4"
curPubIpFilePathV6 = "./currentIPv6"
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_external_ip(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text

# Uncomment if you don't want to use IPv4
extIPv4 = get_external_ip('https://api.ipify.org')

# Uncomment if you don't want to use IPv6/cidr
extIPv6 = get_external_ip('https://api6.ipify.org')
# Edit cidr notation to whitelist other network ranges
extIPv6Cidr = str(ipaddress.IPv6Network((extIPv6 + '/64'), False))

def read_from_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            return content
    except Exception as e:
        print(timestamp + ": Error while reading the file (" + filename + "):", str(e))
        return None

def write_to_file(filename, content):
    try:
        with open(filename, 'w') as file:
            file.write(content)
        print(timestamp + ": File " + filename + " has been written successfully.")
    except Exception as e:
        print(timestamp + ": Error while writing the file (" + filename + "):", str(e))

def reloadCrowdsec():
    if crowdsecContainer:
        subprocess.run(["docker", "restart", crowdsecContainerName], capture_output=True, text=True)
        print(timestamp + ": crowdsec container restarted successfully.")
    else:
        subprocess.run(["systemctl", "reload", "crowdsec.service"], capture_output=True, text=True)
        print(timestamp + ": crowdsec.service reloaded successfully.")

# Uncomment unnecessary lines if you don't use them
whitelistsFileContent = \
"name: fliprocks/publicIpWhitelist" + "\n" + \
"description: \"Whitelist events from public IP address\"" + "\n" + \
"whitelist:" + "\n" + \
"  reason: \"My public IP\"" + "\n" + \
"  ip:" + "\n" + \
"    - \"" + extIPv4 + "\""  + "\n" \
"  cidr:" + "\n" + \
"    - \"" + extIPv6Cidr + "\""  + "\n" \

changed = False

if read_from_file(curPubIpFilePathV4) != extIPv4:
    write_to_file(curPubIpFilePathV4, extIPv4)
    changed = True

if read_from_file(curPubIpFilePathV6) != extIPv6:
    write_to_file(curPubIpFilePathV6, extIPv6)
    changed = True

if changed:
    print(timestamp + ": Public IP has changed. Writing new IP to whitelist.")
    write_to_file(whitelistsFilePath, whitelistsFileContent)
    reloadCrowdsec()
else:
    print(timestamp + ": IP didn't change")
