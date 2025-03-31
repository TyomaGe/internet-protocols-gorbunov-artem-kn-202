from prettytable import PrettyTable
from ip_location import is_private_ip
from find_host_info import info_seeker


def print_trace_results(ips: list) -> None:
    trace_results = fill_trace_results(ips)
    table = PrettyTable()
    table.field_names = ["№", "IP", "AS", "Страна", "Провайдер"]
    table.align = "l"

    for i, host_info in enumerate(trace_results, 1):
        table.add_row([
            i,
            host_info.get('query', 'Нет данных'),
            host_info.get('as', 'Нет данных'),
            host_info.get('country', 'Нет данных'),
            host_info.get('isp', 'Нет данных')
        ])

    print(table)


def fill_trace_results(ips: list) -> list:
    results = []
    for ip in ips:
        if is_private_ip(ip):
            results.append({
                'query': ip,
                'as': 'Приватный IP',
                'country': 'Локальная сеть',
                'isp': 'Локальная сеть'
            })
            continue
        info = info_seeker(ip)
        results.append(info)
    return results
