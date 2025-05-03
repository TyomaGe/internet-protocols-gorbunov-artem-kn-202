import socket
from dnslib import DNSRecord, QTYPE
from DNSCache import DNSCache


class DNSServer:
    def __init__(self, remote_dns_server_ip, port=53):
        self.port = port
        self.dns_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.remote_dns_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dns_server_ip = "127.0.0.1"
        self.remote_dns_server_ip = remote_dns_server_ip
        self.cache = DNSCache()

    def run(self):
        with self.dns_server, self.remote_dns_server:
            self.dns_server.bind((self.dns_server_ip, self.port))
            while True:
                try:
                    data, addr = self.dns_server.recvfrom(512)
                    self.__handle_request(data, addr)
                except Exception as e:
                    print(f"Error: {e}")

    def __handle_request(self, data, addr):
        try:
            query = DNSRecord.parse(data)
            qname = str(query.q.qname)
            qtype = query.q.qtype

            if qtype == QTYPE.PTR and qname == "1.0.0.127.in-addr.arpa.":
                return

            cached = self.cache.get(qname, qtype)

            if cached:
                print(f"\033[92mCache hit for {qname} ({QTYPE[qtype]})\033[0m\n")
                response = self.__build_response(query, cached)
                print(response)
                print()
                self.dns_server.sendto(response.pack(), addr)
                return

            print(
                f"\033[92mCache miss for {qname} ({QTYPE[qtype]}), querying upstream...\033[0m\n")

            try:
                self.remote_dns_server.settimeout(5)
                self.remote_dns_server.sendto(data, (self.remote_dns_server_ip, self.port))
                response_data, _ = self.remote_dns_server.recvfrom(512)
                response = DNSRecord.parse(response_data)

                print(response)
                print()

                if response.rr:
                    ttl = response.rr[0].ttl
                    self.cache.put(qname, qtype, response.rr, ttl)
                self.dns_server.sendto(response_data, addr)

            except socket.timeout:
                print(f"\033[91mTimeout while querying upstream DNS for {qname}\033[0m")
            except Exception as e:
                print(f"\033[91mError querying upstream: {e}\033[0m")
        except Exception as e:
            print(f"\033[91mError handling request: {e}\033[0m")

    def __build_response(self, query, records):
        response = query.reply()
        for rr in records:
            response.add_answer(rr)
        return response
