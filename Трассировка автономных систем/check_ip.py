import ipaddress
import sys
import re


def validate_ip(ip: str) -> None:
    if not re.match(r"^\d{1,3}\.", ip):
        return

    try:
        ipaddress.IPv4Address(ip)
    except ipaddress.AddressValueError:
        print(f"Ошибка: '{ip}' не является валидным IPv4 адресом")
        sys.exit(1)
