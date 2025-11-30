import subprocess
import sys
import ctypes
try:
    from pynput.keyboard import Controller, Key
    import time
    from colorama import init, Fore

except ModuleNotFoundError as e:
    boot_path = "../../boot_loader.py"
    subprocess.Popen(
        ["cmd", "/c", sys.executable, str(boot_path)],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    sys.exit()

init(autoreset=True)
keyboard = Controller()

def trooll():
    try:
        with open("text.txt", "r", encoding="utf-8") as f:
            words = f.read().splitlines()
    except Exception as error_txt:
        ctypes.windll.user32.MessageBoxW(0, f"Сборка повреждена\ntxt не найден\n{error_txt}\nПроверьте совместимость сборки","troll", 0x10)
        sys.exit()

    i = 0

    print(Fore.LIGHTCYAN_EX + "1 - start  2 - exit")
    while True:
        troll_cmd = input("> ").strip()
        if troll_cmd == "1":
            print(Fore.LIGHTCYAN_EX + "выберите скорость вывода (оптимально от 0.5)")
            time1231 = float(input("> "))
            while True:

                print(Fore.BLUE + "wait 5 sec")
                time.sleep(5)

                while i < len(words):

                    for _ in range(10):
                        if i >= len(words):
                            print(f"{Fore.LIGHTRED_EX}Скрипт закончен")
                            break

                        keyboard.type(words[i])
                        keyboard.press(Key.enter)
                        keyboard.release(Key.enter)
                        time.sleep(time1231)
                        i += 1

                    input(f"{Fore.BLUE}Нажми Enter, чтобы продолжить...")
                    print(Fore.BLUE + " wait 3 sec")
                    time.sleep(3)
        elif troll_cmd == "2":
            sys.exit()

        else:
            print(Fore.LIGHTCYAN_EX + "1 - start  2 - exit")


trooll()