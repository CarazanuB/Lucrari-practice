import requests

# Listele predefinite pentru examen
SITES = [
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "http://this-site-does-not-exist.invalid"
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options"
]

# Partea 1: Funcții ajutătoare
def build_url(host, path):
    if path.startswith("/"):
        return f"https://{host}{path}"
    return f"https://{host}/{path}"

def is_https(url):
    return url.startswith("https://")

# Partea 2: Trimiterea unei cereri
def show_response(url):
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type', 'unknown')}")

# Partea 3: Un verificator reutilizabil
def check_site(url):
    try:
        response = requests.get(url, timeout=5)
        server = response.headers.get("Server", "unknown")
        content_type = response.headers.get("Content-Type", "").split(";")[0]
        return {
            "status": response.status_code,
            "content_type": content_type,
            "length": len(response.content),
            "server": server
        }
    except requests.RequestException as e:
        return {"status": None, "error": str(e)[:50]}

# Partea 4: Verificarea mai multor site-uri
def scan_sites():
    results = []
    success_count = 0
    fail_count = 0

    for site in SITES:
        res = check_site(site)
        if res["status"] == 200:
            success_count += 1
            results.append({"url": site, "length": res["length"]})
        else:
            fail_count += 1

    results.sort(key=lambda x: x["length"], reverse=True)

    for item in results:
        print(f"{item['url']} -> 200, {item['length']} octeți")

    print(f"Reuşite: {success_count} Eşuate: {fail_count}")

# Partea 5: Audit de securitate
def check_headers(url):
    try:
        response = requests.get(url, timeout=5)
        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        
        present = []
        missing = []

        for header in SECURITY_HEADERS:
            if header.lower() in headers_lower:
                present.append(header)
            else:
                missing.append(header)

        score = int((len(present) / len(SECURITY_HEADERS)) * 100)

        return {
            "present": present,
            "missing": missing,
            "score": score
        }
    except requests.RequestException as e:
        return {"status": None, "error": str(e)[:50]}

# Partea 6: Încercări repetate
def retry_check(url, attempts=3):
    last_status = None
    last_error = None

    for current_attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code
            
            if last_status < 500:
                return {"status": last_status, "attempts": current_attempt}
            
        except requests.RequestException as e:
            last_status = None
            last_error = str(e)[:50]

    result = {"status": last_status, "attempts": attempts}
    if last_error:
        result["error"] = last_error
    return result