from concurrent.futures import ThreadPoolExecutor, as_completed
import socket


class PortScanner:
    def __is_tcp_port_opened(self, ip, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)
                connected = sock.connect_ex((ip, port))
                return connected == 0
        except socket.timeout:
            return True
        except socket.error:
            return False

    def __is_udp_port_opened(self, ip, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(0.5)
                sock.sendto(b'\x00', (ip, port))
                try:
                    sock.recvfrom(512)
                    return True
                except socket.timeout:
                    return True
                except ConnectionResetError:
                    return False
        except socket.error:
            return False

    def __opened_ports(self, function, ip, lower_bound, upper_bound):
        with ThreadPoolExecutor(max_workers=100) as executor:
            opened_ports = []
            futures = {}
            for port in range(lower_bound, upper_bound + 1):
                future = executor.submit(function, ip, port)
                futures[future] = port
            for future in as_completed(futures):
                port = futures[future]
                if future.result():
                    opened_ports.append(port)
            return sorted(opened_ports)

    def opened_tcp_ports(self, ip, lower_bound, upper_bound):
        return self.__opened_ports(
            self.__is_tcp_port_opened,
            ip,
            lower_bound,
            upper_bound
        )

    def opened_udp_ports(self, ip, lower_bound, upper_bound):
        return self.__opened_ports(
            self.__is_udp_port_opened,
            ip,
            lower_bound,
            upper_bound
        )
