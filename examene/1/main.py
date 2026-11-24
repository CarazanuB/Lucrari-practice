from checker import (
    build_url, is_https, show_response, 
    check_site, scan_sites, check_headers, retry_check
)

print("=== PARTEA 1: Funcții ajutătoare ===")
print("Partea 1, build_url (fără /):", build_url("example.com", "login"))
print("Partea 1, build_url (cu /):", build_url("example.com", "/login"))
print("Partea 1, is_https (True):", is_https("https://example.com"))
print("Partea 1, is_https (False):", is_https("http://example.com"))

print("\n=== PARTEA 2: Trimiterea unei cereri ===")
print("Partea 2, show_response pentru https://example.com:")
show_response("https://example.com")

print("\n=== PARTEA 3: Un verificator reutilizabil ===")
print("Partea 3, check_site (succes):", check_site("https://example.com"))
print("Partea 3, check_site (nereușit/inexistent):", check_site("http://this-site-does-not-exist.invalid"))

print("\n=== PARTEA 4: Verificarea mai multor site-uri ===")
print("Partea 4, scan_sites:")
scan_sites()

print("\n=== PARTEA 5: Audit de securitate ===")
print("Partea 5, check_headers pentru https://example.com:", check_headers("https://example.com"))
print("Partea 5, check_headers (site inexistent):", check_headers("http://this-site-does-not-exist.invalid"))

print("\n=== PARTEA 6: Încercări repetate ===")
print("Partea 6, retry_check (200 OK):", retry_check("https://httpbin.org/status/200"))
print("Partea 6, retry_check (404 Not Found):", retry_check("https://httpbin.org/status/404"))
print("Partea 6, retry_check (500 Server Error):", retry_check("https://httpbin.org/status/500"))
print("Partea 6, retry_check (site inexistent):", retry_check("http://this-site-does-not-exist.invalid"))