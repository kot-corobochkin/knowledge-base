import requests
import time
import json
import os
import re
import sys
import platform

if platform.system() == "Windows":
    import winsound


URL = "https://ais.usvisa-info.com/ru-kz/niv/schedule/73133663/appointment/days/134.json?appointments[expedite]=false"

CHECK_INTERVAL = 30


string = "curl 'https://ais.usvisa-info.com/ru-kz/niv/schedule/73133663/appointment/days/134.json?appointments[expedite]=false' \
  --globoff \
  --compressed \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0' \
  -H 'Accept: application/json, text/javascript, */*; q=0.01' \
  -H 'Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7' \
  -H 'Accept-Encoding: gzip, deflate, br, zstd' \
  -H 'Referer: https://ais.usvisa-info.com/ru-kz/niv/schedule/73133663/appointment?confirmed_limit_message=1&commit=Continue' \
  -H 'X-CSRF-Token: WqCHVDFSy7nTd5zEVoS/l7ug7rICvQDXVAnHRyAwUhCo/pRSuIR1OsnqkEJWLZ8YmjYKyRB0STFqtTX5IjCCpg==' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'Connection: keep-alive' \
  -H 'Cookie: _yatri_session=vw7kV06IBQMrJgR%2BJxhphPp8%2FElwxdXwZHvjj6qWn3UJslFIIJDbM%2Fuz7dyASih9ZGUqV6SKEhNyTnkElFjM%2Fgkcu4mc90QvscbreYsb7w4gry0pMhe2kbxGLUUTg9WcIcfSjmEeaZNeie9%2Brq20u47RD%2BX2FqatFNZwJMgAGz3ItsczrDYRVyRiJywruTJ2kayUdLJELPrdS1POu%2F6aVs%2BLQ%2Ffk9dFO5JRM3YD7gbZvwQs3lc7kq2XP9mTOniew98q%2Bu8XZWtBwoYJ5tKMaU4pvdutR%2B4c%2Bi%2FVSvNuY1rVY9AoBvlPqOY2soUzJUeAJxDQoU9sGieP67SvfRLJke%2F86ymUWpf%2BoyU7fNZIXR7W2z%2B8dNjC%2BAfW5wKlpG%2BkZFX7fz3orXeBGTe4p7ZXrTwJ6PG98kWEXQmGjP%2FDjr4Rd0dYvKFnZ5KBwz3rmIYVfttmTgh6XqGF4mM3%2F9JKxUoI8tUTw8EA3mIuINIoxqJQqJ61odWcTsId2nbdwOMuTiXly7mOFGxSNFC%2BKw2jpnojRAjIbCwhf0HRTzn8VErkkWVb2ncc2nsbY5Ul40LoPy3p4QlN%2BU4AVYAwwfnxOy5yOhP6y7JqsAQOXJBob8Xkf3q3q8ZPLPBOm98pesFdideuhbBbC2hqXLH8FIwru29EtLxT%2FYK6LvsuHRcLpkPe%2B9SgL6bHTTRJRm%2BiBjBOsAmgHpEhTH%2BRG1EypR3alGPhtevfRf%2FsISuhIfE1TtSWo%2BFNnizr77OJR0N65rjnDyTgFDrk4HhxwJCpMP%2FqBl7HugVXfnOtXlUBfnV0lMIvLUndBwDXKYV7P1Rew7%2F5gviY%3D--LlhxnCOLtQzsWWHm--EqVTLy1sIAPxk7G%2FxoKkdA%3D%3D; _ga=GA1.2.1690605039.1772519936; _gid=GA1.2.1615957362.1772519936; _ga_CSLL4ZEK4L=GS2.1.s1772627373$o12$g1$t1772627386$j47$l0$h0; _ga_W1JNKHTW0Y=GS2.2.s1772627373$o12$g1$t1772627395$j38$l0$h0; _gat=1' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin'"



def curl_to_headers(curl_string: str) -> dict:
    """
    Извлекает все -H 'Header: value' из curl строки
    и превращает в словарь Python
    """
    matches = re.findall(r"-H\s+'([^']+)'", curl_string)

    headers = {}

    for m in matches:
        if ":" not in m:
            continue
        key, value = m.split(":", 1)
        headers[key.strip()] = value.strip()

    return headers


def beep():
    time.sleep(1)
    if platform.system() == "Windows":
        winsound.Beep(1000, 500)  # частота, длительность
    else:
        print("\a")


def beep2():
    time.sleep(1)
    if platform.system() == "Windows":
        winsound.Beep(400, 700)
    else:
        print("\a")


def fetch_dates():
    HEADERS = curl_to_headers(string)
    r = requests.get(URL, headers=HEADERS)
    r.raise_for_status()
    data = r.json()
    return sorted([d["date"] for d in data])


def main():
    prev = None

    while True:
        try:
            dates = fetch_dates()
            print("Current dates:", dates)

            if prev and dates != prev:
                print("\n⚠️ ДАТЫ ИЗМЕНИЛИСЬ!")
                print("Было:", prev)
                print("Стало:", dates)

                for _ in range(5):
                    beep()

            prev = dates

        except Exception as e:
            print("Ошибка:", e)

            for _ in range(4):
                beep2()

            break

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()