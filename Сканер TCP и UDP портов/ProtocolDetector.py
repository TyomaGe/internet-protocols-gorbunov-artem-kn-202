from concurrent.futures import ThreadPoolExecutor, as_completed
import socket

from dnslib import DNSRecord, DNSHeader, DNSQuestion, QTYPE


class ProtocolDetector:
    __CLOSED = "closed"
    __HTTP = "HTTP"
    __SMTP = "SMTP"
    __SNTP = "SNTP"
    __DNS = "DNS"
    __POP3 = "POP3"
    __UNKNOWN = "unknown protocol"

    def __detect_protocols(self, function, ip, lower_bound, upper_bound):
        protocols = {}
        futures = {}
        with ThreadPoolExecutor(max_workers=100) as executor:
            for port in range(lower_bound, upper_bound + 1):
                future = executor.submit(function, ip, port)
                futures[future] = port
            for future in as_completed(futures):
                port = futures[future]
                result = future.result()
                if result != self.__CLOSED and result != self.__UNKNOWN:
                    protocols[port] = result
            return protocols

    def __detect_tcp_protocol(self, ip, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1.0)
                sock.connect((ip, port))
                if self._is_http(sock):
                    return self.__HTTP
                elif self._is_smtp(sock):
                    return self.__SMTP
                elif self._is_pop3(sock):
                    return self.__POP3
                else:
                    return self.__UNKNOWN
        except socket.error:
            return self.__CLOSED

    def __detect_udp_protocol(self, ip, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(1.0)
                sock.connect((ip, port))
                if self._is_sntp(sock):
                    return self.__SNTP
                elif self._is_dns(sock, ip):
                    return self.__DNS
                else:
                    return self.__UNKNOWN
        except socket.error:
            return self.__CLOSED

    def detect_tcp_protocols(self, ip, lower_bound, upper_bound):
        return self.__detect_protocols(
            self.__detect_tcp_protocol,
            ip,
            lower_bound,
            upper_bound
        )

    def detect_udp_protocols(self, ip, lower_bound, upper_bound):
        return self.__detect_protocols(
            self.__detect_udp_protocol,
            ip,
            lower_bound,
            upper_bound
        )

    def _is_http(self, sock):
        try:
            sock.sendall(b"GET / HTTP/1.0\r\n\r\n")
            resp = sock.recv(1024)
            return resp and b"HTTP/1." in resp
        except socket.error:
            return False

    def _is_smtp(self, sock):
        try:
            banner = sock.recv(1024)
            if b"SMTP" in banner or b"220" in banner:
                return True
            sock.sendall(b"EHLO test\r\n")
            response = sock.recv(1024)
            return b"SMTP" in response or b"250" in response
        except socket.error:
            return False

    def _is_pop3(self, sock):
        try:
            banner = sock.recv(1024)
            if b"POP3" in banner or b"+OK" in banner:
                return True
            sock.sendall(b"QUIT\r\n")
            response = sock.recv(1024)
            return b"POP3" in response or b"+OK" in response
        except socket.error:
            return False

    def _is_sntp(self, sock):
        try:
            packet = b'\x1b' + 47 * b'\0'
            sock.send(packet)
            data = sock.recv(512)
            return data and len(data) == 48
        except socket.error:
            return False

    def _is_dns(self, sock, ip):
        try:
            query = DNSRecord(
                header=DNSHeader(id=0xABCD, qr=0),
                q=DNSQuestion(ip, QTYPE.A)
            )
            sock.send(query.pack())
            data = sock.recv(512)
            response = DNSRecord.parse(data)
            return response.header.qr == 1 and response.header.id == 0xABCD
        except (socket.error, socket.timeout):
            return False
        except Exception:
            return False
