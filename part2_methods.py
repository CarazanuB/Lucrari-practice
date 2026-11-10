import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

print("--- Exercițiul 9 ---")
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("status_code:", response.status_code)
print("ok:", response.ok)
print("url:", response.url)
print("encoding:", response.encoding)

print("\n--- Exercițiul 10 ---")
try:
    response.raise_for_status()
    print("Pagina principală a trecut de verificare.")
    
    bad_response = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    bad_response.raise_for_status()
except requests.HTTPError as e:
    print("Eroare HTTP prinsă cu succes:", e)

print("\n--- Exercițiul 11 ---")
for name, value in response.headers.items():
    print(f"{name}: {value}")

print("\n--- Exercițiul 12 ---")
print("Server:", response.headers.get("Server", "lipsește"))
print("Content-Type:", response.headers.get("Content-Type", "lipsește"))
print("content-type (litere mici):", response.headers.get("content-type", "lipsește"))

print("\n--- Exercițiul 13 ---")
cyber_count = response.text.lower().count("cyber")
print("De câte ori apare 'cyber':", cyber_count)

print("\n--- Exercițiul 14 ---")
html_text = response.text
start_tag = "<title>"
end_tag = "</title>"
start_idx = html_text.find(start_tag) + len(start_tag)
end_idx = html_text.find(end_tag)
title_text = html_text[start_idx:end_idx].strip()
print("Titlul extras:", title_text)

print("\n--- Exercițiul 15 ---")
lines = html_text.splitlines()
print("Număr total de linii:", len(lines))
longest_line = max(lines, key=len)
print("Lungimea celei mai lungi linii:", len(longest_line))

print("\n--- Exercițiul 16 ---")
if response.url.startswith("https://"):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")

print("\n--- Exercițiul 17 ---")
http_response = requests.get("http://cybercor.org", timeout=TIMEOUT)
for hist in http_response.history:
    print(f"Redirecționare - Status: {hist.status_code}, URL: {hist.url}")
print("URL final:", http_response.url)

print("\n--- Exercițiul 18 ---")
head_resp = requests.head(BASE_URL, timeout=TIMEOUT)
get_resp = requests.get(BASE_URL, timeout=TIMEOUT)
print("Lungime conținut HEAD:", len(head_resp.content))
print("Lungime conținut GET:", len(get_resp.content))

print("\n--- Exercițiul 19 ---")
if len(response.cookies) == 0:
    print("Niciun cookie setat")
else:
    for cookie in response.cookies:
        print(f"Cookie: {cookie.name}, Secure: {cookie.secure}")

print("\n--- Exercițiul 20 ---")
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-Student"})
echo_resp = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
print("Rezultat antet trimis în sesiune:")
print(echo_resp.json())