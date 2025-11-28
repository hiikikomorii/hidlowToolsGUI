try:
    import os
    import tkinter as tk
    import requests
    import random
    import time
    from PIL import Image, ImageTk
    from colorama import init, Fore, Style
    import qrcode
    import psutil, socket, platform
    from datetime import date, datetime
    import json
    from phonenumbers import carrier, geocoder, timezone, parse, is_valid_number
    import phonenumbers
    import urllib.request
    import sys
    import re
    import subprocess
    import threading
    import queue
    from faker import Faker

except ModuleNotFoundError as e:
    print(f"Модуль {e.name} не найден.\nУстановите {e.name}")


root = tk.Tk()
init(autoreset=True)
cmd_queue = queue.Queue()
stop_flag = False

_orig_blue = Fore.BLUE
_orig_lightblue_ex = Fore.LIGHTBLUE_EX
_orig_cyan = Fore.CYAN
_orig_lightcyan_ex = Fore.LIGHTCYAN_EX


print(f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}Канал с обновлениями - https://t.me/+wF7Os8GIEBlkZmNi")
print(f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}creator: https://t.me/Hidlow")

time1 = datetime.now().strftime("%H:%M:%S")
data1 = date.today()

print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTCYAN_EX}Дата & время запуска: {Style.BRIGHT}{data1}, {time1}")


# настройка gui
root.configure(bg="black")
root.attributes("-fullscreen", True)
root.title("HidlowTools-GUI")


#eto api
def select_api1():
    prepare_input(api_number)

def select_api2():
    prepare_input(api_ip)

def select_api3():
    prepare_input(api_lat)

def select_qrcode():
    prepare_input(qrcodee)

def select_gptchc():
    prepare_input(gptchc)


def select_about():
    prepare_about()

def select_custom2():
    select_custom(custombg)

def select_custom(api_func2):
    hide_settings()
    menu_frame.pack_forget()
    menu_frame2.pack_forget()
    clear_entry_frame()
    entry_frame.pack(pady=10)
    confirm_button.config(command=api_func2)

def select_currency():
    hide_settings()
    menu_frame.pack_forget()
    menu_frame2.pack_forget()
    currency_frame.pack(pady=10)
    currencyback_button.config(command=go_back)

def select_faker():
    hide_settings()
    menu_frame.pack_forget()
    menu_frame2.pack_forget()
    faker_frame.pack(pady=10)
    fakerback_button.config(command=go_back)

#prepare about
def prepare_about():
    hide_settings()
    menu_frame.pack_forget()
    menu_frame2.pack_forget()
    about_frame.pack(pady=10)
    aboutback_button.config(command=go_back)


#prepare api
def prepare_input(api_func):
    hide_settings()
    menu_frame.pack_forget()
    menu_frame2.pack_forget()
    clear_entry_frame()
    entry_frame.pack(pady=10)
    confirm_button.config(command=api_func)


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/119.0",
]

headers = {
    "User-Agent": random.choice(user_agents),
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "TE": "Trailers"
}

def send_request(url, phone):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        time.sleep(random.uniform(2, 5))
        if response.status_code == 200:
            print(f"{Fore.BLUE}{Style.BRIGHT}[NUMBER]{Style.NORMAL} {Fore.LIGHTGREEN_EX}Запрос выполнен успешно: {phone}")
            return response.json()
        else:
            print(f"{Fore.BLUE}{Style.BRIGHT}[NUMBER]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка: {response.status_code}")
            return None
    except Exception as er:
        print(f"{Fore.BLUE}{Style.BRIGHT}[NUMBER]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка при отправке запроса: {er}")
        return None

def api_number():
    user_input = entry.get().strip()
    clear_entry_frame()
    output_label.pack_forget()
    if not user_input:
        output_label.config(text="Введите номер телефона!", fg="red")
        output_label.pack(pady=5)
        print(f"{Fore.BLUE}{Style.BRIGHT}[NUMBER]{Style.NORMAL} {Fore.LIGHTYELLOW_EX}Номер телефона не был введен.")
        return

    try:
        copyable = tk.Text(
            entry_frame,
            width=80,
            height=17,
            bg="black",
            fg="white",
            font=("Consolas", 11),
            wrap="word"
        )
        copyable.pack(padx=20, pady=20)

        url = f"https://htmlweb.ru/geo/api.php?json&telcod={user_input}"
        data = send_request(url, user_input)

        if not data or not isinstance(data, dict):
            copyable.insert("1.0", "[!] Ошибка: не удалось получить данные.")
            print(f"{Fore.BLUE}{Style.BRIGHT}[NUMBER]{Style.NORMAL} {Fore.LIGHTRED_EX}[!] Ошибка: не удалось получить данные.")
            return

        if data.get("status_error"):
            copyable.insert("1.0", f"Ошибка API: {data.get('error_message', 'Не удалось получить данные.')}")
            print(f"{Fore.BLUE}{Style.BRIGHT}[NUMBER]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка API: {data.get('error_message', 'Не удалось получить данные.')}")
            return

        if data.get("limit") is not None and data.get("limit") <= 0:
            copyable.insert("1.0", "Ошибка: лимит запросов исчерпан.")
            print(f"{Fore.BLUE}{Style.BRIGHT}[NUMBER]{Style.NORMAL} {Fore.LIGHTRED_EX}Лимит исчерпан!")
            return


        country = data.get('country', {}) or {}
        region = data.get('region', {}) or {}
        capital = data.get('capital', {}) or {}


        text = (
            f"Номер телефона: {user_input}\n"
            f"Страна: {country.get('name', 'Не найдено')} ({country.get('fullname', '—')})\n"
            f"Регион: {region.get('name', 'Не найдено')}\n"
            f"Город: {capital.get('name', 'Не найдено')}\n"
            f"Почтовый индекс: {capital.get('post', 'Не найдено')}\n"
            f"Код валюты: {country.get('iso', 'Не найдено')}\n"
            f"Телефонный код: {capital.get('telcod', 'Не найдено')}\n"
            f"Оператор: {capital.get('oper_brand', 'Не найдено')} ({capital.get('def', 'Не найдено')})\n"
            f"Столица: {capital.get('name', 'Не найдено')}\n"
            f"Широта / Долгота: {capital.get('latitude', '—')}, {capital.get('longitude', '—')}\n"
            f"Wiki: {capital.get('wiki', '—')}\n"
            f"Автокод региона: {region.get('autocod', '—')}\n"
            f"Локация: {country.get('location', '—')}\n"
            f"Язык: {country.get('lang', '—')}\n"
            f"Google Maps: https://www.google.com/maps/place/{capital.get('latitude', '')}+{capital.get('longitude', '')}\n"
            f"Рейтинг номера: https://phoneradar.ru/phone/{user_input}\n"
        )

        copyable.insert("1.0", text)
        make_copyable_readonly(copyable)
        print(f"{Fore.BLUE}{Style.BRIGHT}[NUMBER]{Style.NORMAL} {Fore.LIGHTGREEN_EX}Запрос выполнен: {user_input}")

    except Exception as er:
        output_label.config(text=f"Ошибка API: {er}", fg="red")
        print(f"{Fore.BLUE}{Style.BRIGHT}[NUMBER]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка API: {er}")




