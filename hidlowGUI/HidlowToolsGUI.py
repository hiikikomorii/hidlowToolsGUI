try:
    import os
    import customtkinter as ctk
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
    import ctypes
    from pynput.keyboard import Controller, Key
    from flask import Flask, jsonify
    from pathlib import Path

except ModuleNotFoundError as e:
    print(f"Модуль {e.name} не найден.\nУстановите {e.name}")


root = ctk.CTk()
init(autoreset=True)
cmd_queue = queue.Queue()
stop_flag = False
fullscreen = False
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
time1 = datetime.now().strftime("%H:%M:%S")
data1 = date.today()


_orig_blue = Fore.BLUE
_orig_lightblue_ex = Fore.LIGHTBLUE_EX
_orig_cyan = Fore.CYAN
_orig_lightcyan_ex = Fore.LIGHTCYAN_EX

print(f"{Style.BRIGHT}{Fore.BLUE}GitHub: https://github.com/hiikikomorii")

print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTCYAN_EX}Дата & время запуска: {Style.BRIGHT}{data1}, {time1}")

check_path_debug = Path(r"files\consoledebug\debugconsole.py")
if check_path_debug.exists():
    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTGREEN_EX}CMD is available")
else:
    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM] {Fore.RED}CMD is not available\n" * 10)



# настройка gui
root.configure(fg_color="black")
root.attributes('-fullscreen', True)
root.after(0, lambda:root.state('zoomed'))
root.title("HidlowTools-GUI-V2")


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

def select_notify():
    prepare_input(main_notify)

def select_about():
    prepare_about()

def select_currency():
    hide_settings()
    menu_frame.pack_forget()
    menu_frame2.pack_forget()
    currency_frame.pack(pady=10)
    currencyback_button.configure(command=go_back)

def select_faker():
    hide_settings()
    menu_frame.pack_forget()
    menu_frame2.pack_forget()
    faker_frame.pack(pady=10)
    fakerback_button.configure(command=go_back)

#prepare about
def prepare_about():
    hide_settings()
    menu_frame.pack_forget()
    menu_frame2.pack_forget()
    about_frame.pack(pady=10)
    aboutback_button.configure(command=go_back)


#prepare api
def prepare_input(api_func):
    hide_settings()
    menu_frame.pack_forget()
    menu_frame2.pack_forget()
    clear_entry_frame()
    entry_frame.pack(pady=10)
    confirm_button.configure(command=api_func)


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
        output_label.configure(text="Введите номер телефона!", text_color="red")
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

        def paste_text(_=None):
            copyable.configure(state="normal")
            copyable.event_generate("<<Paste>>")
            copyable.configure(state="normal")
            return "break"

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
        copyable.bind("<Control-v>", paste_text)
        print(f"{Fore.BLUE}{Style.BRIGHT}[NUMBER]{Style.NORMAL} {Fore.LIGHTGREEN_EX}Запрос выполнен: {user_input}")

    except Exception as er:
        output_label.configure(text=f"Ошибка API: {er}", text_color="red")
        print(f"{Fore.BLUE}{Style.BRIGHT}[NUMBER]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка API: {er}")




def api_ip():
    user_input = entry.get().strip()
    clear_entry_frame()
    output_label.pack_forget()
    if not user_input:
        output_label.configure(text="Введите ip!", text_color="red")
        output_label.pack(pady=5)
        print(f"{Fore.BLUE}{Style.BRIGHT}[IP]{Style.NORMAL} {Fore.LIGHTYELLOW_EX}IP не был введен")
        return

    try:
        copyable = tk.Text(
            entry_frame,
            width=60,
            height=23,
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
            f"Тип: {data.get('type', 'не найдено')}\n"
            f"Долгота: {data.get('latitudee', 'не найдено')}\n"
            f"Широта: {data.get('longitudee', 'не найдено')}\n"
            f"Континент: {data.get('continent', 'не найдено')}\n"
            f"Страна: {data.get('country', 'не найдено')}\n"
            f"Столица: {data.get('country_capital', 'не найдено')}\n"
            f"Регион: {data.get('region', 'не найдено')}\n"
            f"Город: {data.get('city', 'не найдено')}\n"
            f"Соседние страны: {data.get('country_neighbours', 'не найдено')}\n"
            f"Флаг: {data.get('country_flag', 'не найдено')}\n"
            f"Код телефона: {data.get('country_phone', 'не найдено')}\n"
            f"Код континента: {data.get('continent_code', 'не найдено')}\n"
            f"Код страны: {data.get('country_code', 'не найдено')}\n"
            f"Код валюты: {data.get('currency_code', 'не найдено')}\n"
            f"ASN: {data.get('asn', 'не найдено')}\n"
            f"Провайдер: {data.get('isp', 'не найдено')}\n" 
            f"Организация: {data.get('org', 'не найденo')}\n"           
            f"Часовой пояс: {data.get('timezone', 'не найдено')}\n"
            f"Название: {data.get('timezone_name', 'не найдено')}\n"
            f"Валюта: {data.get('currency', 'не найдено')}\n"
            f"Символ валюты: {data.get('currency_symbol', 'не найдено')}\n"

        )


        copyable.insert("1.0", text)
        copyable.configure(state="normal")
        print(f"{Fore.BLUE}{Style.BRIGHT}[IP]{Style.NORMAL} {Fore.LIGHTGREEN_EX}Запрос выполнен: {user_input}")

    except Exception as er:
        output_label.config(text=f"Ошибка API-IP: {er}", text_color="red")
        print(f"{Fore.BLUE}{Style.BRIGHT}[IP]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка API-IP: {er}")

