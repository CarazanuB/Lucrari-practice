import argparse
import base64
import hashlib
import json
import re
from urllib.parse import unquote


def incalzire():
    s = "Salut"
    b = s.encode()
    hex_str = b.hex()
    reconstruit = bytes.fromhex(hex_str)


def ghici_strat(s):
    if "%" in s and re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"
    if len(s) % 2 == 0 and re.fullmatch(r"[0-9a-fA-F]+", s):
        return "hex"
    if re.fullmatch(r"[A-Za-z0-9+/=]+", s):
        return "base64"
    return "necunoscut"


def desfa(s):
    strat = ghici_strat(s)
    try:
        if strat == "base64":
            padding = len(s) % 4
            if padding:
                s += "=" * (4 - padding)
            return strat, base64.b64decode(s)
        elif strat == "hex":
            return strat, bytes.fromhex(s)
        elif strat == "url":
            return strat, unquote(s).encode()
    except Exception:
        pass
    return "necunoscut", s.encode()


def citibil(b):
    if not b:
        return False
    return all(32 <= c < 127 for c in b)


def decodare_multipla(val):
    for _ in range(8):
        strat, b = desfa(val)
        if citibil(b):
            rezultat_text = b.decode("utf-8", errors="ignore")
            return strat, b
        try:
            val = b.decode("utf-8")
        except UnicodeDecodeError:
            break
    return "necunoscut", val.encode()


def sparge_xor(cale_fisier="probe/xor.bin"):
    try:
        date = open(cale_fisier, "rb").read()
    except FileNotFoundError:
        return None, None

    for k in range(256):
        clar = bytes(b ^ k for b in date)
        if citibil(clar):
            text_clar = clar.decode("utf-8", errors="ignore")
            return k, text_clar
    return None, None


def sparge_hash(cale_hashuri="probe/hashuri.txt", cale_wordlist="probe/wordlist.txt"):
    try:
        tinta = open(cale_hashuri).readline().strip()
    except FileNotFoundError:
        return None

    lungime = len(tinta)

    try:
        wordlist = open(cale_wordlist, encoding="latin1")
    except FileNotFoundError:
        return None

    for cuv in wordlist:
        cuv = cuv.strip()
        if lungime == 32:
            h = hashlib.md5(cuv.encode()).hexdigest()
        elif lungime == 40:
            h = hashlib.sha1(cuv.encode()).hexdigest()
        elif lungime == 64:
            h = hashlib.sha256(cuv.encode()).hexdigest()
        else:
            break

        if h == tinta:
            return cuv
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("intrare", nargs="?", default="NTM1OTU3NTk=")
    parser.add_argument("--fisier", action="store_true")
    args = parser.parse_args()

    if args.fisier:
        try:
            with open(args.intrare, "rb") as f:
                continut_binar = f.read()
            val_intrare = continut_binar.decode("utf-8", errors="ignore").strip()
        except Exception:
            val_intrare = args.intrare
    else:
        val_intrare = args.intrare

    strat, rezultat_b = desfa(val_intrare)
    rezultat_str = rezultat_b.decode("utf-8", errors="ignore")

    fisa = {
        "strat": strat,
        "rezultat": rezultat_str
    }
    with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f_json:
        json.dump(fisa, f_json, indent=4)