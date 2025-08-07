# Arcar - Araç Bakım Günlüğü

Modern ve kullanıcı dostu bir araç bakım takip uygulaması. Araçlarınızın bakım ve tamir geçmişini kolayca takip edebilirsiniz.

## 🚗 Özellikler

### Temel Özellikler
- **Araç Yönetimi**: Birden fazla araç ekleyip yönetebilme
- **Bakım/Tamir Takibi**: Detaylı bakım ve tamir kayıtları
- **Fotoğraf Desteği**: Her işlem için fotoğraf ekleme
- **Modern UI**: Kullanıcı dostu ve modern tasarım
- **Yerel Depolama**: Veriler cihazda güvenle saklanır

### Araç Bilgileri
- Marka ve model bilgileri
- Yıl ve plaka bilgileri
- Güncel kilometre takibi
- Yakıt türü (Benzin, Dizel, Elektrik, Hibrit)
- Motor hacmi ve renk bilgileri
- Satın alma tarihi
- Araç fotoğrafı

### Bakım/Tamir Özellikleri
- Yağ değişimi
- Lastik değişimi  
- Fren bakımı
- Motor tamiri
- Diğer özel işlemler
- Kilometre ve tarih takibi
- Maliyet hesaplama
- Fotoğraf ekleme
- Detaylı notlar

## 🛠 Teknolojiler

- **React Native 0.80.2** - Cross-platform mobil geliştirme
- **TypeScript** - Tip güvenli JavaScript
- **React Navigation** - Navigasyon yönetimi
- **AsyncStorage** - Yerel veri depolama
- **React Native Vector Icons** - İkon kütüphanesi
- **React Native Linear Gradient** - Gradient efektleri
- **React Native Image Picker** - Fotoğraf seçimi

## 📱 Kurulum

### Gereksinimler
- Node.js (14 veya üzeri)
- React Native CLI
- Android Studio (Android için)
- Xcode (iOS için)

### Adımlar

1. Projeyi klonlayın:
```bash
git clone <proje-url>
cd Arcar
```

2. Bağımlılıkları yükleyin:
```bash
npm install
```

3. iOS için pod kurulumu (sadece iOS):
```bash
cd ios && pod install && cd ..
```

4. Uygulamayı çalıştırın:

Android için:
```bash
npm run android
```

iOS için:
```bash
npm run ios
```

## 🎨 Tasarım

Uygulama modern Material Design prensiplerini takip eder:
- **Renkler**: Mavi tonları (#3b82f6, #2563eb)
- **Tipografi**: System fontları
- **Componentler**: Kart tabanlı tasarım
- **Navigasyon**: Bottom tabs + Stack navigation
- **Animasyonlar**: Smooth geçişler

## 📂 Proje Yapısı

```
src/
├── components/         # Yeniden kullanılabilir componentler
│   ├── VehicleCard.tsx
│   ├── MaintenanceCard.tsx
│   └── FloatingActionButton.tsx
├── navigation/         # Navigasyon yapısı
│   └── AppNavigator.tsx
├── screens/           # Ekran componentleri
│   ├── HomeScreen.tsx
│   ├── VehicleListScreen.tsx
│   ├── VehicleDetailScreen.tsx
│   ├── AddVehicleScreen.tsx
│   └── ...
├── services/          # Veri yönetimi
│   └── StorageService.ts
└── types/            # TypeScript tip tanımları
    └── index.ts
```

## 🔄 Veri Yapısı

### Vehicle (Araç)
```typescript
interface Vehicle {
  id: string;
  brand: string;
  model: string;
  year: number;
  licensePlate: string;
  currentKm: number;
  fuelType: 'gasoline' | 'diesel' | 'hybrid' | 'electric';
  engineSize?: string;
  color?: string;
  purchaseDate?: string;
  imageUri?: string;
}
```

### MaintenanceRecord (Bakım Kaydı)
```typescript
interface MaintenanceRecord {
  id: string;
  vehicleId: string;
  type: 'maintenance' | 'repair';
  category: 'oil_change' | 'tire_change' | 'brake_service' | 'engine_repair' | 'other';
  description: string;
  date: string;
  kilometerage: number;
  cost?: number;
  notes?: string;
  imageUri?: string;
  nextMaintenanceKm?: number;
  nextMaintenanceDate?: string;
}
```

## 🚀 Gelecek Özellikler

- [ ] Sunucu entegrasyonu
- [ ] Bakım hatırlatıcıları
- [ ] PDF rapor çıktısı
- [ ] Yedekleme ve geri yükleme
- [ ] Multi-language desteği
- [ ] Dark mode
- [ ] Widget desteği
- [ ] QR kod ile araç paylaşımı

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

Arcar, modern araç sahiplerinin ihtiyaçlarını karşılamak için geliştirilmiştir.

---

**Not**: Bu uygulama aktif geliştirme aşamasındadır. Geri bildirimleriniz ve katkılarınız için memnun oluruz.
