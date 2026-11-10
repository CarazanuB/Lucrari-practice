import requests
import time

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

def fetch(url):
    return requests.get(url, timeout=TIMEOUT)

def get_status(url):
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

def fetch_with_timeout(url, timeout=10):
    return requests.get(url, timeout=timeout)

def get_title(html):
    start_tag = "<title>"
    end_tag = "</title>"
    start_idx = html.find(start_tag) + len(start_tag)
    end_idx = html.find(end_tag)
    return html[start_idx:end_idx].strip()

def get_status_typed(url: str) -> int:
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

def page_exists(url):
    try:
        response = requests.get(url, timeout=TIMEOUT)
        return response.ok
    except requests.RequestException:
        return False

def check_paths(base, paths):
    results = {}
    for p in paths:
        url = base.rstrip("/") + "/" + p.lstrip("/")
        results[p] = get_status(url)
        time.sleep(1)
    return results

def get_header(url, name, default="lipsește"):
    resp = requests.get(url, timeout=TIMEOUT)
    return resp.headers.get(name, default)

def security_headers(url):
    headers_to_check = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    resp = requests.get(url, timeout=TIMEOUT)
    return {h: h in resp.headers for h in headers_to_check}

def score_headers(results):
    passed = sum(1 for val in results.values() if val)
    total = len(results)
    return f"{passed}/{total}"

def fetch_robots(base):
    url = base.rstrip("/") + "/robots.txt"
    try:
        resp = requests.get(url, timeout=TIMEOUT)
        if resp.ok:
            return resp.text
    except requests.RequestException:
        pass
    return None

def disallowed_paths(robots_text):
    if not robots_text:
        return []
    disallowed = []
    for line in robots_text.splitlines():
        if line.strip().lower().startswith("disallow:"):
            path = line.split(":", 1)[1].strip()
            if path:
                disallowed.append(path)
    return disallowed

def response_times(*urls):
    times = {}
    for u in urls:
        start = time.perf_counter()
        requests.get(u, timeout=TIMEOUT)
        end = time.perf_counter()
        times[u] = end - start
        time.sleep(1)
    return times

def log(message, **details):
    details_str = " | ".join(f"{k}={v}" for k, v in details.items())
    if details_str:
        print(f"{message} | {details_str}")
    else:
        print(message)

if __name__ == "__main__":
    print("--- Teste Partea 3 ---")
    print("Status BASE_URL:", get_status(BASE_URL))
    print("Verificare site invalid:", page_exists("https://this-domain-does-not-exist.invalid"))
    print("Scor securitate:", score_headers(security_headers(BASE_URL)))
    log("verificat", url=BASE_URL, status=200)