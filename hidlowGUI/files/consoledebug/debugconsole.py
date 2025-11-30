

try:
    import sys
    from colorama import init, Fore, Style
    import psutil, socket, platform
    import os, subprocess
    from datetime import date, datetime
    import requests
    from colorama import init, Fore, Style
    from phonenumbers import carrier, geocoder, timezone, parse, is_valid_number
    import phonenumbers
    import requests
    import json, urllib.request
    import sys
    import random
    import qrcode
    import re
    import time
    from pingapi_func import try_ping_number, send_request_ping, try_ping_ll, try_ping_btc, try_ping_ton, try_ping_ip, check_internet, onlypingarg
    import threading
    import ctypes
except ModuleNotFoundError as e:
    print(f"Модуль {e.name} не найден.\nУстановите {e.name}")
    text_wdll = f"Модуль {e.name} не найден.\nУстановите {e.name}"

    ctypes.windll.user32.MessageBoxW(0, text_wdll, "console", 0x10)
    sys.exit()

init(autoreset=False)

_orig_white = Fore.WHITE
_orig_white_ex = Fore.LIGHTWHITE_EX


def help_cmd():
    print(f"""{Fore.LIGHTWHITE_EX}
clear
info
myip
help
time
exit
reboot
fg blue
fg cyan
fg red
fg white
ping number
ping ip
ping latlon
ping btc
ping ton

{Style.BRIGHT}подробное описание команд: [GUI] -> info -> about console
""")


def clear_cmd():
    os.system("cls")


def exit_cmd():
    print(Fore.RED + "Выход...")
    sys.exit()

def info_cmd():
    sys1 = platform.node()
    sys2 = platform.platform()
    sys3 = platform.machine()
    sys4 = platform.processor()
    sys5 = psutil.cpu_count()
    sys6 = psutil.cpu_percent(interval=1)
    sys7 = psutil.virtual_memory()

    syspy1 = platform.python_version()
    syspy2 = platform.python_build()
    syspy3 = platform.python_compiler()

    try:
        print(f"{Fore.WHITE}Name:{Fore.LIGHTWHITE_EX}{Style.BRIGHT} {sys1}")
        print(f"{Fore.WHITE}OS:{Fore.LIGHTWHITE_EX}{Style.BRIGHT} {sys2}")
        print(f"{Fore.WHITE}Machine:{Fore.LIGHTWHITE_EX}{Style.BRIGHT} {sys3}")
        print(f"{Fore.WHITE}processor:{Fore.LIGHTWHITE_EX}{Style.BRIGHT} {sys4}")
        print(f"{Fore.WHITE}CPU count:{Fore.LIGHTWHITE_EX}{Style.BRIGHT} {sys5}")
        print(f"{Fore.WHITE}CPU usage:{Fore.LIGHTWHITE_EX}{Style.BRIGHT} {sys6}")
        print(f"{Fore.WHITE}Memory:{Fore.LIGHTWHITE_EX}{Style.BRIGHT} {sys7}")

        print(f"{Fore.WHITE}Py Version:{Fore.LIGHTWHITE_EX}{Style.BRIGHT} {syspy1}")
        print(f"{Fore.WHITE}Py Build:{Fore.LIGHTWHITE_EX}{Style.BRIGHT} {syspy2}")
        print(f"{Fore.WHITE}Py Compiler:{Fore.LIGHTWHITE_EX}{Style.BRIGHT} {syspy3}")
    except Exception as error_sysinfo:
        print(f"{Fore.RED}error info about system\n{error_sysinfo}")


def reboot_cmd():
    try:
        script_path = os.path.abspath(__file__)
        subprocess.Popen(
            ["cmd", "/k", sys.executable, str(script_path)],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        time.sleep(2)
        sys.exit()
    except Exception as error_reboot:
        print(f"{Fore.RED} Reboot error.\n{error_reboot}")

def ipconfig_cmd():

    ipv4 = requests.get("https://api.ipify.org").text
    local_ip = socket.gethostbyname(socket.gethostname())

    print(f"{Fore.WHITE}IPv4: {Fore.LIGHTWHITE_EX}{Style.BRIGHT}{ipv4}")
    print(f"{Fore.WHITE}Local IP: {Fore.LIGHTWHITE_EX}{Style.BRIGHT}{local_ip}")


def date_cmd():

    time1 = datetime.now().strftime("%H:%M:%S")
    data1 = date.today()

    print(f"{Fore.WHITE}date: {Fore.LIGHTWHITE_EX}{Style.BRIGHT}{data1}", end=" | ")
    print(f"{Fore.WHITE}time: {Fore.LIGHTWHITE_EX}{Style.BRIGHT}{time1}")


def onlyfgarg():
    print(Fore.LIGHTWHITE_EX + "fg red, blue, cyan, white")
def fgred_cmd():
    Fore.WHITE = Fore.RED
    Fore.LIGHTWHITE_EX = Fore.LIGHTRED_EX
def fgwhite_cmd():
    Fore.WHITE = _orig_white
    Fore.LIGHTWHITE_EX = _orig_white_ex
def fgblue_cmd():
    Fore.WHITE = Fore.BLUE
    Fore.LIGHTWHITE_EX = Fore.LIGHTBLUE_EX
def fgcyan_cmd():
    Fore.WHITE = Fore.CYAN
    Fore.LIGHTWHITE_EX = Fore.LIGHTCYAN_EX


def try_ping_number_cmd():
    print(Fore.LIGHTWHITE_EX +
    "wait..")
    user_iput = "+79268471359"
    phone = re.sub(r"\D", "", user_iput)

    if check_internet():
        a = try_ping_number(phone)
        print(a)
    else:
        print(f"{Fore.RED}Отсутствует интернет-соединение!")

def main():
    commands = {
        "clear": clear_cmd,
        "exit": exit_cmd,
        "info": info_cmd,
        "myip": ipconfig_cmd,
        "help": help_cmd,
        "time": date_cmd,
        "reboot": reboot_cmd,
        "fg blue": fgblue_cmd,
        "fg cyan": fgcyan_cmd,
        "fg red": fgred_cmd,
        "fg white": fgwhite_cmd,
        "fg": onlyfgarg,
        "ping number": try_ping_number_cmd,
        "ping ip": try_ping_ip,
        "ping latlon": try_ping_ll,
        "ping btc": try_ping_btc,
        "ping ton": try_ping_ton,
        "ping": onlypingarg
    }


    while True:
        cmd = input(Fore.WHITE + "> ").strip().lower()
        if not cmd:
            continue
        if cmd in commands:
            commands[cmd]()
        else:
            print(f"{Style.BRIGHT}{Fore.RED}неизвестная команда: {cmd}. Введите 'help' для списка команд.")

if __name__ == '__main__':
    main()