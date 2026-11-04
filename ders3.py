# Ders 3: fonksiyonlar
# Aracın durumu: bir sözlük (dict). Her bilgi bir isimle (anahtar) saklanır.
arac = {
    "sicaklik": 21.0,
    "hedef": None,
    "ses": 5,
}


def set_temperature(arac, istenen):
    """Sıcaklığı ayarlar. 16-28 dışındaysa reddeder."""
    if istenen < 16 or istenen > 28:
        return f"Hata: {istenen} derece izin verilen aralıkta değil (16-28)"
    arac["sicaklik"] = istenen
    return f"Sıcaklık {istenen} dereceye ayarlandı"


def navigate_to(arac, yer):
    """Navigasyon hedefini ayarlar."""
    arac["hedef"] = yer
    return f"Rota oluşturuldu: {yer}"


def set_volume(arac, seviye):
    """Sesi ayarlar, 0-10 dışını sınıra çeker."""
    if seviye > 10:
        seviye = 10
    if seviye < 0:
        seviye = 0
    arac["ses"] = seviye
    return f"Ses {seviye} seviyesine ayarlandı"


# Deneme: fonksiyonları çağıralım
print("Başlangıç:", arac)
print(set_temperature(arac, 30))
print(set_temperature(arac, 22))
print(navigate_to(arac, "Münih Havalimanı"))
print(set_volume(arac, 15))
print("Son durum:", arac)
