from ParametersChecker import ParametersChecker
from ArgumentParser import ArgumentParser
from PortScanner import PortScanner
from Printer import Printer
from ProtocolDetector import ProtocolDetector
from Exceptions import *


def main():
    argument_parser = ArgumentParser()
    parameters_checker = ParametersChecker()
    protocol_detector = ProtocolDetector()
    port_scanner = PortScanner()
    printer = Printer()
    args = argument_parser.get_arguments()
    try:
        ip = parameters_checker.correct_ip(args.ip)
        protocol = parameters_checker.correct_protocol(args.protocol)
        lower_bound, upper_bound = parameters_checker.correct_port_range(
            args.lower_bound,
            args.upper_bound
        )
        mode = args.mode
        if protocol == "tcp":
            if mode == "opened":
                opened_ports = port_scanner.opened_tcp_ports(
                    ip,
                    lower_bound,
                    upper_bound
                )
                printer.print_opened_ports(ip, opened_ports)
            else:
                protocols = protocol_detector.detect_tcp_protocols(
                    ip,
                    lower_bound,
                    upper_bound
                )
                printer.print_protocols(ip, protocols)
        else:
            if mode == "opened":
                opened_ports = port_scanner.opened_udp_ports(
                    ip,
                    lower_bound,
                    upper_bound
                )
                printer.print_opened_ports(ip, opened_ports)
            else:
                protocols = protocol_detector.detect_udp_protocols(
                    ip,
                    lower_bound,
                    upper_bound
                )
                printer.print_protocols(ip, protocols)
    except exceptions as e:
        print(f"\033[91m{e}\033[0m")


if __name__ == "__main__":
    main()