def api_lat():
    user_input = entry.get().strip()
    clear_entry_frame()
    output_label.pack_forget()
    if not user_input:
        output_label.configure(text="Введите координаты (lat lon)", text_color="red")
        output_label.pack(pady=5)
        print(f"{Fore.BLUE}{Style.BRIGHT}[LatLon]{Style.NORMAL} {Fore.LIGHTYELLOW_EX}Координаты не были введены.")
        return

    try:

        parts = user_input.split()

        if len(parts) != 2:
            output_label.config(text="Введите два значения: широта и долгота через пробел", text_color="red")
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
            height=20,
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
            f"Регион: {data.get('address', {}).get('region', 'не найдено')}\n"
            f"Область: {data.get('address', {}).get('state', 'не найдено')}\n"
            f"Город: {data.get('address', {}).get('city', data.get('address', {}).get('town', 'не найдено'))}\n"
            f"Пригород: {data.get('address', {}).get('suburb', 'не найдено')}\n"           
            f"Квартал: {data.get('address', {}).get('quarter', 'не найдено')}\n"
            f"Улица: {data.get('address', {}).get('road', 'не найдено')}\n"
            f"Микрорайон: {data.get('address', {}).get('neighbourhood', 'не найдено')}\n"
            f"Достопримечательность: {data.get('address', {}).get('name', 'не найдено')}\n"
            f"Номер дома: {data.get('address', {}).get('house_number', 'не найдено')}\n\n"
            f"Код страны: {data.get('address', {}).get('country_code', 'не найдено')}\n"
            f"ID места: {data.get('place_id', 'не найдено')}\n"
            f"Тип объекта: {data.get('osm_type', 'не найдено')}\n"
            f"Класс объекта: {data.get('class', 'не найдено')}\n"
            f"Тип: {data.get('type', 'не найдено')}\n"
            f"Почтовый индекс: {data.get('address', {}).get('postcode', 'не найдено')}\n"

        )

        copyable.insert("1.0", text)
        copyable.configure(state="normal")

        print(f"{Fore.BLUE}{Style.BRIGHT}[LatLon]{Style.NORMAL} {Fore.LIGHTGREEN_EX}Запрос был выполнен: {parts}")

    except Exception as er:
        output_label.config(text=f"Ошибка API-lat: {er}", text_color="red")
        print(f"{Fore.BLUE}{Style.BRIGHT}[LatLon]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка API-lat: {er}")

def qrcodee():
    user_input = entry.get().strip()

    clear_entry_frame()

    output_label.pack_forget()
    if not user_input:
        output_label.config(text="Введите URL", text_color="red")
        output_label.pack(pady=5)
        print(f"{Fore.BLUE}{Style.BRIGHT}[QR]{Style.NORMAL} {Fore.LIGHTYELLOW_EX}Url не был введен.")
        return

    try:
        img = qrcode.make(user_input)
        img.save("qrcode.png")
        output_label.config(text="QRcode сохранен", text_color="green")
        print(f"{Fore.BLUE}{Style.BRIGHT}[QR]{Style.NORMAL} {Fore.LIGHTGREEN_EX}QR код сгенерирован и сохранён как 'qrcodde.png'")

    except Exception as er:
        output_label.config(text="error. see log", text_color="red")
        output_label.pack(pady=5)
        print(f"{Fore.BLUE}{Style.BRIGHT}[QR]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка функции qr: {er}")

