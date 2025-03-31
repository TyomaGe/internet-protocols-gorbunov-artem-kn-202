import re
import subprocess
import sys


def trace(name: str) -> list:
    ip_regex = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    print("\nОпределение маршрута . . .")

    try:
        result = subprocess.run(
            ["tracert", name],
            capture_output=True,
            text=True,
            check=True,
            timeout=180
        )

        found_ips = ip_regex.findall(result.stdout)
        return found_ips[1:]

    except subprocess.CalledProcessError as e:
        print(f"Ошибка трассировки (код {e.returncode}):")
        print(e.stderr)
        sys.exit(e.returncode)
    except subprocess.TimeoutExpired:
        print("Превышено время ожидания выполнения трассировки в 3 минуты")
        sys.exit(1)
