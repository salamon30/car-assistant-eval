# Ders 1: değişkenler
sicaklik = 21.0
hedef = None

print("Sıcaklık:", sicaklik)
print("Hedef:", hedef)

sicaklik = 23.5
hedef = "Münih Havalimanı"

print("Yeni sıcaklık:", sicaklik)
print("Yeni hedef:", hedef)

# Ders 2: koşul (if)
istenen = 30

if istenen < 16 or istenen > 28:
    print("Hata:", istenen, "derece izin verilen aralıkta değil")
else:
    sicaklik = istenen
    print("Sıcaklık ayarlandı:", sicaklik)

# Görev: sesi 10 ile sınırla
ses = 15

if ses > 10:
    print("Ses 10'a düşürüldü")
    ses = 10
else:
    print("Ses uygun")

print("Son ses:", ses)
