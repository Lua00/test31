import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import threading
import time
from collections import deque
import json
import os

class AdvancedObjectTracker:
    def __init__(self):
        # Ana pencere ayarları
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("🎯 Gelişmiş Nesne Takip Sistemi - Enemy/Friend Detector Pro")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#1a1a1a')
        
        # Video capture
        self.cap = None
        self.is_running = False
        self.video_url = "http://192.168.1.109:8080/video"
        
        # Nesne takip değişkenleri
        self.red_objects = []
        self.blue_objects = []
        self.tracking_history = deque(maxlen=50)
        self.object_tracks = {}  # Nesne takip geçmişi
        
        # Ayarlar
        self.settings = {
            'red_lower1': [0, 100, 100],
            'red_upper1': [10, 255, 255],
            'red_lower2': [160, 100, 100],
            'red_upper2': [180, 255, 255],
            'blue_lower': [100, 100, 100],
            'blue_upper': [130, 255, 255],
            'min_area': 500,
            'max_area': 50000,
            'tracking_threshold': 30,
            'fps_limit': 30
        }
        
        # Ayarları yükle
        self.load_settings()
        
        self.setup_ui()
        
    def load_settings(self):
        """Ayarları dosyadan yükle"""
        try:
            if os.path.exists('tracker_settings.json'):
                with open('tracker_settings.json', 'r') as f:
                    saved_settings = json.load(f)
                    self.settings.update(saved_settings)
        except Exception as e:
            print(f"Ayar yükleme hatası: {e}")
            
    def save_settings(self):
        """Ayarları dosyaya kaydet"""
        try:
            with open('tracker_settings.json', 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Ayar kaydetme hatası: {e}")
        
    def setup_ui(self):
        # Ana frame
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Başlık
        title_label = ctk.CTkLabel(
            main_frame, 
            text="🎯 Gelişmiş Nesne Takip Sistemi", 
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#00ff88"
        )
        title_label.pack(pady=(0, 20))
        
        # Ana içerik frame
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        # Sol panel (Video)
        left_panel = ctk.CTkFrame(content_frame, fg_color="#2b2b2b", corner_radius=15)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Video başlığı
        video_title = ctk.CTkLabel(
            left_panel,
            text="📹 Kamera Görüntüsü",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#00ccff"
        )
        video_title.pack(pady=15)
        
        # Video canvas
        self.video_canvas = tk.Canvas(
            left_panel,
            bg="#1a1a1a",
            highlightthickness=0,
            width=900,
            height=600
        )
        self.video_canvas.pack(pady=(0, 15), padx=15)
        
        # Kontrol paneli
        control_frame = ctk.CTkFrame(left_panel, fg_color="#333333", corner_radius=10)
        control_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Kontrol butonları
        button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame.pack(pady=15)
        
        self.start_button = ctk.CTkButton(
            button_frame,
            text="▶️ Başlat",
            command=self.start_video,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#00aa44",
            hover_color="#008833",
            width=120,
            height=40
        )
        self.start_button.pack(side="left", padx=10)
        
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="⏹️ Durdur",
            command=self.stop_video,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#aa0000",
            hover_color="#880000",
            width=120,
            height=40
        )
        self.stop_button.pack(side="left", padx=10)
        
        self.settings_button = ctk.CTkButton(
            button_frame,
            text="⚙️ Ayarlar",
            command=self.show_settings,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#666666",
            hover_color="#555555",
            width=120,
            height=40
        )
        self.settings_button.pack(side="left", padx=10)
        
        self.stop_button.configure(state="disabled")
        
        # URL girişi
        url_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        url_frame.pack(pady=10)
        
        ctk.CTkLabel(url_frame, text="Kamera URL:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        
        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="Kamera URL'sini girin...",
            width=400,
            height=35
        )
        self.url_entry.pack(side="left", padx=5)
        self.url_entry.insert(0, self.video_url)
        
        # Sağ panel (Bilgiler)
        right_panel = ctk.CTkFrame(content_frame, fg_color="#2b2b2b", corner_radius=15)
        right_panel.pack(side="right", fill="y", padx=(10, 0))
        
        # Bilgi başlığı
        info_title = ctk.CTkLabel(
            right_panel,
            text="📊 Sistem Bilgileri",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffaa00"
        )
        info_title.pack(pady=15)
        
        # Nesne sayıları
        stats_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        stats_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Kırmızı nesneler (Enemy)
        enemy_frame = ctk.CTkFrame(stats_frame, fg_color="#440000", corner_radius=10)
        enemy_frame.pack(fill="x", pady=5)
        
        self.enemy_count_label = ctk.CTkLabel(
            enemy_frame,
            text="🔴 Enemy: 0",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ff6666"
        )
        self.enemy_count_label.pack(pady=15)
        
        # Mavi nesneler (Friend)
        friend_frame = ctk.CTkFrame(stats_frame, fg_color="#004400", corner_radius=10)
        friend_frame.pack(fill="x", pady=5)
        
        self.friend_count_label = ctk.CTkLabel(
            friend_frame,
            text="🔵 Friend: 0",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#66ff66"
        )
        self.friend_count_label.pack(pady=15)
        
        # Performans bilgileri
        perf_frame = ctk.CTkFrame(right_panel, fg_color="#333333", corner_radius=10)
        perf_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        perf_title = ctk.CTkLabel(
            perf_frame,
            text="⚡ Performans",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#00ccff"
        )
        perf_title.pack(pady=10)
        
        self.fps_label = ctk.CTkLabel(
            perf_frame,
            text="FPS: 0",
            font=ctk.CTkFont(size=14),
            text_color="#cccccc"
        )
        self.fps_label.pack(pady=5)
        
        self.processing_time_label = ctk.CTkLabel(
            perf_frame,
            text="İşlem Süresi: 0ms",
            font=ctk.CTkFont(size=14),
            text_color="#cccccc"
        )
        self.processing_time_label.pack(pady=5)
        
        # Durum bilgisi
        self.status_label = ctk.CTkLabel(
            right_panel,
            text="⏳ Kamera bekleniyor...",
            font=ctk.CTkFont(size=14),
            text_color="#888888"
        )
        self.status_label.pack(pady=15)
        
        # Takip geçmişi
        history_frame = ctk.CTkFrame(right_panel, fg_color="#333333", corner_radius=10)
        history_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        history_title = ctk.CTkLabel(
            history_frame,
            text="📈 Takip Geçmişi",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#00ccff"
        )
        history_title.pack(pady=10)
        
        self.history_text = ctk.CTkTextbox(
            history_frame,
            width=300,
            height=200,
            font=ctk.CTkFont(size=12)
        )
        self.history_text.pack(padx=10, pady=(0, 10), fill="both", expand=True)
        
    def show_settings(self):
        """Ayarlar penceresini göster"""
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("⚙️ Ayarlar")
        settings_window.geometry("600x700")
        settings_window.configure(bg='#1a1a1a')
        
        # Ayarlar başlığı
        title = ctk.CTkLabel(
            settings_window,
            text="⚙️ Nesne Tespit Ayarları",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#00ff88"
        )
        title.pack(pady=20)
        
        # Ayarlar frame
        settings_frame = ctk.CTkScrollableFrame(settings_window, fg_color="transparent")
        settings_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Kırmızı nesne ayarları
        red_frame = ctk.CTkFrame(settings_frame, fg_color="#440000", corner_radius=10)
        red_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(red_frame, text="🔴 Kırmızı Nesne (Enemy) Ayarları", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Kırmızı alt aralık 1
        red1_frame = ctk.CTkFrame(red_frame, fg_color="transparent")
        red1_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(red1_frame, text="Alt Aralık 1 (H,S,V):").pack(side="left")
        
        self.red_lower1_h = ctk.CTkEntry(red1_frame, width=50)
        self.red_lower1_h.pack(side="left", padx=5)
        self.red_lower1_h.insert(0, str(self.settings['red_lower1'][0]))
        
        self.red_lower1_s = ctk.CTkEntry(red1_frame, width=50)
        self.red_lower1_s.pack(side="left", padx=5)
        self.red_lower1_s.insert(0, str(self.settings['red_lower1'][1]))
        
        self.red_lower1_v = ctk.CTkEntry(red1_frame, width=50)
        self.red_lower1_v.pack(side="left", padx=5)
        self.red_lower1_v.insert(0, str(self.settings['red_lower1'][2]))
        
        # Kırmızı üst aralık 1
        red1_upper_frame = ctk.CTkFrame(red_frame, fg_color="transparent")
        red1_upper_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(red1_upper_frame, text="Üst Aralık 1 (H,S,V):").pack(side="left")
        
        self.red_upper1_h = ctk.CTkEntry(red1_upper_frame, width=50)
        self.red_upper1_h.pack(side="left", padx=5)
        self.red_upper1_h.insert(0, str(self.settings['red_upper1'][0]))
        
        self.red_upper1_s = ctk.CTkEntry(red1_upper_frame, width=50)
        self.red_upper1_s.pack(side="left", padx=5)
        self.red_upper1_s.insert(0, str(self.settings['red_upper1'][1]))
        
        self.red_upper1_v = ctk.CTkEntry(red1_upper_frame, width=50)
        self.red_upper1_v.pack(side="left", padx=5)
        self.red_upper1_v.insert(0, str(self.settings['red_upper1'][2]))
        
        # Mavi nesne ayarları
        blue_frame = ctk.CTkFrame(settings_frame, fg_color="#004400", corner_radius=10)
        blue_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(blue_frame, text="🔵 Mavi Nesne (Friend) Ayarları", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Mavi alt aralık
        blue_lower_frame = ctk.CTkFrame(blue_frame, fg_color="transparent")
        blue_lower_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(blue_lower_frame, text="Alt Aralık (H,S,V):").pack(side="left")
        
        self.blue_lower_h = ctk.CTkEntry(blue_lower_frame, width=50)
        self.blue_lower_h.pack(side="left", padx=5)
        self.blue_lower_h.insert(0, str(self.settings['blue_lower'][0]))
        
        self.blue_lower_s = ctk.CTkEntry(blue_lower_frame, width=50)
        self.blue_lower_s.pack(side="left", padx=5)
        self.blue_lower_s.insert(0, str(self.settings['blue_lower'][1]))
        
        self.blue_lower_v = ctk.CTkEntry(blue_lower_frame, width=50)
        self.blue_lower_v.pack(side="left", padx=5)
        self.blue_lower_v.insert(0, str(self.settings['blue_lower'][2]))
        
        # Mavi üst aralık
        blue_upper_frame = ctk.CTkFrame(blue_frame, fg_color="transparent")
        blue_upper_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(blue_upper_frame, text="Üst Aralık (H,S,V):").pack(side="left")
        
        self.blue_upper_h = ctk.CTkEntry(blue_upper_frame, width=50)
        self.blue_upper_h.pack(side="left", padx=5)
        self.blue_upper_h.insert(0, str(self.settings['blue_upper'][0]))
        
        self.blue_upper_s = ctk.CTkEntry(blue_upper_frame, width=50)
        self.blue_upper_s.pack(side="left", padx=5)
        self.blue_upper_s.insert(0, str(self.settings['blue_upper'][1]))
        
        self.blue_upper_v = ctk.CTkEntry(blue_upper_frame, width=50)
        self.blue_upper_v.pack(side="left", padx=5)
        self.blue_upper_v.insert(0, str(self.settings['blue_upper'][2]))
        
        # Genel ayarlar
        general_frame = ctk.CTkFrame(settings_frame, fg_color="#333333", corner_radius=10)
        general_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(general_frame, text="🔧 Genel Ayarlar", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        # Minimum alan
        min_area_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
        min_area_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(min_area_frame, text="Minimum Alan:").pack(side="left")
        self.min_area_entry = ctk.CTkEntry(min_area_frame, width=100)
        self.min_area_entry.pack(side="left", padx=10)
        self.min_area_entry.insert(0, str(self.settings['min_area']))
        
        # FPS limiti
        fps_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
        fps_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(fps_frame, text="FPS Limiti:").pack(side="left")
        self.fps_entry = ctk.CTkEntry(fps_frame, width=100)
        self.fps_entry.pack(side="left", padx=10)
        self.fps_entry.insert(0, str(self.settings['fps_limit']))
        
        # Butonlar
        button_frame = ctk.CTkFrame(settings_window, fg_color="transparent")
        button_frame.pack(pady=20)
        
        save_button = ctk.CTkButton(
            button_frame,
            text="💾 Kaydet",
            command=lambda: self.save_settings_from_ui(settings_window),
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#00aa44",
            hover_color="#008833",
            width=120,
            height=40
        )
        save_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="❌ İptal",
            command=settings_window.destroy,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#aa0000",
            hover_color="#880000",
            width=120,
            height=40
        )
        cancel_button.pack(side="left", padx=10)
        
    def save_settings_from_ui(self, window):
        """UI'den ayarları kaydet"""
        try:
            # Kırmızı ayarları
            self.settings['red_lower1'] = [
                int(self.red_lower1_h.get()),
                int(self.red_lower1_s.get()),
                int(self.red_lower1_v.get())
            ]
            self.settings['red_upper1'] = [
                int(self.red_upper1_h.get()),
                int(self.red_upper1_s.get()),
                int(self.red_upper1_v.get())
            ]
            
            # Mavi ayarları
            self.settings['blue_lower'] = [
                int(self.blue_lower_h.get()),
                int(self.blue_lower_s.get()),
                int(self.blue_lower_v.get())
            ]
            self.settings['blue_upper'] = [
                int(self.blue_upper_h.get()),
                int(self.blue_upper_s.get()),
                int(self.blue_upper_v.get())
            ]
            
            # Genel ayarlar
            self.settings['min_area'] = int(self.min_area_entry.get())
            self.settings['fps_limit'] = int(self.fps_entry.get())
            
            # Ayarları kaydet
            self.save_settings()
            
            messagebox.showinfo("Başarılı", "Ayarlar kaydedildi!")
            window.destroy()
            
        except ValueError as e:
            messagebox.showerror("Hata", "Lütfen geçerli sayısal değerler girin!")
        
    def start_video(self):
        """Video akışını başlat"""
        self.video_url = self.url_entry.get()
        if not self.video_url:
            messagebox.showerror("Hata", "Lütfen geçerli bir kamera URL'si girin!")
            return
            
        self.is_running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_label.configure(text="🟢 Kamera bağlandı - Nesneler tespit ediliyor...")
        
        # Video thread'ini başlat
        self.video_thread = threading.Thread(target=self.video_loop, daemon=True)
        self.video_thread.start()
        
    def stop_video(self):
        """Video akışını durdur"""
        self.is_running = False
        if self.cap:
            self.cap.release()
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_label.configure(text="⏹️ Kamera durduruldu")
        
        # Canvas'ı temizle
        self.video_canvas.delete("all")
        self.video_canvas.create_text(
            450, 300,
            text="Kamera görüntüsü bekleniyor...",
            fill="#888888",
            font=("Arial", 16)
        )
        
    def video_loop(self):
        """Ana video döngüsü"""
        try:
            self.cap = cv2.VideoCapture(self.video_url)
            if not self.cap.isOpened():
                raise Exception("Kamera bağlantısı kurulamadı!")
                
            fps_counter = 0
            fps_start_time = time.time()
            
            while self.is_running:
                frame_start_time = time.time()
                
                ret, frame = self.cap.read()
                if not ret:
                    continue
                    
                # Frame'i işle
                processed_frame = self.process_frame(frame)
                
                # FPS hesapla
                fps_counter += 1
                if time.time() - fps_start_time >= 1.0:
                    self.current_fps = fps_counter
                    fps_counter = 0
                    fps_start_time = time.time()
                
                # İşlem süresini hesapla
                processing_time = (time.time() - frame_start_time) * 1000
                
                # UI'yi güncelle
                self.update_ui(processed_frame, processing_time)
                
                # FPS limiti
                sleep_time = max(0, (1.0 / self.settings['fps_limit']) - (time.time() - frame_start_time))
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
        except Exception as e:
            self.status_label.configure(text=f"❌ Hata: {str(e)}")
            self.stop_video()
            
    def process_frame(self, frame):
        """Frame'i işle ve nesneleri tespit et"""
        # Frame boyutunu ayarla
        frame = cv2.resize(frame, (900, 600))
        
        # HSV'ye dönüştür
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Kırmızı nesneleri tespit et (Enemy)
        red_lower1 = np.array(self.settings['red_lower1'])
        red_upper1 = np.array(self.settings['red_upper1'])
        red_lower2 = np.array(self.settings['red_lower2'])
        red_upper2 = np.array(self.settings['red_upper2'])
        
        red_mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
        red_mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
        red_mask = red_mask1 + red_mask2
        
        # Mavi nesneleri tespit et (Friend)
        blue_lower = np.array(self.settings['blue_lower'])
        blue_upper = np.array(self.settings['blue_upper'])
        blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
        
        # Morfolojik işlemler
        kernel = np.ones((5, 5), np.uint8)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
        blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
        blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel)
        
        # Konturları bul
        red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Nesneleri işle
        self.red_objects = []
        self.blue_objects = []
        
        # Kırmızı nesneler (Enemy)
        for contour in red_contours:
            area = cv2.contourArea(contour)
            if self.settings['min_area'] < area < self.settings['max_area']:
                x, y, w, h = cv2.boundingRect(contour)
                center = (x + w//2, y + h//2)
                self.red_objects.append((x, y, w, h, center))
                
                # Kutuyu çiz
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "ENEMY", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Merkez noktayı çiz
                cv2.circle(frame, center, 3, (0, 0, 255), -1)
        
        # Mavi nesneler (Friend)
        for contour in blue_contours:
            area = cv2.contourArea(contour)
            if self.settings['min_area'] < area < self.settings['max_area']:
                x, y, w, h = cv2.boundingRect(contour)
                center = (x + w//2, y + h//2)
                self.blue_objects.append((x, y, w, h, center))
                
                # Kutuyu çiz
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, "FRIEND", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                
                # Merkez noktayı çiz
                cv2.circle(frame, center, 3, (255, 0, 0), -1)
        
        # Takip geçmişini güncelle
        self.tracking_history.append({
            'red': len(self.red_objects),
            'blue': len(self.blue_objects),
            'timestamp': time.time()
        })
        
        return frame
        
    def update_ui(self, frame, processing_time):
        """UI'yi güncelle"""
        try:
            # Frame'i RGB'ye dönüştür
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # PIL Image'e dönüştür
            pil_image = Image.fromarray(frame_rgb)
            
            # Canvas boyutuna ölçekle
            canvas_width = self.video_canvas.winfo_width()
            canvas_height = self.video_canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:
                pil_image = pil_image.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)
            
            # Tkinter PhotoImage'e dönüştür
            photo = ImageTk.PhotoImage(pil_image)
            
            # Canvas'ı güncelle
            self.video_canvas.delete("all")
            self.video_canvas.create_image(0, 0, anchor="nw", image=photo)
            self.video_canvas.image = photo  # Referansı koru
            
            # Nesne sayılarını güncelle
            self.enemy_count_label.configure(text=f"🔴 Enemy: {len(self.red_objects)}")
            self.friend_count_label.configure(text=f"🔵 Friend: {len(self.blue_objects)}")
            
            # Performans bilgilerini güncelle
            if hasattr(self, 'current_fps'):
                self.fps_label.configure(text=f"FPS: {self.current_fps}")
            self.processing_time_label.configure(text=f"İşlem Süresi: {processing_time:.1f}ms")
            
            # Takip geçmişini güncelle
            self.update_history()
            
        except Exception as e:
            print(f"UI güncelleme hatası: {e}")
            
    def update_history(self):
        """Takip geçmişini güncelle"""
        try:
            if len(self.tracking_history) > 0:
                latest = self.tracking_history[-1]
                timestamp = time.strftime("%H:%M:%S", time.localtime(latest['timestamp']))
                
                history_text = f"[{timestamp}] Enemy: {latest['red']}, Friend: {latest['blue']}\n"
                
                # Son 10 kaydı göster
                current_text = self.history_text.get("1.0", "end-1c")
                lines = current_text.split('\n')
                if len(lines) > 10:
                    lines = lines[-10:]
                
                new_text = '\n'.join(lines) + history_text
                self.history_text.delete("1.0", "end")
                self.history_text.insert("1.0", new_text)
                
        except Exception as e:
            print(f"Geçmiş güncelleme hatası: {e}")
            
    def run(self):
        """Uygulamayı çalıştır"""
        self.root.mainloop()
        
    def __del__(self):
        """Temizlik"""
        if self.cap:
            self.cap.release()

if __name__ == "__main__":
    app = AdvancedObjectTracker()
    app.run()