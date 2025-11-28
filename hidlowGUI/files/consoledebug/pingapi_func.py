from colorama import init, Fore, Style
from phonenumbers import carrier, geocoder, timezone, parse, is_valid_number
import phonenumbers
import requests
import json, urllib.request
import sys
import random
import re
import time


init(autoreset=True)

# 55.7342 37.6129
# 51.15.84.185
# +79268471359

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

def onlypingarg():
    print(f"{Fore.LIGHTWHITE_EX}number\nip\nlat/lon\nbtc\nton\n")

def try_ping_ip():

    url = r"https://ipwhois.app/json/51.15.84.185"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    data = response.json()

    try:
        ip = data.get("ip", "не найдено")

        _ = ip

        print(f"{Style.BRIGHT}Запрос: ip API {Style.NORMAL}{Fore.RESET}|{Style.BRIGHT}{Fore.LIGHTGREEN_EX} API Доступно")

    except Exception as error_ip:
        print(f"{Fore.RED}Ошибка запроса ip API |{Style.BRIGHT} API недоступно{Style.NORMAL}\n{error_ip}")




def try_ping_ll():
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat=55.7342&lon=37.6129"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    data = response.json()

    try:
        latt = data.get("lat", "не найдено")
        lonn = data.get("lon", "не найдено")

        _ = (latt, lonn)

        print(f"{Style.BRIGHT}Запрос: lat/lon API{Style.NORMAL}{Fore.RESET} |{Style.BRIGHT}{Fore.LIGHTGREEN_EX} API Доступно")
    except Exception as error_ll:
        print(f"{Fore.RED}Ошибка запроса lat/lon API |{Style.BRIGHT} API недоступно{Style.NORMAL}\n{error_ll}")




def check_internet():
    try:
        urllib.request.urlopen('https://google.com', timeout=7)
        return True
    except urllib.error.URLError:
        return False

def send_request_ping(url, phone):
    _ = phone
    try:

        response = requests.get(url, headers=headers, timeout=10)

        time.sleep(random.uniform(2, 5))

        if response.status_code == 200:
            print(f"{Style.BRIGHT}Запрос: number API{Style.NORMAL}{Fore.RESET} |{Style.BRIGHT}{Fore.LIGHTGREEN_EX} API Доступно")
            return response.json()
        else:
            print(f"Ошибка: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ошибка при отправке запроса: {e}")
        return None



def try_ping_number(phone):
    try:
        url = f"https://htmlweb.ru/geo/api.php?json&telcod={phone}"
        data = send_request_ping(url, phone)

        if not isinstance(data, dict):
            return "[!] Произошла ошибка: данные ответа не являются словарем."

        country = data.get('country', {})
        region = data.get('region', {})
        capital = data.get('capital', {})

        if not isinstance(country, dict):
            country = {}
        if not isinstance(region, dict):
            region = {}
        if not isinstance(capital, dict):
            capital = {}

        if data.get("status_error"):
            return f"Ошибка: {data.get('error_message', 'Не удалось получить данные обратитесь к владельцу.')}"

        if data.get("limit") <= 0:
            return f"Ошибка: {data.get('error_message', f'У ВАС ИСЧЕРПАН ЛИМИТ {data.get("limit")}')}"

        country_id = country.get('id', 'Не найднено')

        parsed_phone = phonenumbers.parse(phone, country_id)

        _ = parsed_phone
        _ = region
        _ = capital
        _ = phone

        return f""""""

    except Exception as error_number:
        print(f"{Fore.RED}Ошибка запроса number API |{Style.BRIGHT} API недоступно{Style.NORMAL}\n{error_number}")


def try_ping_ton():
    url = "https://api.coinpaprika.com/v1/tickers/toncoin-the-open-network?quotes=USD,RUB"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    data = response.json()

    try:
        quo = data.get("quotes", {})
        usd = quo.get("USD", {})
        rub = quo.get("RUB", {})

        tonusd = usd.get("price", "not found")
        tonrub = rub.get("price", "not found")

        _ = tonrub
        _ = tonusd

        print(f"{Style.BRIGHT}Запрос: TON API{Style.NORMAL}{Fore.RESET} |{Style.BRIGHT}{Fore.LIGHTGREEN_EX} API Доступно")

    except Exception as error_ton:
        print(f"{Fore.RED}Ошибка запроса TON API |{Style.BRIGHT} API недоступно{Style.NORMAL}\n{error_ton}")


def try_ping_btc():
    url = "https://api.coinpaprika.com/v1/tickers/btc-bitcoin?quotes=USD,RUB"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    data = response.json()

    try:
        quo = data.get("quotes", {})
        usd = quo.get("USD", {})
        rub = quo.get("RUB", {})

        btcusd = usd.get("price", "not found")
        btcrub = rub.get("price", "not found")

        _ = btcrub
        _ = btcusd

        print(f"{Style.BRIGHT}Запрос: BTC API{Style.NORMAL}{Fore.RESET} |{Style.BRIGHT}{Fore.LIGHTGREEN_EX} API Доступно")

    except Exception as error_btc:
        print(f"{Fore.RED}Ошибка запроса BTC API |{Style.BRIGHT} API недоступно{Style.NORMAL}\n{error_btc}")

def menu():
    while True:
        user = input("> ").strip().lower()
        if user == "num":
            print("wait..")
            user_iput = "+79268471359"
            phone = re.sub(r"\D", "", user_iput)

            if check_internet():
                a = try_ping_number(phone)
                print(a)
            else:
                print(f"{Fore.RED}Отсутствует интернет-соединение!")

        elif user == "ll":
            try_ping_ll()
        elif user == "btc":
            try_ping_btc()
        elif user == "ton":
            try_ping_ton()
        elif user == "ip":
            try_ping_ip()

if __name__ == "__main__":
    menu()