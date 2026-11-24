import os
from arsenal.privesc.enum import GTFO, citeste_linii, nume


def cai(fisier):
    return set(citeste_linii(fisier))


def main():
    baza_path = os.path.join(os.path.dirname(__file__), "start", "baza_suid.txt")
    acum_path = os.path.join(os.path.dirname(__file__), "start", "suid.txt")

    baza = cai(baza_path)
    acum = cai(acum_path)
    print("baza:", len(baza), " acum:", len(acum))

    noi = acum - baza
    print(len(noi), "SUID noi fata de sistemul curat")
    for c in sorted(noi):
        print(" ", c)

    risc = {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in noi}
    periculoase = [c for c in sorted(noi) if nume(c) in GTFO]
    print("risc:", risc)
    print("periculoase NOI:", periculoase)


if __name__ == "__main__":
    main()