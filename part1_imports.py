import requests
import urllib.request
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

print("--- Exercițiul 1 ---")
print("Versiune requests:", requests.__version__)

print("\n--- Exercițiul 2 ---")
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Cod de stare (stil 1):", response.status_code)

from requests import get
response_alt = get(BASE_URL, timeout=TIMEOUT)
print("Cod de stare (stil 2):", response_alt.status_code)

print("\n--- Exercițiul 3 ---")
import requests as rq
response_rq = rq.get(BASE_URL, timeout=TIMEOUT)
print("Cod de stare cu alias:", response_rq.status_code)

print("\n--- Exercițiul 4 ---")
req = urllib.request.Request(
    BASE_URL, 
    headers={"User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(req) as u_resp:
    print("Status urllib:", u_resp.status)
    body_snippet = u_resp.read(200).decode("utf-8")
    print("Primele 200 caractere:", body_snippet)
print("\n--- Exercițiul 5 ---")
 #print(dir(requests))

print("\n--- Exercițiul 6 ---")
response_doc = requests.get(BASE_URL, timeout=TIMEOUT)
print("Cerere cu timeout reușită:", response_doc.status_code)

print("\n--- Exercițiul 7 ---")
start_time = time.perf_counter()
response_timed = requests.get(BASE_URL, timeout=TIMEOUT)
end_time = time.perf_counter()
print("Timp măsurat manual (secunde):", end_time - start_time)
print("Timp raportat de response.elapsed:", response_timed.elapsed.total_seconds())

print("\n--- Exercițiul 8 ---")
try:
    import bs4
    print("Modulul bs4 este instalat.")
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")