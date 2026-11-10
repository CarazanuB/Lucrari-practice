import requests
import csv
import time


URLS_TO_AUDIT = [
    "https://cybercor.org",
    "https://cybercor.org/about",
    "https://cybercor.org/contact"
]
TIMEOUT = 10

def audit_single_url(url):
    row = {}
    try:
        start_time = time.perf_counter()
        resp = requests.get(url, timeout=TIMEOUT)
        end_time = time.perf_counter()
        
        row["URL"] = url
        row["Status"] = resp.status_code
        row["Timp (s)"] = round(end_time - start_time, 4)
        row["Server"] = resp.headers.get("Server", "necunoscut")
        row["Lungime"] = len(resp.content)
        row["Securizat (HTTPS)"] = "Da" if url.startswith("https://") else "Nu"
    except requests.RequestException as e:
        row["URL"] = url
        row["Status"] = "Eroare"
        row["Timp (s)"] = 0
        row["Server"] = "N/A"
        row["Lungime"] = 0
        row["Securizat (HTTPS)"] = "N/A"
    return row

def save_multiline_csv(filename="audit_report.csv"):
    fieldnames = ["URL", "Status", "Timp (s)", "Server", "Lungime", "Securizat (HTTPS)"]
    
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()  # Scrie antetul tabelului
        
        for url in URLS_TO_AUDIT:
            print(f"Auditez: {url}...")
            data = audit_single_url(url)
            writer.writerow(data)  # Scrie fiecare rând separat
            time.sleep(1)
            
    print(f"\nTabelul CSV a fost salvat cu succes în {filename}!")

if __name__ == "__main__":
    print("--- Generare Raport CSV Multilinie ---")
    save_multiline_csv()