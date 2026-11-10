import requests
import urllib.parse
import re
from html.parser import HTMLParser
import hashlib
import json
import socket
import ssl
import time

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

print("--- Exercițiul 35 ---")
parsed_url = urllib.parse.urlparse("https://cybercor.org/path?x=1#top")
print("scheme:", parsed_url.scheme)
print("netloc:", parsed_url.netloc)
print("path:", parsed_url.path)
print("query:", parsed_url.query)
print("fragment:", parsed_url.fragment)

print("\n--- Exercițiul 36 ---")
for link in ["/about", "contact.html", "../index.html"]:
    print(urllib.parse.urljoin(BASE_URL, link))

def extract_links(html):
    links = re.findall(r'href="([^"]+)"', html)
    return list(set(links))

def split_links(links, domain):
    internal = []
    external = []
    for l in links:
        full_url = urllib.parse.urljoin(domain, l)
        netloc = urllib.parse.urlparse(full_url).netloc
        if netloc == "" or netloc == urllib.parse.urlparse(domain).netloc:
            internal.append(l)
        else:
            external.append(l)
    return internal, external

class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
 
    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)

def page_fingerprint(url):
    resp = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(resp.content).hexdigest()

print("\n--- Exercițiul 41 ---")
resp_sample = requests.get(BASE_URL, timeout=TIMEOUT)
with open("headers.json", "w", encoding="utf-8") as f:
    json.dump(dict(resp_sample.headers), f, indent=2)

with open("headers.json", "r", encoding="utf-8") as f:
    loaded_headers = json.load(f)
    print("Antet Server încărcat din JSON:", loaded_headers.get("Server"))

def resolve(hostname):
    return socket.gethostbyname(hostname)

print("Adresa IP pentru cybercor.org:", resolve("cybercor.org"))

def cert_days_left(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expiry_time = ssl.cert_time_to_seconds(cert["notAfter"])
            return int((expiry_time - time.time()) // 86400)

print("Zile rămase până la expirarea certificatului:", cert_days_left("cybercor.org"))

if __name__ == "__main__":
    test_html = """
    <html><body>
      <img src="/logo.png" alt="Logo">
      <IMG SRC="poza.jpg">
      <img alt="imagine fără src">
      <img src="https://cdn.example.com/banner.webp" />
      <a href="/despre">Aceasta nu este o imagine</a>
    </body></html>
    """
    finder = ImageFinder()
    finder.feed(test_html)
    assert finder.images == [
        "/logo.png",
        "poza.jpg",
        "https://cdn.example.com/banner.webp",
    ], "Parserul nu a găsit exact imaginile așteptate"
    print("Testul pentru ImageFinder a trecut cu succes!")