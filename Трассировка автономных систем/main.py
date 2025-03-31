import sys
from tracer import trace
from check_ip import validate_ip
from make_table import print_trace_results

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("\nИспользование: python main.py <хост>")
        print("Пример:\n"
              "python main.py google.com\n"
              "python main.py 8.8.8.8\n")
        sys.exit(1)

    host = sys.argv[1]
    validate_ip(host)
    ips = trace(host)

    print("\nРезультаты трассировки до", host)
    print_trace_results(ips)
