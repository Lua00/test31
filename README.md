# Modern Encryptor (Python)

Python ile modern arayüze sahip basit bir şifreleme uygulaması.

- Arayüz: `customtkinter`
- Şifreleme: `cryptography` (Fernet + PBKDF2)

## Kurulum

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Çalıştırma

```bash
python app/main.py
```

## Özellikler

- Metin şifreleme/çözme (salt gömülü, kendini içeren format)
- Dosya şifreleme/çözme (`.enc` uzantısı)
- Tema: Sistem / Açık / Koyu, vurgu rengi seçimi
- PBKDF2 iteration ayarı (varsayılan 200.000)

## Notlar

- Parolanızı unutursanız veriler geri getirilemez.
- Büyük dosyalarda işlem süresi parolanın türetilmesi ve şifreleme nedeniyle uzayabilir.