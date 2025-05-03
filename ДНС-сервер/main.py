from DNSServer import DNSServer


if __name__ == "__main__":
    dns_server = DNSServer('8.8.8.8')
    dns_server.run()
