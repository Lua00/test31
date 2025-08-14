# 🎯 Nesne Takip Sistemi - Enemy/Friend Detector

Modern ve gelişmiş bir Python uygulaması ile mavi ve kırmızı nesneleri gerçek zamanlı olarak tespit edip takip edin. Bu uygulama, nesneleri "Enemy" (kırmızı) ve "Friend" (mavi) olarak sınıflandırır.

## ✨ Özellikler

- 🎥 **Gerçek Zamanlı Video İşleme**: IP kamera ve webcam desteği ile canlı görüntü işleme
- 🎯 **Gelişmiş Nesne Tespiti**: HSV renk uzayında hassas renk tespiti
- 📊 **Modern UI**: CustomTkinter ile şık ve kullanıcı dostu arayüz
- ⚙️ **Ayarlanabilir Parametreler**: Renk aralıkları, minimum alan, FPS limiti
- 📈 **Performans İzleme**: FPS ve işlem süresi takibi
- 📝 **Takip Geçmişi**: Tespit edilen nesnelerin zaman damgalı kayıtları
- 💾 **Ayar Kaydetme**: Kullanıcı ayarlarını JSON formatında saklama
- 🎨 **Kalite Ayarları**: Düşük, orta, yüksek kalite seçenekleri
- ⚡ **FPS Optimizasyonu**: Performans için ayarlanabilir FPS limitleri
- 🎯 **Hedef Seçme/Takip**: Mouse ile hedef seçme ve özel takip modu
- 🔧 **Çözünürlük Ayarları**: 480p, 720p, 1080p çözünürlük seçenekleri

## 🚀 Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- OpenCV
- NumPy
- CustomTkinter
- Pillow

### Adım Adım Kurulum

1. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

2. **Uygulamayı çalıştırın:**
```bash
# Başlatıcı ile (önerilen)
python3 run.py

# Veya doğrudan:
# Demo versiyon (webcam ile test)
python3 demo_tracker.py

# Basit versiyon (IP kamera)
python3 object_tracker.py

# Gelişmiş versiyon (tüm özellikler)
python3 enhanced_tracker.py
```

## 🎮 Kullanım

### Ana Özellikler

1. **Kamera Bağlantısı**
   - IP kamera URL'sini girin veya webcam kullanın
   - "Başlat" butonuna tıklayın

2. **Nesne Tespiti**
   - Kırmızı nesneler "ENEMY" olarak işaretlenir
   - Mavi nesneler "FRIEND" olarak işaretlenir
   - Her nesne için bounding box ve merkez nokta çizilir

3. **Hedef Seçme ve Takip**
   - "Takip Modu" butonuna tıklayın
   - Video üzerinde istediğiniz nesneye tıklayın
   - Seçilen hedef özel kutu ile vurgulanır

4. **Kalite ve Performans Ayarları**
   - "Ayarlar" butonuna tıklayarak kalite seviyesini ayarlayın
   - FPS limitini değiştirerek performansı optimize edin
   - Çözünürlük seçeneklerini kullanın

### Ayarlar Açıklaması

#### HSV Renk Uzayı
- **H (Hue)**: Renk tonu (0-180)
- **S (Saturation)**: Doygunluk (0-255)
- **V (Value)**: Parlaklık (0-255)

#### Önerilen Değerler

**Kırmızı Nesneler (Enemy):**
- Alt Aralık 1: H=0, S=100, V=100
- Üst Aralık 1: H=10, S=255, V=255
- Alt Aralık 2: H=160, S=100, V=100
- Üst Aralık 2: H=180, S=255, V=255

**Mavi Nesneler (Friend):**
- Alt Aralık: H=100, S=100, V=100
- Üst Aralık: H=130, S=255, V=255

#### Kalite Ayarları

**Düşük Kalite:**
- FPS: 15
- Bulanıklaştırma: Yüksek
- Performans: En hızlı

**Orta Kalite:**
- FPS: 25
- Bulanıklaştırma: Orta
- Performans: Dengeli

**Yüksek Kalite:**
- FPS: 30
- Bulanıklaştırma: Yok
- Performans: En kaliteli

## 🔧 Teknik Detaylar

### Algoritma
1. **Video Yakalama**: OpenCV ile IP kamera akışını yakalar
2. **Renk Dönüşümü**: BGR'den HSV'ye dönüştürme
3. **Maske Oluşturma**: Belirlenen renk aralıklarında maske oluşturma
4. **Morfolojik İşlemler**: Gürültü azaltma ve nesne birleştirme
5. **Kontur Tespiti**: Nesne sınırlarını bulma
6. **Filtreleme**: Alan bazlı filtreleme
7. **Çizim**: Bounding box ve etiket çizimi

### Performans Optimizasyonu
- Threading ile UI ve video işleme ayrımı
- FPS limiti ile CPU kullanımını kontrol
- Canvas boyutuna göre otomatik ölçekleme
- Bellek yönetimi için deque kullanımı

## 📁 Dosya Yapısı

```
├── run.py                    # Başlatıcı (önerilen)
├── demo_tracker.py           # Demo versiyon (webcam)
├── object_tracker.py         # Basit versiyon
├── enhanced_tracker.py       # Gelişmiş versiyon (tüm özellikler)
├── test_camera.py           # Test scripti
├── requirements.txt          # Bağımlılıklar
├── README.md                # Bu dosya
└── enhanced_tracker_settings.json  # Kaydedilen ayarlar (otomatik oluşur)
```

## 🐛 Sorun Giderme

### Kamera Bağlantı Sorunları
- URL'nin doğru olduğundan emin olun
- Ağ bağlantısını kontrol edin
- Kamera uygulamasının çalıştığından emin olun

### Nesne Tespit Sorunları
- Işık koşullarını kontrol edin
- Ayarlar menüsünden renk aralıklarını ayarlayın
- Minimum alan değerini düşürün

### Performans Sorunları
- FPS limitini düşürün
- Video çözünürlüğünü azaltın
- Diğer uygulamaları kapatın

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Push yapın (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🙏 Teşekkürler

- OpenCV ekibine
- CustomTkinter geliştiricilerine
- Python topluluğuna

---

**Not**: Bu uygulama eğitim amaçlı geliştirilmiştir. Gerçek dünya uygulamalarında ek güvenlik önlemleri alınmalıdır.