def api_ip():
    user_input = entry.get().strip()
    clear_entry_frame()
    output_label.pack_forget()
    if not user_input:
        output_label.config(text="Введите ip!", fg="red")
        output_label.pack(pady=5)
        print(f"{Fore.BLUE}{Style.BRIGHT}[IP]{Style.NORMAL} {Fore.LIGHTYELLOW_EX}IP не был введен")
        return

    try:
        copyable = tk.Text(
            entry_frame,
            width=60,
            height=20,
            bg="black",
            fg="white",
            font=("Arial", 14),
            wrap="word"
        )
        copyable.pack(padx=20, pady=20)

        response = requests.get(f"https://ipwhois.app/json/{user_input}")
        data = response.json()


        text = (
            f"IP: {data.get('ip', 'не найдено')}\n"
            f"Континент: {data.get('continent', 'не найдено')}\n"
            f"Страна: {data.get('country', "не найдено")}\n"
            f"Столица: {data.get('country_capital', 'не найдено')}\n"
            f"Регион: {data.get('region', 'не найдено')}\n"
            f"Город: {data.get('city', 'не найдено')}\n"
            f"Соседние страны: {data.get('country_neighbours', 'не найдено')}\n"
            f"Флаг: {data.get('country_flag', 'не найдено')}\n"
            f"Код телефона: {data.get("country_phone", "не найдено")}\n"
            f"Провайдер: {data.get('isp', 'не найдено')}\n" 
            f"Организация: {data.get('org', 'не найденo')}\n"           
            f"Часовой пояс: {data.get('timezone', 'не найдено')}\n"          
            f"Валюта: {data.get('currency', 'не найдено')}\n"
        )

        copyable.insert("1.0", text)
        make_copyable_readonly(copyable)
        print(f"{Fore.BLUE}{Style.BRIGHT}[IP]{Style.NORMAL} {Fore.LIGHTGREEN_EX}Запрос выполнен: {user_input}")

    except Exception as er:
        output_label.config(text=f"Ошибка API-IP: {er}", fg="red")
        print(f"{Fore.BLUE}{Style.BRIGHT}[IP]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка API-IP: {er}")

def api_lat():
    user_input = entry.get().strip()
    clear_entry_frame()
    output_label.pack_forget()
    if not user_input:
        output_label.config(text="Введите координаты (lat lon)", fg="red")
        output_label.pack(pady=5)
        print(f"{Fore.BLUE}{Style.BRIGHT}[LatLon]{Style.NORMAL} {Fore.LIGHTYELLOW_EX}Координаты не были введены.")
        return

    try:

        parts = user_input.split()

        if len(parts) != 2:
            output_label.config(text="Введите два значения: широта и долгота через пробел", fg="red")
            output_label.pack(pady=5)
            print(f"{Fore.BLUE}{Style.BRIGHT}[LatLon]{Style.NORMAL} {Fore.LIGHTYELLOW_EX}Координаты были введены неправильно.")
            return

        lat, lon = parts

        for widget in entry_frame.pack_slaves():
            if isinstance(widget, tk.Text):
                widget.destroy()

        copyable = tk.Text(
            entry_frame,
            width=50,
            height=6,
            bg="black",
            fg="white",
            font=("Arial", 14),
            wrap="word"
        )
        copyable.pack(padx=20, pady=20)

        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        response = requests.get(url, headers={"User-Agent": "TkinterApp"})
        data = response.json()

        text = (
            f"Страна: {data.get('address', {}).get('country', 'не найдено')}\n"
            f"Регион: {data.get('address', {}).get('state', 'не найдено')}\n"
            f"Город: {data.get('address', {}).get('city', data.get('address', {}).get('town', 'не найдено'))}\n"
            f"Почтовый индекс: {data.get('address', {}).get('postcode', 'не найдено')}\n"
            f"Полный адрес: {data.get('display_name', 'не найдено')}"
        )

        copyable.insert("1.0", text)
        make_copyable_readonly(copyable)
        print(f"{Fore.BLUE}{Style.BRIGHT}[LatLon]{Style.NORMAL} {Fore.LIGHTGREEN_EX}Запрос был выполнен: {parts}")

    except Exception as er:
        output_label.config(text=f"Ошибка API-lat: {er}", fg="red")
        print(f"{Fore.BLUE}{Style.BRIGHT}[LatLon]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка API-lat: {er}")

def qrcodee():
    user_input = entry.get().strip()

    clear_entry_frame()

    output_label.pack_forget()
    if not user_input:
        output_label.config(text="Введите URL", fg="red")
        output_label.pack(pady=5)
        print(f"{Fore.BLUE}{Style.BRIGHT}[QR]{Style.NORMAL} {Fore.LIGHTYELLOW_EX}Url не был введен.")
        return

    try:
        img = qrcode.make(user_input)
        img.save("qrcode.png")
        output_label.config(text="QRcode сохранен", fg="green")
        print(f"{Fore.BLUE}{Style.BRIGHT}[QR]{Style.NORMAL} {Fore.LIGHTGREEN_EX}QR код сгенерирован и сохранён как 'qrcodde.png'")

    except Exception as er:
        output_label.config(text="error. see log", fg="red")
        output_label.pack(pady=5)
        print(f"{Fore.BLUE}{Style.BRIGHT}[QR]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка функции qr: {er}")

def trol():
    try:
        print(f"{Fore.BLUE}{Style.BRIGHT}[TROLL]{Style.NORMAL} {Fore.LIGHTGREEN_EX}Troll was opened")
        path = r"files\troll\trollsetup.bat"
        os.startfile(path)
    except Exception as error_troll:
        button5.config(fg="#FF0000")
        print(f"{Fore.BLUE}{Style.BRIGHT}[TROLL]{Style.NORMAL} {Fore.RED}произошла ошибка при открытии 'troll'\n{error_troll}")


