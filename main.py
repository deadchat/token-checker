import os
import json
import ctypes
import pyfiglet
import requests

from colorama import Fore
from fake_useragent import UserAgent
from pystyle import Colorate, Colors, Center, Box

agent = UserAgent()

def cls():
    os.system("cls" if os.name == "nt" else "clear")

def getHeaders(token):
    return {"Authorization": token, "Content-Type": "application/json", "User-Agent": agent.chrome}

class logger:
    def valid(token):
        print(f'[ {Fore.LIGHTGREEN_EX}VALID{Fore.RESET} ] {token[:-5]}{"*"*5}')
    def locked(token):
        print(f"[ {Fore.YELLOW}LOCKED{Fore.RESET} ] {token}")
    def invalid(token):
        print(f"[ {Fore.LIGHTRED_EX}INVALID{Fore.RESET} ] {token}")

class _modules:
    def checker():
        cls(); valid = []; locked = []; invalid = []
        with open("tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        with requests.Session() as session:
            for token in tokens:
                if len(token) > 75:
                    token = token.split(":")[2]
                req = session.get("https://discord.com/api/v9/users/@me", headers=getHeaders(token))
                if req.status_code == 200:
                    valid.append(token)
                    ctypes.windll.kernel32.SetConsoleTitleW(f"TokenZ - Valid: {len(valid)}, Locked: {len(locked)}, Invalid: {len(invalid)}")
                    logger.valid(token)
                elif req.status_code == 401:
                    invalid.append(token)
                    ctypes.windll.kernel32.SetConsoleTitleW(f"TokenZ - Valid: {len(valid)}, Locked: {len(locked)}, Invalid: {len(invalid)}")
                    logger.invalid(token)
                elif req.status_code == 403:
                    locked.append(token)
                    logger.locked(token)
        validTokens = ""; lockedTokens = ""; invalidTokens = ""

        for token in valid:
            validTokens += token + "\n"
        for token in locked:
            lockedTokens += token + "\n"
        for token in invalid:
            invalidTokens += token + "\n"
        
        with open("output/valid.txt", "w") as f:
            f.write(validTokens)
        with open("output/locked.txt", "w") as f:
            f.write(lockedTokens)
        with open("output/invalid.txt", "w") as f:
            f.write(invalidTokens)

        input(); cls(); _base.main()

    def settings():
        with open("settings.json", "r") as f:
            settings = json.load(f)
        cls()
        print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(f'[1] Thread Amount: {settings["threads"]}\n[2] Return')))
        choice = input(Colorate.Horizontal(Colors.blue_to_purple, "$> "))

        if choice == "1": 
            amount = input(Colorate.Horizontal(Colors.blue_to_purple, "AMOUNT $> "))
            try:
                int(amount)
            except:
                print(Colorate.Horizontal(Colors.blue_to_purple, "ITS NOT AN INTERGER!")); input(); _modules.settings()
            if int(amount) > 14:
                print(Colorate.Horizontal(Colors.blue_to_purple, "YOU ONLY CAN DO <14"))
            settings["threads"] = int(amount)

            with open("settings.json", "w") as f:
                json.dump(settings, f)

            cls(); _base.main()
        elif choice == "2":
            cls(); _base.main()
        else:
            cls(); _modules.settings()

class _base:
    def main():
        ctypes.windll.kernel32.SetConsoleTitleW("TokenZ | .gg/boostware")
        print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(pyfiglet.figlet_format("TokenZ"))))
        print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter("made by tear#3925")), end="\n\n")
        print(Colorate.Horizontal(Colors.blue_to_purple, Center.XCenter(Box.DoubleCube("[1] Check Tokens \n[2] Settings \n[3] Exit"))))
        choice = input(Colorate.Horizontal(Colors.blue_to_purple, "$> "))
        if choice == "1": _modules.checker()
        elif choice == "2": _modules.settings()
        elif choice == "3": os._exit(0)
        else: cls(); _base.main()


if __name__ == "__main__":
    cls(); _base.main()