def trol():
    try:
        print(f"{Fore.BLUE}{Style.BRIGHT}[TROLL]{Style.NORMAL} {Fore.LIGHTGREEN_EX}Troll was opened")
        script_dir = Path(__file__).parent / "files" / "troll"
        script_file = script_dir / "trollhidlowGUI.py"

        subprocess.Popen(
            ["cmd", "/k", sys.executable, str(script_file)],
            cwd=str(script_dir),
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    except Exception as error_troll:
        button5.config(text_color="#FF0000")
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
        copyable.configure(cursor="arrow")

    except Exception as error_ton:
        print(f"{Fore.BLUE}{Style.BRIGHT}[TON]{Style.NORMAL} {Fore.RED}TON ERROR\napi недоступно\n{error_ton}")

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
        copyable.configure(cursor="arrow")

    except Exception as error_btc:
        print(f"{Fore.BLUE}{Style.BRIGHT}[BTC]{Style.NORMAL} {Fore.RED}BTC ERROR\napi недоступно\n{error_btc}")

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
        output_label.configure(text="Введите ИмяФайла.txt", text_color="red")
        output_label.pack(pady=5)
        print(f"{Fore.BLUE}{Style.BRIGHT}[GPTCHC]{Style.NORMAL} {Fore.LIGHTYELLOW_EX}название файла не было введено.")
        return

    try:
        input_file = "conversations.json"
        chat_input_name = user_input
        output_file = "chat_export.txt"

        extract_chat(input_file, chat_input_name, output_file)

    except Exception as er:
        output_label.config(text="error. see log", text_color="red")
        print(f"{Fore.BLUE}{Style.BRIGHT}[GPTCHC]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка функции GPTCHC: {er}")


#HidlowAPI
def hidlowapi_cmd():
    try:
        print(f"{Fore.BLUE}{Style.BRIGHT}[API Server]{Style.NORMAL} {Fore.LIGHTGREEN_EX}Server was enabled")
        script_dir = Path(__file__).parent / "files" / "apiserver"
        script_file = script_dir / "hidlowAPI.py"

        subprocess.Popen(
            ["cmd", "/k", sys.executable, str(script_file)],
            cwd=str(script_dir),
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    except Exception as error_hidlowapi:
        button9.config(text_color="#FF0000")
        print(f"{Fore.BLUE}{Style.BRIGHT}[API Server]{Style.NORMAL} {Fore.RED}произошла ошибка при запуске 'HidlowAPI'\n{error_hidlowapi}")

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
    copyable.configure(cursor="arrow")

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
    copyable.configure(cursor="arrow")

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
    copyable.configure(cursor="arrow")

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
    copyable.configure(cursor="arrow")


def show_messagebox(text, title, icon):
    ctypes.windll.user32.MessageBoxW(0, text, title, icon)



def main_notify():
    notify_icons = {
        "info": 0x40,
        "warning": 0x30,
        "error": 0x10,
        "question": 0x20
    }

    parts = entry.get().split(maxsplit=2)

    if not parts:
        output_label.configure(text_color="red", text="title, icon_type, text")
        print(f"{Fore.BLUE}{Style.BRIGHT}[CTYPES]{Style.NORMAL} {Fore.YELLOW}No data has been entered")
        output_label.pack(pady=5)
        return
    if len(parts) != 3:
        output_label.configure(text_color="red", text="title, icon_type, text")
        print(f"{Fore.BLUE}{Style.BRIGHT}[CTYPES]{Style.NORMAL} {Fore.YELLOW}Less than 3 data were entered")
        output_label.pack(pady=5)
        return

    try:

        title = parts[0]
        icon_type = parts[1].lower()
        text = parts[2]

        icon_code = notify_icons.get(icon_type, 0x10)

        print(f"{Fore.BLUE}{Style.BRIGHT}[CTYPES]{Style.NORMAL} {Fore.GREEN}Notification was shown")

        threading.Thread(target=show_messagebox, args=(text, title, icon_code)).start()

    except Exception as error_ctypes:
        print(f"{Fore.BLUE}{Style.BRIGHT}[CTYPES]{Style.NORMAL} {Fore.RED}error ctype\n{error_ctypes}")
#console
def consoleadapter():
    try:
        print(f"{Fore.BLUE}{Style.BRIGHT}[CMD]{Style.NORMAL} {Fore.LIGHTGREEN_EX}cmd was opened")
        script_dir = Path(__file__).parent / "files" / "consoledebug"
        script_file = script_dir / "debugconsole.py"

        subprocess.Popen(
            ["cmd", "/k", sys.executable, str(script_file)],
            cwd=str(script_dir),
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    except Exception as error_cmd:
        btn4.config(text_color="#FF0000")
        print(f"{Fore.BLUE}{Style.BRIGHT}[CMD]{Style.NORMAL} {Fore.RED}произошла ошибка при открытии cmd\n{error_cmd}")


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
    API - маленький API сервер на Flask.
    доступные домены: /home, /home/ip=(запрос), home/phone=<запрос>
    /home/lat=<запрос1>&lon=<запрос2>\n
    Notify - создает windows-уведомление: название окна, значок, текст
    пример: [window] [error] [text in window]
    доступные значки: info, warning, error, question\n
    \n
    background имеет 5 задних фонов: белый, черный, синий, красный, фиолетовый\n
    fullscreen меняет размер окна из полноэкранного режима в 1280x720\n
    console - с помощью нее вы можете работать с консолью. команды в 'about console'\n\n
    Версия: BETA ctypes update\n
    Всего строк: 1500\n"""

    copyable.insert("1.0", text)
    copyable.bind("<Key>", lambda s: "break")
    copyable.configure(cursor="arrow")


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
    copyable.configure(cursor="arrow")

#это настройки
def toggle_settings():
    if settings_frame.winfo_ismapped():
        settings_frame.pack_forget()
    else:
        settings_frame.pack(padx=1, pady=1)

def toggle_fullscreen():
    global fullscreen
    fullscreen = not fullscreen
    root.attributes("-fullscreen", fullscreen)

    if fullscreen:
        root.attributes("-fullscreen", False)
        root.geometry("1280x720")
        btn1.configure(text_color="#CF0000")
        print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTGREEN_EX}RootGeometry '1280x720'")
    else:
        root.attributes("-fullscreen", True)
        btn1.configure(text_color="#00CF00")
        print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTGREEN_EX}RootGeometry 'fullscreen'")

def open_folder():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.startfile(current_dir)
        print(f"{Fore.BLUE}{Style.BRIGHT}[FOLDER]{Style.NORMAL} {Fore.LIGHTGREEN_EX}директория 'HidlowGUI' успешно открыта")

    except Exception as error_folder:
        btn3.configure(text_color="#FF0000")
        print(f"{Fore.BLUE}{Style.BRIGHT}[FOLDER]{Style.NORMAL} {Fore.RED}Произошла ошибка при открытии 'folder'\n{error_folder}")


def exitt():
    global stop_flag
    stop_flag = True
    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.RED}Выход из программы")
    root.destroy()

def menu_reboot():
    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.RED}restart GUI..")
    script_path = os.path.abspath(__file__)
    subprocess.Popen(
        ["cmd", "/k", sys.executable, str(script_path)],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    time.sleep(2)
    sys.exit()
    root.destroy()

#это логика кнопок
def go_back_from_entry():
    entry_frame.pack_forget()
    for widget in root.winfo_children():
        if isinstance(widget, ctk.CTkLabel):
            widget.pack_forget()
    menu_frame.pack(pady=20)
    menu_frame2.pack(pady=20)

def go_back():
    entry_frame.pack_forget()
    about_frame.pack_forget()
    currency_frame.pack_forget()
    faker_frame.pack_forget()
    for widget in root.winfo_children():
        if isinstance(widget, ctk.CTkLabel):
            widget.pack_forget()
    menu_frame.pack(pady=20)
    menu_frame2.pack(pady=20)

def hide_settings():
    if settings_frame.winfo_ismapped():
        settings_frame.pack_forget()

def clear_entry_frame():
    entry.delete(0, "end")
    for widget in entry_frame.winfo_children():
        if isinstance(widget, tk.Text):
            widget.destroy()


# переменные фона
# 1-black 2-white 3-blue 4-red 5-magenta
btn2 = None
exit_buttons = None
bg_images = None
reboot_buttons = None



try:
    image_paths = [f"assets/bg_assets/bg{i}.jpg" for i in range(1, 6)]
    bg = [Image.open(path).resize((1920, 1080)) for path in image_paths]
    bg_images = [ctk.CTkImage(light_image=img, size=(1920, 1080)) for img in bg]
    exit_buttons = [ctk.CTkImage(light_image=Image.open(f"assets/exit_assets/exitbutton{i}.png").resize((27, 27)), size=(27, 27))for i in range(1, 6)]
    reboot_buttons = [ctk.CTkImage(light_image=Image.open(f"assets/reboot_assets/rebootbutton{i}.png").resize((25, 25)), size=(25, 25)) for i in range(1, 6)]

except Exception as b:
    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка Background : {b}")
    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTRED_EX}Bg отсутствует в сборке")
    btn2.configure(text_color="red")


# label фон
bg_label = ctk.CTkLabel(root, image=bg_images[0], text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


bg_state = 1

def change_background():
    global bg_state
    global fullscreen

    if bg_state == 1:
        bg_label.configure(image=bg_images[1])

        exitadapter_button.configure(image=exit_buttons[1])
        rebootbutton_button.configure(image=reboot_buttons[1])

        root.configure(fg_color="#D4CECE")
        menu_frame2.configure(fg_color="#D4D4D4")
        settings_frame.configure(fg_color="#BDBDBD")
        exitadapter_button.configure(fg_color="#D4D4D4", hover_color="#D4D4D4", border_color="#D4D4D4")
        rebootbutton_button.configure(fg_color="#D4D4D4", hover_color="#D4D4D4", border_color="#D4D4D4")


        print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTGREEN_EX}BackGround изменен на 'bg2.jpg'{Fore.RESET} | {Style.BRIGHT}WHITE")


        for frame in (menu_frame, entry_frame, about_frame, currency_frame, faker_frame, output_label):
            frame.configure(fg_color="#D4CECE")
            for widget in frame.winfo_children():
                try:
                    if isinstance(widget, ctk.CTkButton):
                        widget.configure(
                            fg_color="#858585",
                            hover_color="#6E6E6E",
                        )
                        about_btn.configure(fg_color="#545454", hover_color="#444444")
                        settings_button.configure(fg_color="#545454", hover_color="#444444")
                        btn1.configure(fg_color="#545454", hover_color="#444444")
                        btn2.configure(fg_color="#545454", hover_color="#444444")
                        btn3.configure(fg_color="#545454", hover_color="#444444")
                        btn4.configure(fg_color="#545454", hover_color="#444444")

                        confirm_button.configure(text_color="#00CF00")

                        fakerback_button.configure(text_color="red")
                        currencyback_button.configure(text_color="red")
                        aboutback_button.configure(text_color="red")
                        back_button.configure(text_color="red")

                except Exception as a:
                    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка background: {a}")

        bg_state = 2


    elif bg_state == 2:
        # синий
        bg_label.configure(image=bg_images[2])
        bg_label.image = bg_images[2]

        exitadapter_button.configure(image=exit_buttons[2])
        rebootbutton_button.configure(image=reboot_buttons[2])

        root.configure(fg_color="#8FCCFA")
        exitadapter_button.configure(fg_color="#95D2F7", hover_color="#95D2F7", border_color="#95D2F7")
        rebootbutton_button.configure(fg_color="#95D2F7", hover_color="#95D2F7", border_color="#95D2F7")

        print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTGREEN_EX}BackGround изменен на 'bg3.jpg'{Fore.RESET} | {Style.BRIGHT}{Fore.LIGHTBLUE_EX}BLUE ")

        settings_frame.configure(fg_color="#AAD4FA")
        entry_frame.configure(fg_color="#95C7F7")
        menu_frame.configure(fg_color="#8FCCFA")
        menu_frame2.configure(fg_color="#95D2F7")
        about_frame.configure(fg_color="#89C6F5")
        currency_frame.configure(fg_color="#9ECFF8")
        faker_frame.configure(fg_color="#89C6F5")
        output_label.configure(fg_color="#9ECFF8")


        for frame in (menu_frame, entry_frame, about_frame, faker_frame, currency_frame, output_label):
            for widget in frame.winfo_children():
                try:
                    if isinstance(widget, ctk.CTkButton):
                        widget.configure(
                            fg_color="#006597",
                            hover_color="#003D5C",
                        )

                        about_btn.configure(fg_color="#003D5C", hover_color="#00689C")
                        settings_button.configure(fg_color="#003D5C", hover_color="#00689C")
                        btn1.configure(fg_color="#003D5C", hover_color="#00689C")
                        btn2.configure(fg_color="#003D5C", hover_color="#00689C")
                        btn3.configure(fg_color="#003D5C", hover_color="#00689C")
                        btn4.configure(fg_color="#003D5C", hover_color="#00689C")

                        confirm_button.configure(text_color="#00CF00")

                        fakerback_button.configure(text_color="red")
                        currencyback_button.configure(text_color="red")
                        aboutback_button.configure(text_color="red")
                        back_button.configure(text_color="red")

                except Exception as a:
                    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка background: {a}")


        bg_state = 3


    elif bg_state == 3:
        # красный
        bg_label.configure(image=bg_images[3])
        bg_label.image = bg_images[3]

        exitadapter_button.configure(image=exit_buttons[3])
        rebootbutton_button.configure(image=reboot_buttons[3])

        root.configure(fg_color="#390100")
        exitadapter_button.configure(fg_color="#3E0202", hover_color="#3E0202", border_color="#3E0202")
        rebootbutton_button.configure(fg_color="#3E0202", hover_color="#3E0202", border_color="#3E0202")

        print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTGREEN_EX}BackGround изменен на 'bg4.jpg'{Fore.RESET} | {Style.BRIGHT}{Fore.LIGHTRED_EX}RED")

        settings_frame.configure(fg_color="#440301")
        menu_frame.configure(fg_color="#390100")
        menu_frame2.configure(fg_color="#3E0202")
        entry_frame.configure(fg_color="#3C0200")
        about_frame.configure(fg_color="#3C0200")
        faker_frame.configure(fg_color="#3C0200")
        currency_frame.configure(fg_color="#3C0200")
        output_label.configure(fg_color="#3C0200")


        for frame in (menu_frame, entry_frame, about_frame, faker_frame, currency_frame, output_label):
            for widget in frame.winfo_children():
                try:
                    if isinstance(widget, ctk.CTkButton):
                        widget.configure(
                            fg_color="#7B0202",
                            hover_color="#B40000",
                        )
                        about_btn.configure(fg_color="#840302", hover_color="#B40000")
                        settings_button.configure(fg_color="#840302", hover_color="#B40000")
                        btn1.configure(fg_color="#840302", hover_color="#B40000")
                        btn2.configure(fg_color="#840302", hover_color="#B40000")
                        btn3.configure(fg_color="#840302", hover_color="#B40000")
                        btn4.configure(fg_color="#840302", hover_color="#B40000")

                        confirm_button.configure(text_color="#00CF00")

                        fakerback_button.configure(text_color="red")
                        currencyback_button.configure(text_color="red")
                        aboutback_button.configure(text_color="red")
                        back_button.configure(text_color="red")

                except Exception as a:
                    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка background: {a}")

        bg_state = 4


    elif bg_state == 4:
        # фиолетовый
        bg_label.configure(image=bg_images[4])
        bg_label.image = bg_images[4]

        exitadapter_button.configure(image=exit_buttons[4])
        rebootbutton_button.configure(image=reboot_buttons[4])

        root.configure(fg_color="#2C0D6B")
        exitadapter_button.configure(fg_color="#300B74", hover_color="#300B73", border_color="#300B74")
        rebootbutton_button.configure(fg_color="#300B74", hover_color="#300B73", border_color="#300B74")

        print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTGREEN_EX}BackGround изменен на 'bg5.jpg'{Fore.RESET} | {Style.BRIGHT}{Fore.MAGENTA}MAGENTA")

        settings_frame.configure(fg_color="#311174")
        menu_frame.configure(fg_color="#280963")
        menu_frame2.configure(fg_color="#300B74")


        for frame in (entry_frame, about_frame, currency_frame, faker_frame, output_label):
            frame.configure(fg_color="#300B72")

        for frame in (menu_frame, entry_frame, about_frame, faker_frame, currency_frame, output_label):
            for widget in frame.winfo_children():
                try:
                    if isinstance(widget, ctk.CTkButton):
                        widget.configure(
                            fg_color="#540073",
                            hover_color="#640096"
                        )

                        about_btn.configure(fg_color="#29003E", hover_color="#640096")
                        settings_button.configure(fg_color="#29003E", hover_color="#640096")
                        btn1.configure(fg_color="#29003E", hover_color="#640096")
                        btn2.configure(fg_color="#29003E", hover_color="#640096")
                        btn3.configure(fg_color="#29003E", hover_color="#640096")
                        btn4.configure(fg_color="#29003E", hover_color="#640096")

                        confirm_button.configure(text_color="#00CF00")

                        fakerback_button.configure(text_color="red")
                        currencyback_button.configure(text_color="red")
                        aboutback_button.configure(text_color="red")
                        back_button.configure(text_color="red")

                except Exception as a:
                    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка background: {a}")

        bg_state = 5

    else:
        bg_label.configure(image=bg_images[0])
        bg_label.image = bg_images[0]

        exitadapter_button.configure(image=exit_buttons[0])
        rebootbutton_button.configure(image=reboot_buttons[0])

        root.configure(fg_color="black")
        menu_frame2.configure(fg_color="black")
        exitadapter_button.configure(fg_color="black", hover_color="black", border_color="black")
        rebootbutton_button.configure(fg_color="black", hover_color="black", border_color="black")

        print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTGREEN_EX}BackGround изменен на 'bg1.jpg'{Fore.RESET} | {Style.BRIGHT}{Fore.LIGHTBLACK_EX}BLACK")

        for frame in (menu_frame, settings_frame, entry_frame, about_frame, currency_frame, faker_frame, output_label):
            frame.configure(fg_color="black")

            for widget in frame.winfo_children():
                try:
                    if isinstance(widget, ctk.CTkButton):
                        widget.configure(
                            fg_color="#262626",
                            hover_color="#444444"
                        )
                        about_btn.configure(fg_color="#202020", hover_color="#444444")
                        settings_button.configure(fg_color="#202020", hover_color="#444444")


                        confirm_button.configure(text_color="#00CF00")

                        fakerback_button.configure(text_color="red")
                        currencyback_button.configure(text_color="red")
                        aboutback_button.configure(text_color="red")
                        back_button.configure(text_color="red")

                except Exception as a:
                    print(f"{Fore.BLUE}{Style.BRIGHT}[SYSTEM]{Style.NORMAL} {Fore.LIGHTRED_EX}Ошибка background: {a}")

        bg_state = 1

    try:
        if fullscreen:
            btn1.configure(text_color="#CF0000")
        else:
            btn1.configure(text_color="#00CF00")
    except Exception as error_fg_fullscreen:
        print(f"Ошибка цвета fullscreen кнопки: {error_fg_fullscreen}")


# главное меню
menu_frame = ctk.CTkFrame(root, fg_color="black")
menu_frame.pack(pady=20)

# главное меню №2
menu_frame2 = ctk.CTkFrame(root, fg_color="black")
menu_frame2.pack(pady=15)

# settigs frame
settings_frame = ctk.CTkFrame(root, fg_color="black")

# about frame
about_frame = ctk.CTkFrame(root, fg_color="black")

# currency frame
currency_frame = ctk.CTkFrame(root, fg_color="black")

#faker frame
faker_frame = ctk.CTkFrame(root, fg_color="black")

# кнопки
button1 = ctk.CTkButton(menu_frame, text="Number", fg_color="#262626", text_color="white", width=50, corner_radius=10, hover_color="#444444", command=select_api1)
button1.pack(side="left", padx=5)

button2 = ctk.CTkButton(menu_frame, text="IP", fg_color="#262626", text_color="white", width=50, corner_radius=10, hover_color="#444444", command=select_api2)
button2.pack(side="left", padx=5)

button3 = ctk.CTkButton(menu_frame, text="Lat/Lon", fg_color="#262626", text_color="white", width=50, corner_radius=10,  hover_color="#444444", command=select_api3)
button3.pack(side="left", padx=5)

button4 = ctk.CTkButton(menu_frame, text="QRcode", fg_color="#262626", text_color="white", width=50, corner_radius=10,  hover_color="#444444", command=select_qrcode)
button4.pack(side="left", padx=5)

button5 = ctk.CTkButton(menu_frame, text="Troll", fg_color="#262626", text_color="white", width=50, corner_radius=10,  hover_color="#444444", command=trol)
button5.pack(side="left", padx=5)

button6 = ctk.CTkButton(menu_frame, text="Currency", fg_color="#262626", text_color="white", width=50, corner_radius=10,  hover_color="#444444", command=select_currency)
button6.pack(side="left", padx=5)

button7 = ctk.CTkButton(menu_frame, text="GPT CHC", fg_color="#262626", text_color="white", width=50, corner_radius=10,  hover_color="#444444", command=select_gptchc)
button7.pack(side="left", padx=5)

button8 = ctk.CTkButton(menu_frame, text="Faker", fg_color="#262626", text_color="white", width=50, corner_radius=10,  hover_color="#444444", command=select_faker)
button8.pack(side="left", padx=5)

button9 = ctk.CTkButton(menu_frame, text="API", fg_color="#262626", text_color="white", width=50, corner_radius=10,  hover_color="#444444", command=hidlowapi_cmd)
button9.pack(side="left", padx=5)

button10 = ctk.CTkButton(menu_frame, text="Notify", fg_color="#262626", text_color="white", width=50, corner_radius=10,  hover_color="#444444", command=select_notify)
button10.pack(side="left", padx=5)


about_btn = ctk.CTkButton(menu_frame2, text="Info", fg_color="#202020", text_color="white", hover_color="#444444", width=5, command=select_about)
about_btn.pack(side="left", padx=5)

settings_button = ctk.CTkButton(menu_frame2, text="Settings", fg_color="#202020", text_color="white", hover_color="#444444", width=10, corner_radius=10, command=toggle_settings)
settings_button.pack(side="left", padx=5)

btn1 = ctk.CTkButton(settings_frame, text="fullscreen", fg_color="#202020", text_color="#00CF00", hover_color="#444444", width=85, corner_radius=10, command=toggle_fullscreen)
btn1.pack(pady=2)


btn2 = ctk.CTkButton(settings_frame, text="background", fg_color="#202020", text_color="white", hover_color="#444444", width=90, corner_radius=10, command=change_background)
btn2.pack(pady=3)

btn3 = ctk.CTkButton(settings_frame, text="folder", fg_color="#202020", text_color="white", hover_color="#444444", width=90, corner_radius=10, command=open_folder)
btn3.pack(pady=3)

btn4 = ctk.CTkButton(settings_frame, text="console", fg_color="#202020", text_color="white", hover_color="#444444", width=90, corner_radius=10, command=consoleadapter)
btn4.pack(pady=3)


exitadapter_button = ctk.CTkButton(menu_frame2, text="", image=exit_buttons[0], fg_color="black", hover_color="black", corner_radius=0, border_width=2, border_color="black", width=10, command=exitt)
exitadapter_button.pack(side="right", padx=5)

rebootbutton_button = ctk.CTkButton(menu_frame2, text="", image=reboot_buttons[0], fg_color="black", hover_color="black", corner_radius=0, border_width=2, border_color="black", width=10, command=menu_reboot)
rebootbutton_button.pack(side="right", padx=5)

# ввод
entry_frame = ctk.CTkFrame(root, fg_color="black", width=200, height=30)
entry = ctk.CTkEntry(entry_frame)
entry.pack(pady=5)
confirm_button = ctk.CTkButton(entry_frame, text="OK", fg_color="#262626", text_color="#00CF00", hover_color="#444444", width=5)
confirm_button.pack(pady=5)
back_button = ctk.CTkButton(entry_frame, text="Back", fg_color="#262626", text_color="red", hover_color="#444444", width=5, command=go_back_from_entry)
back_button.pack(pady=1)

#back about & info
abot_button = ctk.CTkButton(about_frame, text="about project", fg_color="#262626", text_color="white", hover_color="#444444", width=10, command=about_project)
abot_button.pack(pady=5)
aboutconsole_button = ctk.CTkButton(about_frame, text="about console", fg_color="#262626", text_color="white", hover_color="#444444", width=10, command=consoleabout)
aboutconsole_button.pack(pady=5)
aboutback_button = ctk.CTkButton(about_frame, text="Back", fg_color="#262626", text_color="red", hover_color="#444444", width=10, command=go_back)
aboutback_button.pack(pady=5)

#currency
btc_button = ctk.CTkButton(currency_frame, text="BTC", fg_color="#262626", text_color="white", hover_color="#444444", width=5, command=select_btc)
btc_button.pack(pady=3)
ton_button = ctk.CTkButton(currency_frame, text="TON", fg_color="#262626", text_color="white", hover_color="#444444", width=5, command=select_ton)
ton_button.pack(pady=3)
currencyback_button = ctk.CTkButton(currency_frame, text="Back", fg_color="#262626", text_color="red", hover_color="#444444", width=5, command=go_back)
currencyback_button.pack(pady=1)

#faker
rubtn = ctk.CTkButton(faker_frame, text="Russian", fg_color="#262626", text_color="white", hover_color="#444444", width=8, command=fakerru)
rubtn.pack(pady=3)
engbtn = ctk.CTkButton(faker_frame, text="English", fg_color="#262626", text_color="white", hover_color="#444444", width=8, command=fakereng)
engbtn.pack(pady=3)
kzbtn = ctk.CTkButton(faker_frame, text="Spanish", fg_color="#262626", text_color="white", hover_color="#444444", width=8, command=fakeres)
kzbtn.pack(pady=3)
jpbtn = ctk.CTkButton(faker_frame, text="Japanese", fg_color="#262626", text_color="white", hover_color="#444444", width=8, command=fakerjp)
jpbtn.pack(pady=3)
fakerback_button = ctk.CTkButton(faker_frame, text="Back", fg_color="#262626", text_color="red", hover_color="#444444", width=8, command=go_back)
fakerback_button.pack(pady=1)



output_label = ctk.CTkLabel(root, fg_color="black", text_color="#FF0000")
root.mainloop()
