#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой клиент-заглушка: спрашивает IP и порт, «подключается»,
затем пишет «Сервер работает!» и остаётся запущенным.
Корректно выводит русские символы и обычные дефисы в Windows‑консоли.
"""

import ipaddress
import os
import sys
import time

WINDOWS = os.name == "nt"
if WINDOWS:
    import msvcrt

# ---------------------- исправление кодировки Windows ---------------------- #
def _fix_windows_console_encoding() -> None:
    """Переключает консоль Windows в UTF‑8 и перенастраивает вывод."""
    if WINDOWS:
        # 65001 = UTF‑8
        os.system("chcp 65001 > nul")
        for stream in (sys.stdout, sys.stderr):
            try:
                stream.reconfigure(encoding="utf-8")
            except AttributeError:
                # reconfigure есть начиная с Python 3.7
                pass

_fix_windows_console_encoding()

# ------------------------------ безопасный ввод --------------------------- #
def _win_input(prompt: str) -> str:
    """Корректный ввод строки в Windows (символы по одному, чтобы не терять Юникод)."""
    print(prompt, end='', flush=True)
    buf = ''
    while True:
        ch = msvcrt.getwch()
        if ch in ('\r', '\n'):
            print()
            return buf.strip()
        elif ch == '\b':
            if buf:
                buf = buf[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        else:
            buf += ch
            print(ch, end='', flush=True)

def ask(prompt: str) -> str:
    try:
        return _win_input(prompt) if WINDOWS else input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(1)

# --------------------------- валидация IP и порта -------------------------- #
def get_ip() -> str:
    while True:
        ip_str = ask("\nВведите IP-адрес: ")
        try:
            ipaddress.ip_address(ip_str)
            return ip_str
        except ValueError:
            print("\nНеверный IP-адрес.")

def get_port() -> int:
    while True:
        port_str = ask("\nВведите порт (1-65535): ")
        if not port_str.isdigit():
            print("\nПорт должен быть числом.")
            continue
        port = int(port_str)
        if 1 <= port <= 65535:
            return port
        print("\nПорт вне диапазона 1-65535.")

# ---------------------------------- main ---------------------------------- #
def main() -> None:
    ip = get_ip()
    port = get_port()
    print(f"\nПодключаюсь к {ip}:{port}...")
    time.sleep(2)
    print("\nСервер работает!")
    try:
        while True:      # имитируем работу сервера
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Программа остановлена пользователем.")

if __name__ == "__main__":
    main()