def select_ton():
    try:
        for widget in currency_frame.pack_slaves():
            if isinstance(widget, tk.Text):
                widget.destroy()

        copyable = tk.Text(
            currency_frame,
            width=20,
            height=3,
            bg="black",
            fg="white",
            font=("Arial", 14),
            wrap="word"
        )
        copyable.pack(padx=20, pady=20)
        print(f"{Fore.BLUE}{Style.BRIGHT}[TON]{Style.NORMAL} {Fore.LIGHTGREEN_EX}TON currency was shown")

        url = "https://api.coinpaprika.com/v1/tickers/toncoin-the-open-network?quotes=USD,RUB"
        response = requests.get(url, headers={"User-Agent": "TkinterApp"})
        data = response.json()

        quo = data.get("quotes", {})
        usd = quo.get("USD", {})
        rub = quo.get("RUB", {})

        tonusd = usd.get("price", "не найдено")
        tonrub = rub.get("price", "не найдено")

        text = (
            f"Криптовалюта: TON\n"
            f"Цена в USD: {tonusd:.2f} $\n"
            f"Цена в RUB: {tonrub:.1f} ₽"
        )

        copyable.insert("1.0", text)
        copyable.bind("<Key>", lambda s: "break")
        copyable.config(cursor="arrow")
    except Exception:
        print(f"{Fore.BLUE}{Style.BRIGHT}[TON]{Style.NORMAL} {Fore.RED}TON ERROR")

def select_btc():
    try:
        for widget in currency_frame.pack_slaves():
            if isinstance(widget, tk.Text):
                widget.destroy()

        copyable = tk.Text(
            currency_frame,
            width=21,
            height=3,
            bg="black",
            fg="white",
            font=("Arial", 14),
            wrap="word"
        )
        copyable.pack(padx=20, pady=20)
        print(f"{Fore.BLUE}{Style.BRIGHT}[BTC]{Style.NORMAL} {Fore.LIGHTGREEN_EX}BTC currency was shown")

        url = "https://api.coinpaprika.com/v1/tickers/btc-bitcoin?quotes=USD,RUB"
        response = requests.get(url, headers={"User-Agent": "TkinterApp"})
        data = response.json()

        quo = data.get("quotes", {})
        usd = quo.get("USD", {})
        rub = quo.get("RUB", {})

        btcusd = usd.get("price", "not found")
        btcrub = rub.get("price", "not found")

        text = (
            f"Криптовалюта: BTC\n"
            f"Цена в USD: {btcusd:.2f} $\n"
            f"Цена в RUB: {btcrub:.1f} ₽"
        )

        copyable.insert("1.0", text)
        copyable.bind("<Key>", lambda s: "break")
        copyable.config(cursor="arrow")

    except Exception:
        print(f"{Fore.BLUE}{Style.BRIGHT}[BTC]{Style.NORMAL} {Fore.RED}BTC ERROR")

def extract_chat(input_path, chat_name, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chat = next((conv for conv in data if conv.get("title") == chat_name), None)
    if not chat:
        print(f"{Fore.BLUE}{Style.BRIGHT}[GPTCHC]{Style.NORMAL} {Fore.RED}Чат с названием '{Style.BRIGHT}{chat_name}{Style.NORMAL}' не найден.")
        return

    messages = []
    for msg in chat.get("mapping", {}).values():
        message = msg.get("message")
        if not message:
            continue

        author = message.get("author", {}).get("role", "unknown")
        content_parts = message.get("content", {}).get("parts", [])
        text_parts = [
            part if isinstance(part, str) else str(part.get("text", part))
            for part in content_parts
        ]
        text = "\n".join(text_parts).strip()

        if text:
            prefix = {
                "user": "Вы: ",
                "assistant": "ChatGPT: ",
                "system": "[СИСТЕМА]: "
            }.get(author, "")
            messages.append(prefix + text)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(messages))

    print(f"{Fore.BLUE}{Style.BRIGHT}[GPTCHC]{Style.NORMAL} {Fore.LIGHTGREEN_EX}Чат '{Style.BRIGHT}{chat_name}{Style.NORMAL}' сохранён в {Style.BRIGHT}{output_path}{Style.NORMAL}'")


def gptchc():
    user_input = entry.get().strip()

    clear_entry_frame()

    if not user_input:
        output_label.config(text="Введите ИмяФайла.txt", fg="red")
        output_label.pack(pady=5)
        print(f"{Fore.BLUE}{Style.BRIGHT}[GPTCHC]{Style.NORMAL} {Fore.LIGHTYELLOW_EX}название файла не было введено.")
        return

    try:
        input_file = "conversations.json"
        chat_input_name = user_input
        output_file = "chat_export.txt"

        extract_chat(input_file, chat_input_name, output_file)

    except Exception as er:
        output_label.config(text="error. see log", fg="red")
        print(f"{Fore.BLUE}{Style.BRIGHT}[GPTCHC]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка функции GPTCHC: {er}")

#faker backend
def fakerru():
    for widget in faker_frame.pack_slaves():
        if isinstance(widget, tk.Text):
            widget.destroy()

    copyable = tk.Text(
        faker_frame,
        width=55,
        height=20,
        bg="black",
        fg="white",
        font=("Arial", 14),
        wrap="word"
    )
    copyable.pack(padx=20, pady=20)
    print(f"{Fore.BLUE}{Style.BRIGHT}[FAKER: RU]{Style.NORMAL} {Fore.LIGHTGREEN_EX}fake information was shown")

    fake = Faker('Ru_ru')

    ipv4f = fake.ipv4()
    addressf = fake.address()
    namef = fake.name()
    phonef = fake.phone_number()
    emailf = fake.email()
    ssnf = fake.ssn()
    cityf = fake.city()
    passwf = fake.password()

    text = f"""
    name: {namef}\n
    address: {addressf}\n
    city: {cityf}\n
    phone number: {phonef}\n
    email: {emailf}\n
    ssn: {ssnf}\n
    password: {passwf}\n
    ip: {ipv4f}\n
    """
    copyable.insert("1.0", text)
    copyable.bind("<Key>", lambda s: "break")
    copyable.config(cursor="arrow")

def fakereng():
    for widget in faker_frame.pack_slaves():
        if isinstance(widget, tk.Text):
            widget.destroy()

    copyable = tk.Text(
        faker_frame,
        width=55,
        height=20,
        bg="black",
        fg="white",
        font=("Arial", 14),
        wrap="word"
    )
    copyable.pack(padx=20, pady=20)
    print(f"{Fore.BLUE}{Style.BRIGHT}[FAKER: ENG]{Style.NORMAL} {Fore.LIGHTGREEN_EX}fake information was shown")

    fake = Faker()

    ipv4f = fake.ipv4()
    addressf = fake.address()
    namef = fake.name()
    phonef = fake.phone_number()
    emailf = fake.email()
    ssnf = fake.ssn()
    cityf = fake.city()
    passwf = fake.password()

    text = f"""
    name: {namef}\n
    address: {addressf}\n
    city: {cityf}\n
    phone number: {phonef}\n
    email: {emailf}\n
    ssn: {ssnf}\n
    password: {passwf}\n
    ip: {ipv4f}\n
    """
    copyable.insert("1.0", text)
    copyable.bind("<Key>", lambda s: "break")
    copyable.config(cursor="arrow")

