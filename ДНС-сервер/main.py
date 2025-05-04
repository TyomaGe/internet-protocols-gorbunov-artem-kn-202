import os
from DNSServer import DNSServer
import threading


def user_input_handler(dns_server):
    while True:
        cmd = input().strip().lower()
        # Чтобы корректно все закрылось и сохранилось, на консоль вводим exit
        if cmd == 'exit':
            print("Shutting down the DNS server...")
            dns_server.cache.save_cache()
            os._exit(0)


if __name__ == "__main__":
    dns_server = DNSServer('8.8.8.8')
    input_thread = threading.Thread(target=user_input_handler, args=(dns_server,), daemon=True)
    input_thread.start()
    dns_server.run()
