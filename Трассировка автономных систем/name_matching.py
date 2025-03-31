import socket


def get_ip(host: str) -> str | None:
    try:
        ip = socket.gethostbyname(host)
        return ip
    except (socket.gaierror, socket.herror):
        return None