def fakeres():
    for widget in faker_frame.pack_slaves():
        if isinstance(widget, tk.Text):
            widget.destroy()

    copyable = tk.Text(
        faker_frame,
        width=55,
        height=20,
        bg="black",
        fg="white",
        font=("Arial", 14),
        wrap="word"
    )
    copyable.pack(padx=20, pady=20)
    print(f"{Fore.BLUE}{Style.BRIGHT}[FAKER: KZ]{Style.NORMAL} {Fore.LIGHTGREEN_EX}fake information was shown")

    fake = Faker('es_ES')

    ipv4f = fake.ipv4()
    addressf = fake.address()
    namef = fake.name()
    phonef = fake.phone_number()
    emailf = fake.email()
    ssnf = fake.ssn()
    cityf = fake.city()
    passwf = fake.password()

    text = f"""
    name: {namef}\n
    address: {addressf}\n
    city: {cityf}\n
    phone number: {phonef}\n
    email: {emailf}\n
    ssn: {ssnf}\n
    password: {passwf}\n
    ip: {ipv4f}\n
    """
    copyable.insert("1.0", text)
    copyable.bind("<Key>", lambda s: "break")
    copyable.config(cursor="arrow")

def fakerjp():
    for widget in faker_frame.pack_slaves():
        if isinstance(widget, tk.Text):
            widget.destroy()

    copyable = tk.Text(
        faker_frame,
        width=55,
        height=20,
        bg="black",
        fg="white",
        font=("Arial", 14),
        wrap="word"
    )
    copyable.pack(padx=20, pady=20)
    print(f"{Fore.BLUE}{Style.BRIGHT}[FAKER: KZ]{Style.NORMAL} {Fore.LIGHTGREEN_EX}fake information was shown")

    fake = Faker('ja_JP')

    ipv4f = fake.ipv4()
    addressf = fake.address()
    namef = fake.name()
    phonef = fake.phone_number()
    emailf = fake.email()
    ssnf = fake.ssn()
    cityf = fake.city()
    passwf = fake.password()

    text = f"""
    name: {namef}\n
    address: {addressf}\n
    city: {cityf}\n
    phone number: {phonef}\n
    email: {emailf}\n
    ssn: {ssnf}\n
    password: {passwf}\n
    ip: {ipv4f}\n
    """
    copyable.insert("1.0", text)
    copyable.bind("<Key>", lambda s: "break")
    copyable.config(cursor="arrow")


#console
def consoleadapter(cmd):
    from files.consoledebug.debugconsole import clear_cmd, info_cmd, ipconfig_cmd, date_cmd, help_debug_cmd
    from files.apicalling_func.pingapi_func import try_ping_number, send_request_ping, try_ping_ll, try_ping_btc, try_ping_ton, try_ping_ip, check_internet

    cmd_buttonopen = None
    try:
        def cmd_buttonopen():
            root.attributes("-fullscreen", False)
            root.geometry("1280x720")
            print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTGREEN_EX}cmd was enabled")

    except Exception as error_console:
        btn4.config(fg="#FF0000")
        print(
            f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTRED_EX}произошла ошибка при открытии 'console'\n{error_console}")

    def remotebot_open():
        try:
            bot_path = r"files\remotebot\remote.bat"
            os.startfile(bot_path)
        except Exception:
            print(f"{Fore.RED}{Style.BRIGHT}Данная функция доступна только владельцу")

    def try_ping_number_cmd():
        print("wait..")
        user_iput = "+79268471359"
        phone = re.sub(r"\D", "", user_iput)

        if check_internet():
            a = try_ping_number(phone)
            print(a)
        else:
            print(f"{Fore.RED}Отсутствует интернет-соединение!")

    def try_ping_ip_cmd():
        try_ping_ip()

    def try_ping_ll_cmd():
        try_ping_ll()

    def try_ping_btc_cmd():
        try_ping_btc()

    def try_ping_ton_cmd():
        try_ping_ton()

    def help_cmd():
        help_debug_cmd()

    def clear_cmd11():
        clear_cmd()

    def info_cmd11():
        info_cmd()

    def ipconfig_cmd11():
        ipconfig_cmd()

    def date_cmd11():
        date_cmd()

    def reboot_cmd():
        print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.RED}restart GUI..")
        path = r"hidlowgui.bat"
        os.startfile(path)
        time.sleep(2)
        root.destroy()


    def fgred_cmd():
        Fore.BLUE = Fore.RED
        Fore.LIGHTBLUE_EX = Fore.LIGHTRED_EX
        Fore.CYAN = Fore.RED
        Fore.LIGHTCYAN_EX = Fore.LIGHTRED_EX

    def fgyellow_cmd():
        Fore.BLUE = Fore.YELLOW
        Fore.LIGHTBLUE_EX = Fore.YELLOW
        Fore.CYAN = Fore.YELLOW
        Fore.LIGHTCYAN_EX = Fore.YELLOW

    def fggreen_cmd():
        Fore.BLUE = Fore.GREEN
        Fore.LIGHTBLUE_EX = Fore.LIGHTGREEN_EX
        Fore.CYAN = Fore.GREEN
        Fore.LIGHTCYAN_EX = Fore.LIGHTGREEN_EX

    def fgpurple_cmd():
        Fore.BLUE = Fore.MAGENTA
        Fore.LIGHTBLUE_EX = Fore.LIGHTMAGENTA_EX
        Fore.CYAN = Fore.MAGENTA
        Fore.LIGHTCYAN_EX = Fore.LIGHTMAGENTA_EX

    def fgwhite_cmd():
        Fore.BLUE = Fore.WHITE
        Fore.LIGHTBLUE_EX = Fore.LIGHTWHITE_EX
        Fore.CYAN = Fore.WHITE
        Fore.LIGHTCYAN_EX = Fore.LIGHTWHITE_EX


    def fgdef_cmd():
        Fore.BLUE = _orig_blue
        Fore.LIGHTBLUE_EX = _orig_lightblue_ex
        Fore.CYAN = _orig_cyan
        Fore.LIGHTCYAN_EX = _orig_lightcyan_ex



    commands = {
        "clear": clear_cmd11,
        "info": info_cmd11,
        "myip": ipconfig_cmd11,
        "help": help_cmd,
        "time": date_cmd11,
        "reboot": reboot_cmd,
        "fgblue": fgdef_cmd,
        "fgred": fgred_cmd,
        "fgyellow": fgyellow_cmd,
        "fggreen": fggreen_cmd,
        "fgpurple": fgpurple_cmd,
        "fgwhite": fgwhite_cmd,
        "ping number": try_ping_number_cmd,
        "ping ip": try_ping_ip_cmd,
        "ping latlon": try_ping_ll_cmd,
        "ping btc": try_ping_btc_cmd,
        "ping ton": try_ping_ton_cmd,
        "remote": remotebot_open,
        "consoleopened": cmd_buttonopen
    }

    if not cmd:
        pass
    if cmd in commands:
        commands[cmd]()
    else:
        print(f"{Fore.RED}неизвестная команда: {cmd}. список команд: [GUI] -> info -> about console")

