import requests
import subprocess
from datetime import datetime

crowdsecContainer = False
crowdsecContainerName = "crowdsec"
whitelistsFilePath = "/etc/crowdsec/parsers/s02-enrich/publicIpWhitelist.yaml"
curPubIpFilePath = "./currentIP"
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_external_ip():
    response = requests.get('https://api.ipify.org')
    if response.status_code == 200:
        return response.text

extIP = get_external_ip()

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

whitelistsFileContent = \
"name: phipzzz/publicIpWhitelist" + "\n" + \
"description: \"Whitelist events from public IPv4 address\"" + "\n" + \
"whitelist:" + "\n" + \
"  reason: \"My public IP\"" + "\n" + \
"  ip:" + "\n" + \
"    - \"" + extIP + "\""  + "\n" 

if read_from_file(curPubIpFilePath) != extIP:
    print(timestamp + ": Public IP has changed. Setting new IP to whitelist.")
    write_to_file(curPubIpFilePath, extIP)
    write_to_file(whitelistsFilePath, whitelistsFileContent)
    reloadCrowdsec()
else:
    print(timestamp + ": IP didn't change")
