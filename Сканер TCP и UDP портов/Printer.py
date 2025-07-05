class Printer:
    def print_opened_ports(self, ip, ports):
        if not ports:
            print(f"\n\033[91mNo open ports found\033[0m\n")
            return
        print(f"\n\033[96mOpened ports for {ip}:\033[0m")
        for port in ports:
            print(port)
        else:
            print()

    def print_protocols(self, ip, protocols):
        if not protocols:
            print(f"\n\033[91mNo open ports found\033[0m\n")
            return
        print(f"\n\033[96mOpened ports and relevant protocols for {ip}:\033[0m")
        for port, protocol in protocols.items():
            print(f"Port {port}  ->  {protocol}")
        else:
            print()