#console potok
def console_thread():
    while not stop_flag:
        try:
            cmd = input("> ").strip().lower()
            if cmd:
                cmd_queue.put(cmd)
            if cmd == "exit":
                break
        except EOFError:
            break
        except Exception:
            print(Fore.RED + "console_thread наебнулась, hidlow eblan")
            break


def check_queue():
    while not cmd_queue.empty():
        cmd = cmd_queue.get()
        consoleadapter(cmd)
    if not stop_flag:
        root.after(100, check_queue)


# about
def about_project():
    for widget in about_frame.pack_slaves():
        if isinstance(widget, tk.Text):
            widget.destroy()

    copyable = tk.Text(
        about_frame,
        width=70,
        height=42,
        bg="black",
        fg="white",
        font=("Arial", 14),
        wrap="word"
    )
    copyable.pack(padx=20, pady=20)
    print(f"{Fore.BLUE}{Style.BRIGHT}[ABOUT: project]{Style.NORMAL} {Fore.LIGHTGREEN_EX}about was shown")
    text = f"""
    number - показывает информацию о введенном номере\n
    ip - показывает информацию о введенном ip\n
    lat/lon - показывает информаю по введенной долготе(lat) и широте(lon)\n
    qrcode - создает qrcode.png которая содержит вашу ссылку\n
    troll - отдельный скрипт который троллится за вас используя pr.txt\n
    currency - выводит курс о BTC и TON в $ & ₽\n
    GPT CHC - Gpt chat history converter.\n
    - вытаскивает .json файл и переводит его в .txt для чтения\n
    Faker - генерирует фейк данные.\n
    \n
    background имеет 5 задних фонов: белый, черный, синий, красный, фиолетовый\n
    fullscreen меняет размер окна из полноэкранного режима в 1280x720\n
    console - с помощью нее вы можете работать с консолью. команды в 'about console'\n\n
    Версия: BETA Alldebug\n
    Всего строк: 1420\n"""

    copyable.insert("1.0", text)
    copyable.bind("<Key>", lambda s: "break")
    copyable.config(cursor="arrow")


def consoleabout():
    for widget in about_frame.pack_slaves():
        if isinstance(widget, tk.Text):
            widget.destroy()

    copyable = tk.Text(
        about_frame,
        width=50,
        height=26,
        bg="black",
        fg="white",
        font=("Arial", 14),
        wrap="word"
    )
    copyable.pack(padx=20, pady=20)
    print(f"{Fore.BLUE}{Style.BRIGHT}[ABOUT: console]{Style.NORMAL} {Fore.LIGHTGREEN_EX}project stats was shown")

    text = f"""
    доступные команды:\n
    clear - очистка консоли\n
    info - детальная информация о системе и python\n
    myip - ваш локальный ip\n
    help - список команд\n
    time - актуальная дата и время\n
    reboot - перезапускает GUI\n
    fg[color] - меняет цвет тега на введенный в [color]
    доступные цвета: red, blue, green, yellow, purple, white.
    пример: fgred\n
    ping [func] - проверяет работоспособность API
    доступные функции: number, latlon, ip, btc, ton
    """
    copyable.insert("1.0", text)
    copyable.bind("<Key>", lambda s: "break")
    copyable.config(cursor="arrow")

#это настройки
def toggle_settings():
    if settings_frame.winfo_ismapped():
        settings_frame.pack_forget()
    else:
        settings_frame.pack(padx=1, pady=1)

def toggle_fullscreen():
    is_fullscreen = root.attributes("-fullscreen")
    if is_fullscreen:
        root.attributes("-fullscreen", False)
        root.geometry("1280x720")
        btn1.config(fg="#CF0000", activeforeground="#CF0000")
        print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTGREEN_EX}RootGeometry '1280x720'")
    else:
        root.attributes("-fullscreen", True)
        btn1.config(activeforeground="#00CF00", fg="#00CF00")
        print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTGREEN_EX}RootGeometry 'fullscreen'")

def open_folder():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.startfile(current_dir)
        print(f"{Fore.BLUE}{Style.BRIGHT}[FOLDER]{Style.NORMAL} {Fore.LIGHTGREEN_EX}директория 'HidlowGUI' успешно открыта")

    except Exception as error_folder:
        btn3.config(fg="#FF0000")
        print(f"{Fore.BLUE}{Style.BRIGHT}[FOLDER]{Style.NORMAL} {Fore.RED}Произошла ошибка при открытии 'folder'\n{error_folder}")


def exitt():
    global stop_flag
    stop_flag = True
    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.RED}Выход из программы")
    root.destroy()

def menu_reboot():
    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.RED}restart GUI..")
    root.geometry("100x100")
    time.sleep(1)
    path = r"hidlowgui.bat"
    os.startfile(path)
    time.sleep(2)
    root.destroy()

#это логика кнопок
def go_back_from_entry():
    entry_frame.pack_forget()
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.pack_forget()
    menu_frame.pack(pady=20)
    menu_frame2.pack(pady=20)

def go_back():
    entry_frame.pack_forget()
    about_frame.pack_forget()
    currency_frame.pack_forget()
    faker_frame.pack_forget()
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.pack_forget()
    menu_frame.pack(pady=20)
    menu_frame2.pack(pady=20)

def hide_settings():
    if settings_frame.winfo_ismapped():
        settings_frame.pack_forget()

def clear_entry_frame():
    entry.delete(0, tk.END)
    for widget in entry_frame.winfo_children():
        if isinstance(widget, tk.Text):
            widget.destroy()

def make_copyable_readonly(text_widget):
    def on_key(event):
        if event.state & 0x4 and event.keysym.lower() in ("c", "v", "x", "a"):
            return
        return "break"

    text_widget.bind("<Key>", on_key)
    text_widget.bind("<Control-c>", lambda er: None)
    text_widget.bind("<Control-C>", lambda er: None)
    text_widget.bind("<Control-v>", lambda er: text_widget.event_generate("<<Paste>>"))
    text_widget.bind("<Control-V>", lambda er: text_widget.event_generate("<<Paste>>"))
    text_widget.bind("<Control-a>", lambda er: text_widget.event_generate("<<SelectAll>>"))
    text_widget.bind("<Control-A>", lambda er: text_widget.event_generate("<<SelectAll>>"))

    text_widget.bind("<Button-1>", lambda er: None)
    text_widget.bind("<B1-Motion>", lambda er: None)

    text_widget.config(cursor="arrow")
    text_widget.config(state="normal")

    def enable_copy_paste():
        text_widget.config(state="normal")
        text_widget.clipboard_clear()
        text_widget.event_generate("<<Copy>>")
        text_widget.config(state="normal")

    text_widget.bind("<Control-c>", lambda er: enable_copy_paste())

