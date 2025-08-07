# Arcar - Android Studio'da Açma Rehberi

## 🚀 Android Studio'da Açma Adımları

1. **Android Studio'yu açın**
2. **"Open an Existing Project" seçin**
3. **`/workspace/Arcar/android` klasörünü seçin**
4. **"OK" butonuna tıklayın**

## ⚙️ İlk Kurulum

Android Studio proje açtıktan sonra:

### 1. SDK Ayarları
- File → Project Structure → SDK Location
- Android SDK path'ini ayarlayın (genellikle otomatik algılanır)

### 2. Gradle Sync
- Android Studio otomatik olarak Gradle sync yapacak
- Eğer hata alırsanız "Sync Now" butonuna tıklayın

### 3. Dependencies
- Tüm bağımlılıklar otomatik olarak indirilecek

## 📁 Proje Yapısı

```
android/
├── app/
│   ├── src/main/
│   │   ├── java/com/arcar/
│   │   │   ├── MainActivity.java      # Ana aktivite
│   │   │   └── MainApplication.java   # Uygulama sınıfı
│   │   ├── res/
│   │   │   ├── layout/
│   │   │   │   └── activity_main.xml  # Ana layout
│   │   │   └── values/
│   │   │       └── strings.xml        # String değerleri
│   │   └── AndroidManifest.xml        # Manifest dosyası
│   └── build.gradle                   # App build dosyası
├── build.gradle                       # Root build dosyası
└── settings.gradle                    # Settings dosyası
```

## 🔧 Ayarlar

### Build Configuration
- **compileSdkVersion**: 34
- **minSdkVersion**: 21
- **targetSdkVersion**: 34
- **Application ID**: com.arcar

### Permissions
- `INTERNET` - İnternet erişimi
- `READ_EXTERNAL_STORAGE` - Dosya okuma
- `WRITE_EXTERNAL_STORAGE` - Dosya yazma
- `CAMERA` - Kamera erişimi

## 🏃‍♂️ Çalıştırma

1. **Emulator veya gerçek cihaz bağlayın**
2. **"Run" butonuna tıklayın (Shift+F10)**
3. **APK build edilecek ve cihazda çalışacak**

## 🛠 Geliştirme

Bu Android projesi, React Native Arcar uygulamasının temel Android Studio yapısını içerir. 

### React Native Entegrasyonu İçin:
1. React Native modüllerini gradle'a ekleyin
2. JavaScript bundle'ları entegre edin
3. Native bridge kodlarını ekleyin

### Özelleştirme:
- `MainActivity.java` - Ana aktivite mantığı
- `activity_main.xml` - UI layout
- `AndroidManifest.xml` - Permissions ve ayarlar

## 📱 Test

Uygulama şu anda basit bir hoş geldin ekranı gösterecek:
- Arcar logosu
- Uygulama adı
- "Android Studio'da açılmaya hazır!" mesajı

## 🔄 Sonraki Adımlar

1. **React Native entegrasyonu**
2. **JavaScript bridge ekleme**
3. **Native modüller geliştirme**
4. **UI geliştirme**

---

**Not**: Bu proje Android Studio'da açılmaya ve geliştirilmeye hazır durumda!