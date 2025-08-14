#!/usr/bin/env python3
"""
Kamera Bağlantı Test Scripti
Bu script, kamera bağlantısını test etmek ve temel işlevselliği doğrulamak için kullanılır.
"""

import cv2
import numpy as np
import time
import sys

def test_camera_connection(url):
    """Kamera bağlantısını test et"""
    print(f"🔍 Kamera bağlantısı test ediliyor: {url}")
    
    try:
        cap = cv2.VideoCapture(url)
        
        if not cap.isOpened():
            print("❌ Kamera bağlantısı başarısız!")
            return False
            
        print("✅ Kamera bağlantısı başarılı!")
        
        # Birkaç frame oku
        for i in range(5):
            ret, frame = cap.read()
            if ret:
                print(f"✅ Frame {i+1} başarıyla okundu - Boyut: {frame.shape}")
            else:
                print(f"❌ Frame {i+1} okunamadı")
                
        cap.release()
        return True
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

def test_color_detection():
    """Renk tespit algoritmasını test et"""
    print("\n🎨 Renk tespit algoritması test ediliyor...")
    
    # Test görüntüsü oluştur
    test_image = np.zeros((300, 400, 3), dtype=np.uint8)
    
    # Kırmızı daire çiz
    cv2.circle(test_image, (100, 150), 50, (0, 0, 255), -1)
    
    # Mavi daire çiz
    cv2.circle(test_image, (300, 150), 50, (255, 0, 0), -1)
    
    # HSV'ye dönüştür
    hsv = cv2.cvtColor(test_image, cv2.COLOR_BGR2HSV)
    
    # Kırmızı maske
    red_lower1 = np.array([0, 100, 100])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([160, 100, 100])
    red_upper2 = np.array([180, 255, 255])
    
    red_mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
    red_mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
    red_mask = red_mask1 + red_mask2
    
    # Mavi maske
    blue_lower = np.array([100, 100, 100])
    blue_upper = np.array([130, 255, 255])
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    
    # Konturları bul
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    print(f"🔴 Tespit edilen kırmızı nesne sayısı: {len(red_contours)}")
    print(f"🔵 Tespit edilen mavi nesne sayısı: {len(blue_contours)}")
    
    if len(red_contours) > 0 and len(blue_contours) > 0:
        print("✅ Renk tespit algoritması çalışıyor!")
        return True
    else:
        print("❌ Renk tespit algoritmasında sorun var!")
        return False

def test_opencv_installation():
    """OpenCV kurulumunu test et"""
    print("\n📦 OpenCV kurulumu test ediliyor...")
    
    try:
        version = cv2.__version__
        print(f"✅ OpenCV versiyonu: {version}")
        
        # Temel işlevleri test et
        test_array = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.uint8)
        blurred = cv2.GaussianBlur(test_array, (3, 3), 0)
        
        if blurred is not None:
            print("✅ OpenCV temel işlevleri çalışıyor!")
            return True
        else:
            print("❌ OpenCV temel işlevlerinde sorun var!")
            return False
            
    except Exception as e:
        print(f"❌ OpenCV test hatası: {e}")
        return False

def main():
    """Ana test fonksiyonu"""
    print("🎯 Nesne Takip Sistemi - Test Scripti")
    print("=" * 50)
    
    # Test URL'leri
    test_urls = [
        "http://192.168.1.109:8080/video",
        "http://localhost:8080/video",
        "http://127.0.0.1:8080/video"
    ]
    
    # OpenCV testi
    opencv_ok = test_opencv_installation()
    
    # Renk tespit testi
    color_ok = test_color_detection()
    
    # Kamera bağlantı testi
    camera_ok = False
    working_url = None
    
    for url in test_urls:
        if test_camera_connection(url):
            camera_ok = True
            working_url = url
            break
        time.sleep(1)
    
    # Sonuçları göster
    print("\n" + "=" * 50)
    print("📊 TEST SONUÇLARI")
    print("=" * 50)
    
    print(f"OpenCV Kurulumu: {'✅ Başarılı' if opencv_ok else '❌ Başarısız'}")
    print(f"Renk Tespiti: {'✅ Başarılı' if color_ok else '❌ Başarısız'}")
    print(f"Kamera Bağlantısı: {'✅ Başarılı' if camera_ok else '❌ Başarısız'}")
    
    if working_url:
        print(f"Çalışan URL: {working_url}")
    
    # Öneriler
    print("\n💡 ÖNERİLER:")
    
    if not opencv_ok:
        print("- OpenCV'yi yeniden yükleyin: pip install opencv-python")
    
    if not color_ok:
        print("- NumPy'ı kontrol edin: pip install numpy")
    
    if not camera_ok:
        print("- Kamera URL'sini kontrol edin")
        print("- Ağ bağlantısını kontrol edin")
        print("- Kamera uygulamasının çalıştığından emin olun")
    
    if opencv_ok and color_ok and camera_ok:
        print("🎉 Tüm testler başarılı! Uygulamayı çalıştırabilirsiniz.")
        print("Komut: python advanced_tracker.py")
    else:
        print("⚠️  Bazı testler başarısız. Lütfen yukarıdaki önerileri takip edin.")

if __name__ == "__main__":
    main()