def custombg():
    user_input = entry.get().strip()
    if not user_input:
        print("Введите цвет!")
        return

    try:
        bg_label.destroy()

        root.config(bg=user_input)
        print(f"Цвет изменён на {user_input}")
    except Exception:
        print(f"'{user_input}' - некорректный цвет!")

# переменные фона
# 1-black 2-white 3-blue 4-red 5-magenta
btn2 = None

bg1 = None
bg2 = None
bg3 = None
bg4 = None
bg5 = None

exitbuttonbg1 = None
exitbuttonbg2 = None
exitbuttonbg3 = None
exitbuttonbg4 = None
exitbuttonbg5 = None

rebootbuttonbg1 = None
rebootbuttonbg2 = None
rebootbuttonbg3 = None
rebootbuttonbg4 = None
rebootbuttonbg5 = None

try:
    image1 = Image.open("assets/bg_assets/bg1.jpg").resize((1920, 1080))
    image2 = Image.open("assets/bg_assets/bg2.jpg").resize((1920, 1080))
    image3 = Image.open("assets/bg_assets/bg3.jpg").resize((1920, 1080))
    image4 = Image.open("assets/bg_assets/bg4.jpg").resize((1920, 1080))
    image5 = Image.open("assets/bg_assets/bg5.jpg").resize((1920, 1080))

    exitbuttonbg1 = Image.open("assets/exit_assets/exitbutton1.png").resize((27, 27))
    exitbuttonbg2 = Image.open("assets/exit_assets/exitbutton2.png").resize((27, 27))
    exitbuttonbg3 = Image.open("assets/exit_assets/exitbutton3.png").resize((27, 27))
    exitbuttonbg4 = Image.open("assets/exit_assets/exitbutton4.png").resize((27, 27))
    exitbuttonbg5 = Image.open("assets/exit_assets/exitbutton5.png").resize((27, 27))

    rebootbuttonbg1 = Image.open("assets/reboot_assets/rebootbutton1.png").resize((25, 25))
    rebootbuttonbg2 = Image.open("assets/reboot_assets/rebootbutton2.png").resize((25, 25))
    rebootbuttonbg3 = Image.open("assets/reboot_assets/rebootbutton3.png").resize((25, 25))
    rebootbuttonbg4 = Image.open("assets/reboot_assets/rebootbutton4.png").resize((25, 25))
    rebootbuttonbg5 = Image.open("assets/reboot_assets/rebootbutton5.png").resize((25, 25))

    bg1 = ImageTk.PhotoImage(image1)
    bg2 = ImageTk.PhotoImage(image2)
    bg3 = ImageTk.PhotoImage(image3)
    bg4 = ImageTk.PhotoImage(image4)
    bg5 = ImageTk.PhotoImage(image5)

    exitbuttonbg1 = ImageTk.PhotoImage(exitbuttonbg1)
    exitbuttonbg2 = ImageTk.PhotoImage(exitbuttonbg2)
    exitbuttonbg3 = ImageTk.PhotoImage(exitbuttonbg3)
    exitbuttonbg4 = ImageTk.PhotoImage(exitbuttonbg4)
    exitbuttonbg5 = ImageTk.PhotoImage(exitbuttonbg5)

    rebootbuttonbg1 = ImageTk.PhotoImage(rebootbuttonbg1)
    rebootbuttonbg2 = ImageTk.PhotoImage(rebootbuttonbg2)
    rebootbuttonbg3 = ImageTk.PhotoImage(rebootbuttonbg3)
    rebootbuttonbg4 = ImageTk.PhotoImage(rebootbuttonbg4)
    rebootbuttonbg5 = ImageTk.PhotoImage(rebootbuttonbg5)

except Exception as b:
    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка Background : {b}")
    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTRED_EX}Bg отсутствует в сборке")
    btn2.config(fg="red")


# label фон
bg_label = tk.Label(root, image=bg1)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


bg_state = 1

