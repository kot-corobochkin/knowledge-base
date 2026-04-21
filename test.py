
import requests

s = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://opendata.fssp.gov.ru/"
}

r = s.get("https://opendata.fssp.gov.ru/api/route?hash==eyJwYXRoIjoiLzc3MDk1NzY5MjktaXBsZWdhbGxpc3QifQ~~", headers=headers)
print(r.json())