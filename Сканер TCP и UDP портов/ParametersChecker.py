from ipaddress import IPv4Address
from Exceptions import *


class ParametersChecker:
    def correct_ip(self, ip):
        try:
            result = IPv4Address(ip)
        except:
            raise InvalidIpAddress
        return ip

    def correct_protocol(self, protocol: str):
        if protocol.lower() == "udp" or protocol.lower() == "tcp":
            return protocol
        else:
            raise InvalidProtocol

    def correct_port_range(self, lower_bound, upper_bound):
        if not isinstance(lower_bound, int):
            raise TypeError("Lower bound must be an integer")
        if not isinstance(upper_bound, int):
            raise TypeError("Upper bound must be an integer")
        if lower_bound > upper_bound:
            raise InvalidPortRange("Incorrect port range")
        if lower_bound < 1 or upper_bound < 1:
            raise ValueError("Port must be in range 1 to 65535")
        if lower_bound > 65535 or upper_bound > 65535:
            raise ValueError("Port must be in range 1 to 65535")
        return lower_bound, upper_bound