def change_background():
    global bg_state

    if bg_state == 1:
        bg_label.config(image=bg2)
        bg_label.image = bg2

        exitadapter_button.config(image=exitbuttonbg2)
        rebootbutton_button.config(image=rebootbuttonbg2)

        print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTGREEN_EX}BackGround изменен на 'bg1.jpg'{Fore.RESET} | {Style.BRIGHT}WHITE")

        for frame in (menu_frame, menu_frame2, entry_frame, about_frame, currency_frame, faker_frame, output_label):
            frame.config(bg="#DDE2E8")
            for widget in frame.winfo_children():
                try:
                    if isinstance(widget, tk.Button):
                        widget.config(
                            bg="#858585",
                            fg="white",
                            activebackground="#858585",
                            activeforeground="white"
                        )

                        settings_frame.config(bg="#E0E3E8")
                        about_btn.config(bg="#545454", activebackground="#444444")
                        settings_button.config(bg="#545454", activebackground="#444444")
                        btn1.config(bg="#545454", activebackground="#444444")
                        btn2.config(bg="#545454", activebackground="#444444")
                        btn3.config(bg="#545454", activebackground="#444444")
                        btn4.config(bg="#545454", activebackground="#444444")
                        exitadapter_button.config(bg="#DDE2E8", activebackground="#DDE2E8")
                        rebootbutton_button.config(bg="#DDE2E8", activebackground="#DDE2E8")

                        confirm_button.config(fg="#00CF00", activeforeground="#00CF00")

                        fakerback_button.config(fg="red", activeforeground="red")
                        currencyback_button.config(fg="red", activeforeground="red")
                        aboutback_button.config(fg="red", activeforeground="red")
                        back_button.config(fg="red", activeforeground="red")

                except Exception as a:
                    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка background: {a}")

        bg_state = 2


    elif bg_state == 2:
        # синий
        bg_label.config(image=bg3)
        bg_label.image = bg3

        exitadapter_button.config(image=exitbuttonbg3)
        rebootbutton_button.config(image=rebootbuttonbg3)

        print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTGREEN_EX}BackGround изменен на 'bg3.jpg'{Fore.RESET} | {Style.BRIGHT}{Fore.LIGHTBLUE_EX}BLUE ")

        settings_frame.config(bg="#036576")
        entry_frame.config(bg="#0A3B59")
        menu_frame.config(bg="#131A2E")
        menu_frame2.config(bg="#142342")
        about_frame.config(bg="#151F3A")
        currency_frame.config(bg="#0A3B59")
        faker_frame.config(bg="#0A3B59")
        output_label.config(bg="#0A3B59")
        exitadapter_button.config(bg="#142342", activebackground="#142342")
        rebootbutton_button.config(bg="#142342", activebackground="#142342")

        for frame in (menu_frame, entry_frame, about_frame, faker_frame, currency_frame, output_label):
            for widget in frame.winfo_children():
                try:
                    if isinstance(widget, tk.Button):
                            widget.config(
                                bg="#006597",
                                fg="white",
                                activebackground="#00689C",
                                activeforeground = "white"
                            )

                            about_btn.config(bg="#003D5C", activebackground="#00689C")
                            settings_button.config(bg="#003D5C", activebackground="#00689C")
                            btn1.config(bg="#003D5C", activebackground="#00689C")
                            btn2.config(bg="#003D5C", activebackground="#00689C")
                            btn3.config(bg="#003D5C", activebackground="#00689C")
                            btn4.config(bg="#003D5C", activebackground="#00689C")

                            confirm_button.config(fg="#00CF00", activeforeground="#00CF00")

                            fakerback_button.config(fg="red", activeforeground="red")
                            currencyback_button.config(fg="red", activeforeground="red")
                            aboutback_button.config(fg="red", activeforeground="red")
                            back_button.config(fg="red", activeforeground="red")

                except Exception as a:
                    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка background: {a}")


        bg_state = 3


    elif bg_state == 3:
        # красный
        bg_label.config(image=bg4)
        bg_label.image = bg4

        exitadapter_button.config(image=exitbuttonbg4)
        rebootbutton_button.config(image=rebootbuttonbg4)

        print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTGREEN_EX}BackGround изменен на 'bg4.jpg'{Fore.RESET} | {Style.BRIGHT}{Fore.LIGHTRED_EX}RED")

        settings_frame.config(bg="#D60000")
        menu_frame.config(bg="#940000")
        menu_frame2.config(bg="#940000")
        entry_frame.config(bg="#800404")
        about_frame.config(bg="#8C0303")
        faker_frame.config(bg="#8C0303")
        currency_frame.config(bg="#D30802")
        output_label.config(bg="#710000")
        exitadapter_button.config(bg="#940000", activebackground="#940000")
        rebootbutton_button.config(bg="#940000", activebackground="#940000")

        for frame in (menu_frame, entry_frame, about_frame, faker_frame, currency_frame, output_label):
            for widget in frame.winfo_children():
                try:
                    if isinstance(widget, tk.Button):
                            widget.config(
                                bg="#8B0000",
                                fg="white",
                                activebackground="#B40000",
                                activeforeground = "white"
                            )
                            about_btn.config(bg="#570000", activebackground="#B40000")
                            settings_button.config(bg="#570000", activebackground="#B40000")
                            btn1.config(bg="#570000", activebackground="#B40000")
                            btn2.config(bg="#570000", activebackground="#B40000")
                            btn3.config(bg="#570000", activebackground="#B40000")
                            btn4.config(bg="#570000", activebackground="#B40000")

                            confirm_button.config(fg="#00CF00", activeforeground="#00CF00")

                            fakerback_button.config(fg="red", activeforeground="red")
                            currencyback_button.config(fg="red", activeforeground="red")
                            aboutback_button.config(fg="red", activeforeground="red")
                            back_button.config(fg="red", activeforeground="red")


                except Exception as a:
                    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка background: {a}")

        bg_state = 4


    elif bg_state == 4:
        # фиолетовый
        bg_label.config(image=bg5)
        bg_label.image = bg5

        exitadapter_button.config(image=exitbuttonbg5)
        rebootbutton_button.config(image=rebootbuttonbg5)

        print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTGREEN_EX}BackGround изменен на 'bg5.jpg'{Fore.RESET} | {Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}MAGENTA")

        settings_frame.config(bg="#43087E")
        menu_frame.config(bg="#2D0453")
        menu_frame2.config(bg="#2D0453")
        entry_frame.config(bg="#410778")
        about_frame.config(bg="#2D0453")
        currency_frame.config(bg="#2D0453")
        faker_frame.config(bg="#2D0453")
        output_label.config(bg="#410778")
        exitadapter_button.config(bg="#2D0453", activebackground="#2D0453")
        rebootbutton_button.config(bg="#2D0453", activebackground="#2D0453")

        for frame in (menu_frame, entry_frame, about_frame, faker_frame, currency_frame, output_label):
            for widget in frame.winfo_children():
                try:
                    if isinstance(widget, tk.Button):
                            widget.config(
                                bg="#370051",
                                fg="white",
                                activebackground="#640096",
                                activeforeground = "white"
                            )
                            about_btn.config(bg="#29003E", activebackground="#640096")
                            settings_button.config(bg="#29003E", activebackground="#640096")
                            btn1.config(bg="#29003E", activebackground="#640096")
                            btn2.config(bg="#29003E", activebackground="#640096")
                            btn3.config(bg="#29003E", activebackground="#640096")
                            btn4.config(bg="#29003E", activebackground="#640096")

                            confirm_button.config(fg="#00CF00", activeforeground="#00CF00")

                            fakerback_button.config(fg="red", activeforeground="red")
                            currencyback_button.config(fg="red", activeforeground="red")
                            aboutback_button.config(fg="red", activeforeground="red")
                            back_button.config(fg="red", activeforeground="red")


                except Exception as a:
                    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка background: {a}")

        bg_state = 5


    else:
        bg_label.config(image=bg1)
        bg_label.image = bg1

        exitadapter_button.config(image=exitbuttonbg1)
        rebootbutton_button.config(image=rebootbuttonbg1)

        print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTGREEN_EX}BackGround изменен на 'bg2.jpg'{Fore.RESET} | {Style.BRIGHT}{Fore.LIGHTBLACK_EX}BLACK")

        for frame in (menu_frame, menu_frame2, settings_frame, entry_frame, about_frame, currency_frame, faker_frame, output_label):
            frame.config(bg="black")
            frame.lift()

            for widget in frame.winfo_children():
                try:
                    if isinstance(widget, tk.Button):
                            widget.config(
                                bg="#262626",
                                fg="white",
                                activebackground="#444444",
                                activeforeground = "white"
                            )
                            about_btn.config(bg="#202020", activebackground="#444444")
                            settings_button.config(bg="#202020", activebackground="#444444")
                            btn1.config(activeforeground="#00CF00", fg="#00CF00")
                            exitadapter_button.config(bg="black", activebackground="black")
                            rebootbutton_button.config(bg="black", activebackground="black")

                            confirm_button.config(fg="#00CF00", activeforeground="#00CF00")

                            fakerback_button.config(fg="red", activeforeground="red")
                            currencyback_button.config(fg="red", activeforeground="red")
                            aboutback_button.config(fg="red", activeforeground="red")
                            back_button.config(fg="red", activeforeground="red")

                except Exception as a:
                    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка background: {a}")

        bg_state = 1


