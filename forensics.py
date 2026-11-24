import re
from PIL import Image
from PIL.ExifTags import TAGS


def tip_real(cale):
    try:
        cap = open(cale, "rb").read(8)
        if cap.startswith(b"%PDF"):
            return "pdf"
        elif cap.startswith(b"\x89PNG"):
            return "png"
        elif cap.startswith(b"\xff\xd8"):
            return "jpeg"
        elif cap.startswith(b"PK\x03\x04"):
            return "zip/docx"
        return cap.hex()
    except FileNotFoundError:
        return "Fișier negăsit"


def extrage_strings(cale="probe/ascuns.png"):
    try:
        date = open(cale, "rb").read()
        matches = re.findall(rb"[ -~]{4,}", date)
        for m in matches[:20]:
            m.decode("utf-8", errors="ignore")
    except FileNotFoundError:
        pass


def citeste_exif(cale="probe/foto.jpg"):
    try:
        img = Image.open(cale)
        exif = img._getexif() or {}
        gps_info = {}
        for id, val in exif.items():
            nume_tag = TAGS.get(id, id)
            if nume_tag == "GPSInfo":
                gps_info = val
    except Exception:
        pass


def file_carving(cale="probe/ascuns.png", iesire="gasit.zip"):
    try:
        date = open(cale, "rb").read()
        i = date.find(b"PK\x03\x04")
        if i != -1:
            open(iesire, "wb").write(date[i:])
    except FileNotFoundError:
        pass


def ascunde_lsb(cale_sursa="probe/foto.jpg", cale_dest="stego.png", mesaj=b"FLAG{ascuns_in_pixeli}"):
    img = Image.open(cale_sursa).convert("RGB")
    px = list(img.getdata())
    
    mesaj_complet = mesaj + b"\x00"
    biti = "".join(f"{x:08b}" for x in mesaj_complet)
    
    if len(biti) > len(px) * 3:
        raise ValueError("Mesajul este prea lung!")
    
    px_nou = []
    bit_idx = 0
    for pixel in px:
        r, g, b = pixel
        canal = [r, g, b]
        for c in range(3):
            if bit_idx < len(biti):
                canal[c] = (canal[c] & ~1) | int(biti[bit_idx])
                bit_idx += 1
        px_nou.append(tuple(canal))
    
    img_noua = Image.new(img.mode, img.size)
    img_noua.putdata(px_nou)
    img_noua.save(cale_dest)


def dezvaluie_lsb(cale_stego="stego.png"):
    try:
        img = Image.open(cale_stego).convert("RGB")
        px = list(img.getdata())
        
        biti = []
        for r, g, b in px:
            biti.append(str(r & 1))
            biti.append(str(g & 1))
            biti.append(str(b & 1))
        
        octeti = []
        for i in range(0, len(biti), 8):
            octet_biti = "".join(biti[i:i+8])
            if len(octet_biti) < 8:
                break
            val_octet = int(octet_biti, 2)
            if val_octet == 0:
                break
            octeti.append(val_octet)
        
        mesaj_extras = bytes(octeti)
        return mesaj_extras
    except FileNotFoundError:
        return None


if __name__ == "__main__":
    tip_real("probe/foto.jpg")
    tip_real("probe/ascuns.png")
    extrage_strings()
    citeste_exif()
    file_carving()
    ascunde_lsb()
    dezvaluie_lsb()