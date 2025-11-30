import tkinter as tk
import subprocess
import sys
import threading
import os
import platform
import time
root = tk.Tk()

try:
    import customtkinter
    import requests
    from PIL import Image, ImageTk
    import colorama
    import qrcode
    import psutil
    from phonenumbers import carrier, geocoder, timezone, parse, is_valid_number
    import phonenumbers
    from faker import Faker
    import pynput
    from flask import Flask, jsonify

    hidlow_path = "HidlowToolsGUI.py"
    subprocess.Popen(
        ["cmd", "/k", sys.executable, str(hidlow_path)],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

    sys.exit()
except ModuleNotFoundError as e:

    root.title("BOOT-LOADER-NOMODULE")
    root.attributes('-fullscreen', True)
    root.config(bg="blue")

    pybuild = platform.python_build()
    pycomp = platform.python_compiler()
    pyver = platform.python_version()


    def exit_bbt():
        root.destroy()
        sys.exit()


    text = ("""
Boottraped-GUI\n
Если вы попали сюда - значит у вас не установлен модуль который показывается на экране\n
нажмите кнопку 'Install' для того, чтобы установить этот модуль\n
Затем нажмите 'Reboot' для того, чтобы попытаться запустить HidlowToolsGUI
                   """)


    def reboot_bsod():
        script_path = os.path.abspath(__file__)
        subprocess.Popen(
            ["cmd", "/k", sys.executable, str(script_path)],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        sys.exit()
        root.destroy()



    def install_pip_cmd():
        label_ru.config(text=f"Подождите..", fg="white")
        label_ru.pack(anchor="nw", pady=5)
        label_eng.config(text=f"Wait..", fg="white")
        label_eng.pack(anchor="nw", pady=5)
        if e.name == "PIL":
            subprocess.run([sys.executable, "-m", "pip", "install", "Pillow"])
            return
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "install", e.name], capture_output=True, text=True)
            if result.returncode == 0:
                label_ru.config(text=f"pip {e.name} Установлено!", fg="#00CF00")
                label_ru.pack(anchor="nw", pady=5)
                label_eng.config(text=f"pip {e.name} it was established", fg="green")
                label_eng.pack(anchor="nw", pady=5)

            if result.returncode != 0:
                error_msg = result.stderr
                label_ru.config(text=f"Ошибка pip: {error_msg}", fg="red")
                label_ru.pack(anchor="nw", pady=5)
                label_eng.config(text=f"error pip: {error_msg}", fg="red")
                label_eng.pack(anchor="nw", pady=5)


        except Exception as error_pip_cmd:
           print(error_pip_cmd)

    def upd_pip_cmd():
        label_pipudp.config(text="wait...")
        label_pipudp.pack(anchor="sw", pady=5, padx=20)
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], capture_output=True, text=True)
            if result.returncode == 0:
                out_msg = result.stdout
                label_pipudp.config(text=f"pip successfully updated\n{out_msg}", fg="#00CF00")
                label_pipudp.pack(anchor="sw", pady=5, padx=20)
            if result.returncode != 0:
                error_msg = result.stderr
                label_pipudp.config(text=f"pip upd error: {error_msg}", fg="red")
                label_pipudp.pack(anchor="sw", pady=5, padx=20)

        except Exception as error_updpip:
            print(error_updpip)


    def thread_install_pip_cmd():
        threading.Thread(target=install_pip_cmd).start()

    def thread_upd_pip_cmd():
        threading.Thread(target=upd_pip_cmd).start()


    frame = tk.Frame(root, bg="blue")
    frame.pack(padx=20, pady=20, anchor="nw")

    info_frame = tk.Frame(root, bg="blue")
    info_frame.pack(side="right", pady=20, padx=20, anchor="se")


    label_help = tk.Label(info_frame, text=text, fg="white", bg="blue", font=("bold", 12))
    label_help.pack(pady=5)

    labelinfo = tk.Label(info_frame, text=f"version: {pyver}\ncompiler: {pycomp}\nbuild: {pybuild}", fg="white", bg="blue", font=("bold", 15))
    labelinfo.pack(pady=5)

    label_ru = tk.Label(frame, fg="white", bg="blue", font=("bold", 15), text=f"Отсутствующие модули: {e.name}", justify="left", anchor="nw")
    label_ru.pack(anchor="nw", pady=5)

    label_eng = tk.Label(frame, fg="white", bg="blue", font=("bold", 15), text=f"Missing modules: {e.name}",justify="left", anchor="nw")
    label_eng.pack(anchor="nw", pady=5)

    label_pipudp = tk.Label(root, fg="white", bg="blue", font=("bold", 15), text=f"", justify="left", anchor="sw")

    btn_exit = tk.Button(frame, text="Exit", activebackground="#0010A7", bg="blue", fg="white", command=exit_bbt, width=10)
    btn_exit.pack(side="left", padx=5, pady=5)

    btn_reboot = tk.Button(frame, text="Reboot", activebackground="#0010A7", bg="blue", fg="white", command=reboot_bsod, width=10)
    btn_reboot.pack(side="left", padx=5, pady=5)

    btn_download = tk.Button(frame, text="Install", activebackground="#0010A7", bg="blue", fg="white", command=thread_install_pip_cmd, width=10)
    btn_download.pack(side="left", padx=5, pady=5)

    btn_pip = tk.Button(frame, text="upgrade pip", activebackground="#0010A7", bg="blue", fg="white", command=thread_upd_pip_cmd, width=10)
    btn_pip.pack(side="left", padx=5, pady=5)

    root.mainloop()