# главное меню
menu_frame = tk.Frame(root, bg="black")
menu_frame.pack(pady=20)

# главное меню №2
menu_frame2 = tk.Frame(root, bg="black")
menu_frame2.pack(pady=20)

# settigs frame
settings_frame = tk.Frame(root, bg="black")

# about frame
about_frame = tk.Frame(root, bg="black")

# currency frame
currency_frame = tk.Frame(root, bg="black")

#faker frame
faker_frame = tk.Frame(root, bg="black")

# кнопки
button1 = tk.Button(menu_frame, text="Number", bg="#262626", fg="white", width=10, activeforeground="white", activebackground="#444444", command=select_api1)
button1.pack(side="left", padx=5)

button2 = tk.Button(menu_frame, text="IP", bg="#262626", fg="white", width=10, activeforeground="white", activebackground="#444444", command=select_api2)
button2.pack(side="left", padx=5)

button3 = tk.Button(menu_frame, text="Lat/Lon", bg="#262626", fg="white", width=10, activeforeground="white", activebackground="#444444", command=select_api3)
button3.pack(side="left", padx=5)

button4 = tk.Button(menu_frame, text="QRcode", bg="#262626", fg="white", width=10, activeforeground="white", activebackground="#444444", command=select_qrcode)
button4.pack(side="left", padx=5)

button5 = tk.Button(menu_frame, text="Troll", bg="#262626", fg="white", width=10, activeforeground="white", activebackground="#444444", command=trol)
button5.pack(side="left", padx=5)

button6 = tk.Button(menu_frame, text="Currency", bg="#262626", fg="white", width=10, activeforeground="white", activebackground="#444444", command=select_currency)
button6.pack(side="left", padx=5)

button7 = tk.Button(menu_frame, text="GPT CHC", bg="#262626", fg="white", width=10, activeforeground="white", activebackground="#444444", command=select_gptchc)
button7.pack(side="left", padx=5)

button8 = tk.Button(menu_frame, text="Faker", bg="#262626", fg="white", width=10, activeforeground="white", activebackground="#444444", command=select_faker)
button8.pack(side="left", padx=5)

about_btn = tk.Button(menu_frame2, text="Info", bg="#202020", fg="white", activebackground="#444444", activeforeground="white", width=5, command=select_about)
about_btn.pack(side="left", padx=5)

settings_button = tk.Button(menu_frame2, text="Settings", command=toggle_settings, bg="#202020", fg="white", activebackground="#444444", activeforeground="white", width=10)
settings_button.pack(side="left", padx=5)

btn1 = tk.Button(settings_frame, text="fullscreen", bg="#202020", fg="#00CF00", activebackground="#202020", activeforeground="#00CF00", width=10, command=toggle_fullscreen)
btn1.pack(pady=2)

btn2 = tk.Button(settings_frame, text="background", bg="#202020", fg="white", activebackground="#202020", activeforeground="white", width=10, command=change_background)
btn2.pack(pady=3)

btn3 = tk.Button(settings_frame, text="folder", bg="#202020", fg="white", activebackground="#202020", activeforeground="white", width=10, command=open_folder)
btn3.pack(pady=3)

btn4 = tk.Button(settings_frame, text="console", bg="#202020", fg="white", activebackground="#202020", activeforeground="white", width=10, command=lambda: consoleadapter("consoleopened"))
btn4.pack(pady=3)

btn5 = tk.Button(settings_frame, text="test", bg="#202020", fg="white", activebackground="#202020", activeforeground="white", width=10, command=select_custom2)
btn5.pack(pady=3)

exitadapter_button = tk.Button(menu_frame2, image=exitbuttonbg1, bg="black", activebackground="black", borderwidth=0, command=exitt)
exitadapter_button.pack(side="right", padx=5)

rebootbutton_button = tk.Button(menu_frame2, image=rebootbuttonbg1, bg="black", activebackground="black", borderwidth=0, command=menu_reboot)
rebootbutton_button.pack(side="right", padx=5)

# ввод
entry_frame = tk.Frame(root, bg="black")
entry = tk.Entry(entry_frame)
entry.pack(pady=5)
confirm_button = tk.Button(entry_frame, text="OK", bg="#262626", fg="#00CF00", activebackground="#444444", width=5, activeforeground="#00CF00")
confirm_button.pack(pady=5)
back_button = tk.Button(entry_frame, text="Back", bg="#262626", fg="red", activebackground="#444444", width=5, activeforeground="red", command=go_back_from_entry)
back_button.pack(pady=1)

#back about & info
abot_button = tk.Button(about_frame, text="about project", bg="#262626", fg="white", activebackground="#444444", width=10, command=about_project)
abot_button.pack(pady=5)
aboutconsole_button = tk.Button(about_frame, text="about console", bg="#262626", fg="white", activebackground="#444444", width=10, command=consoleabout)
aboutconsole_button.pack(pady=5)
aboutback_button = tk.Button(about_frame, text="back", bg="#262626", fg="red", activebackground="#444444", activeforeground="red", command=go_back)
aboutback_button.pack(pady=5)

#currency
btc_button = tk.Button(currency_frame, text="BTC", bg="#262626", fg="white", activebackground="#444444", width=5, command=select_btc)
btc_button.pack(pady=3)
ton_button = tk.Button(currency_frame, text="TON", bg="#262626", fg="white", activebackground="#444444", width=5, command=select_ton)
ton_button.pack(pady=3)
currencyback_button = tk.Button(currency_frame, text="back", bg="#262626", fg="red", activebackground="#444444", activeforeground="red", command=go_back)
currencyback_button.pack(pady=1)

#faker
rubtn = tk.Button(faker_frame, text="Russian", bg="#262626", fg="white", activebackground="#444444", width=8, command=fakerru)
rubtn.pack(pady=3)
engbtn = tk.Button(faker_frame, text="English", bg="#262626", fg="white", activebackground="#444444", width=8, command=fakereng)
engbtn.pack(pady=3)
kzbtn = tk.Button(faker_frame, text="Spanish", bg="#262626", fg="white", activebackground="#444444", width=8, command=fakeres)
kzbtn.pack(pady=3)
jpbtn = tk.Button(faker_frame, text="Japanese", bg="#262626", fg="white", activebackground="#444444", width=8, command=fakerjp)
jpbtn.pack(pady=3)
fakerback_button = tk.Button(faker_frame, text="back", bg="#262626", fg="red", activebackground="#444444", activeforeground="red", command=go_back)
fakerback_button.pack(pady=1)



output_label = tk.Label(root, bg="black", fg="#FF0000")

threading.Thread(target=console_thread, daemon=True).start()
root.after(100, check_queue)

root.mainloop()
