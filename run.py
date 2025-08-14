#!/usr/bin/env python3
"""
Nesne Takip Sistemi - Başlatıcı
Bu script, farklı versiyonlar arasında seçim yapmanızı sağlar.
"""

import sys
import subprocess
import os

def print_banner():
    """Banner yazdır"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🎯 NESNE TAKİP SİSTEMİ                    ║
    ║                    Enemy/Friend Detector                     ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Bağımlılıkları kontrol et"""
    print("🔍 Bağımlılıklar kontrol ediliyor...")
    
    try:
        import cv2
        import numpy
        import customtkinter
        from PIL import Image
        print("✅ Tüm bağımlılıklar yüklü!")
        return True
    except ImportError as e:
        print(f"❌ Eksik bağımlılık: {e}")
        print("💡 Lütfen şu komutu çalıştırın:")
        print("   pip3 install --break-system-packages opencv-python numpy Pillow customtkinter")
        return False

def show_menu():
    """Ana menüyü göster"""
    menu = """
    📋 UYGULAMA SEÇİMİ:
    
    1️⃣  Demo Versiyon (Webcam ile test)
       - Webcam kullanır
       - Hızlı test için ideal
       - Basit arayüz
    
    2️⃣  Basit Versiyon (IP Kamera)
       - IP kamera desteği
       - Temel özellikler
       - Orta seviye arayüz
    
    3️⃣  Gelişmiş Versiyon (Pro)
       - IP kamera desteği
       - Ayarlar paneli
       - Performans izleme
       - Takip geçmişi
       - Modern arayüz
       - Kalite ayarları
       - FPS optimizasyonu
       - Hedef seçme/takip
    
    4️⃣  Test Scripti
       - Sistem testi
       - Bağlantı kontrolü
    
    0️⃣  Çıkış
    
    """
    print(menu)

def run_application(choice):
    """Seçilen uygulamayı çalıştır"""
    apps = {
        '1': 'demo_tracker.py',
        '2': 'object_tracker.py', 
        '3': 'enhanced_tracker.py',
        '4': 'test_camera.py'
    }
    
    if choice in apps:
        app_file = apps[choice]
        if os.path.exists(app_file):
            print(f"🚀 {app_file} başlatılıyor...")
            try:
                subprocess.run([sys.executable, app_file], check=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ Uygulama hatası: {e}")
            except KeyboardInterrupt:
                print("\n⏹️ Uygulama durduruldu.")
        else:
            print(f"❌ Dosya bulunamadı: {app_file}")
    elif choice == '0':
        print("👋 Görüşürüz!")
        sys.exit(0)
    else:
        print("❌ Geçersiz seçim!")

def main():
    """Ana fonksiyon"""
    print_banner()
    
    # Bağımlılıkları kontrol et
    if not check_dependencies():
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("🎯 Seçiminizi yapın (0-4): ").strip()
            run_application(choice)
            
            if choice != '0':
                input("\n⏸️ Devam etmek için Enter'a basın...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Görüşürüz!")
            break
        except EOFError:
            print("\n\n👋 Görüşürüz!")
            break

if __name__ == "__main__":
    main()