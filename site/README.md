# PHP + Vanilla JS Blog ve Üyelik Sitesi

## Özellikler
- Kayıt / Giriş / Çıkış
- Mock üyelik satın alma (tek tıkla aktif eder)
- Blog yazısı oluşturma (isteğe bağlı kapak görseli yükleme)
- SQLite veritabanı, dosya tabanlı depolama

## Dizinyapısı
- `public/`: Sunulan dosyalar ve sayfalar
  - `index.php`, `blog.php`, `post.php`, `login.php`, `register.php`, `dashboard.php`, `store.php`, `purchase.php`, `post_create.php`
  - `css/styles.css`, `js/main.js`, `uploads/`
- `includes/`: PHP yardımcıları (`db.php`)
- `scripts/`: Komut satırı scriptleri (`init_db.php`)
- `data/`: `app.sqlite` veritabanı dosyası (otomatik oluşturulur)

## Gereksinimler
- PHP (CLI) + PDO SQLite (`pdo_sqlite` / `sqlite3`)

## Kurulum
1. PHP ve SQLite eklentisini yükle (Debian/Ubuntu):
   ```bash
   sudo apt-get update && sudo apt-get install -y php php-sqlite3
   ```
2. Upload klasörü mevcut değilse oluştur:
   ```bash
   mkdir -p /workspace/site/public/uploads
   ```
3. Veritabanı şemasını başlat:
   ```bash
   php /workspace/site/scripts/init_db.php
   ```

## Geliştirme Sunucusu
Yerleşik PHP sunucusunu `public` kökünden çalıştır:
```bash
php -S 0.0.0.0:8000 -t /workspace/site/public
```
Ardından tarayıcıdan `http://localhost:8000` adresine git.

## Notlar
- Görsel yüklemeleri `public/uploads/` altına kaydedilir.
- Bu proje demo amaçlıdır; gerçek ödeme entegrasyonu içermez.