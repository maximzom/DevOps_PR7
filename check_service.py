import os
import subprocess
import sys


def check_service() -> int:
    base_url = os.getenv("BASE_URL", "http://127.0.0.1:8080")
    expected_release = os.getenv("EXPECTED_RELEASE", "devops_7-homework")
    timeout_raw = os.getenv("CHECK_TIMEOUT", "3")

    try:
        timeout = float(timeout_raw)
    except ValueError:
        print(f"[ERROR] Некоректне значення CHECK_TIMEOUT: {timeout_raw}")
        return 1

    cmd = ["curl", "-sS", "-f", base_url]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        print(
            f"[TIMEOUT] Сервіс {base_url} не відповів за {timeout} с "
            f"(перевищено час очікування)."
        )
        return 2
    except FileNotFoundError:
        print("[ERROR] Утиліту curl не знайдено у системному PATH.")
        return 1

    if result.returncode != 0:
        err_msg = result.stderr.strip() or f"curl exit code {result.returncode}"
        print(f"[FAIL] Помилка HTTP-запиту до {base_url}: {err_msg}")
        return 1

    if expected_release not in result.stdout:
        print(
            f"[FAIL] Очікуваний ідентифікатор '{expected_release}' "
            f"не знайдено у відповіді {base_url}."
        )
        return 1

    print(
        f"[OK] Сервіс {base_url} доступний та містить реліз '{expected_release}'."
    )
    return 0


if __name__ == "__main__":
    sys.exit(check_service())