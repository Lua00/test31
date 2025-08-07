# PHP + Vanilla JS Blog ve Üyelik Sitesi

## Özellikler
- Kayıt / Giriş / Çıkış
- Mock üyelik satın alma (tek tıkla aktif eder)
- Blog yazısı oluşturma (isteğe bağlı kapak görseli yükleme)
- SQLite veritabanı, dosya tabanlı depolama
- Üyelere özel indirilebilir dosyalar (İndirilebilirler)

## Dizinyapısı
- `public/`: Sunulan dosyalar ve sayfalar
  - `index.php`, `blog.php`, `post.php`, `login.php`, `register.php`, `dashboard.php`, `store.php`, `purchase.php`, `post_create.php`, `downloads.php`, `download.php`, `download_upload.php`
  - `css/styles.css`, `js/main.js`, `uploads/`
- `includes/`: PHP yardımcıları (`db.php`)
- `scripts/`: Komut satırı scriptleri (`init_db.php`)
- `data/`: `app.sqlite` veritabanı dosyası (otomatik oluşturulur)
- `protected/downloads/`: Üyelere özel dosya depolama (web’den direkt erişilemez)

## Gereksinimler
- PHP (CLI) + PDO SQLite (`pdo_sqlite` / `sqlite3`)

## Kurulum
1. PHP ve SQLite eklentisini yükle (Debian/Ubuntu):
   ```bash
   sudo apt-get update && sudo apt-get install -y php php-sqlite3
   ```
2. Upload ve protected klasörleri oluştur:
   ```bash
   mkdir -p /workspace/site/public/uploads /workspace/site/protected/downloads
   ```
3. Veritabanı şemasını başlat:
   ```bash
   php /workspace/site/scripts/init_db.php
   ```

## Geliştirme Sunucusu
```bash
php -S 0.0.0.0:8000 -t /workspace/site/public
```
Tarayıcı: `http://localhost:8000`

## İndirilebilirler (Üyelere Özel)
- Liste: `downloads.php` (sadece üyeler görebilir)
- İndirme: `download.php?id=...` (üyelik kontrolü yapar, dosyayı `protected/downloads` içinden stream eder)
- Admin yükleme: `download_upload.php` (ilk kullanıcı admin kabul edilir)