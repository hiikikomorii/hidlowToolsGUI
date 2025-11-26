from colorama import init, Fore, Style
import psutil, socket, platform
import os
from datetime import date, datetime
import requests


init(autoreset=True)


def help_debug_cmd():
    print(f"""
clear
info
myip
help
time
exit
reboot
fgblue
fgred
fgyellow
fggreen
fgpurple
fgwhite
ping number
ping ip
ping latlon
ping btc
ping ton

{Style.BRIGHT}подробный список команд: [GUI] -> info -> about console
""")

def clear_cmd():
    os.system("cls")
    print(f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}Канал с обновлениями - https://t.me/+wF7Os8GIEBlkZmNi")
    print(f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}creator: https://t.me/Hidlow")

def exit_cmd():
    print(Fore.RED + "Выход...")
    exit()

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

    print(f"Name:{Style.BRIGHT} {sys1}")
    print(f"OS:{Style.BRIGHT} {sys2}")
    print(f"Machine:{Style.BRIGHT} {sys3}")
    print(f"processor:{Style.BRIGHT} {sys4}")
    print(f"CPU count:{Style.BRIGHT} {sys5}")
    print(f"CPU usage:{Style.BRIGHT} {sys6}")
    print(f"Memory:{Style.BRIGHT} {sys7}")

    print(f"Py Version:{Style.BRIGHT} {syspy1}")
    print(f"Py Build:{Style.BRIGHT} {syspy2}")
    print(f"Py Compiler:{Style.BRIGHT} {syspy3}")



def ipconfig_cmd():

    ipv4 = requests.get("https://api.ipify.org").text
    local_ip = socket.gethostbyname(socket.gethostname())

    print(f"IPv4: {Style.BRIGHT}{ipv4}")
    print(f"Local IP: {Style.BRIGHT}{local_ip}")


def date_cmd():

    time1 = datetime.now().strftime("%H:%M:%S")
    data1 = date.today()

    print(f"date: {Style.BRIGHT}{data1}", end=" | ")
    print(f"time: {Style.BRIGHT}{time1}")



def main():

    commands = {
        "clear": clear_cmd,
        "exit": exit_cmd,
        "help": help_debug_cmd,
        "info": info_cmd,
        "myip": ipconfig_cmd,
        "time": date_cmd,
    }

    while True:
        cmd = input("> ").strip().lower()
        if not cmd:
            continue
        if cmd in commands:
            commands[cmd]()
        else:
            print(f"{Fore.RED}неизвестная команда: {cmd}. Введите 'help' для списка команд.")

if __name__ == '__main__':
    main()