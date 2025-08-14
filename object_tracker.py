import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import threading
import time
from collections import deque

class ObjectTracker:
    def __init__(self):
        # Ana pencere ayarları
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("Nesne Takip Sistemi - Enemy/Friend Detector")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        
        # Video capture
        self.cap = None
        self.is_running = False
        self.video_url = "http://192.168.1.109:8080/video"
        
        # Nesne takip değişkenleri
        self.red_objects = []
        self.blue_objects = []
        self.tracking_history = deque(maxlen=30)
        
        # Renk aralıkları (HSV)
        self.red_lower1 = np.array([0, 100, 100])
        self.red_upper1 = np.array([10, 255, 255])
        self.red_lower2 = np.array([160, 100, 100])
        self.red_upper2 = np.array([180, 255, 255])
        
        self.blue_lower = np.array([100, 100, 100])
        self.blue_upper = np.array([130, 255, 255])
        
        self.setup_ui()
        
    def setup_ui(self):
        # Ana frame
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Başlık
        title_label = ctk.CTkLabel(
            main_frame, 
            text="🎯 Nesne Takip Sistemi", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#00ff88"
        )
        title_label.pack(pady=(0, 20))
        
        # Kontrol paneli
        control_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b", corner_radius=15)
        control_frame.pack(fill="x", pady=(0, 20))
        
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
        
        self.stop_button.configure(state="disabled")
        
        # URL girişi
        url_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        url_frame.pack(pady=10)
        
        ctk.CTkLabel(url_frame, text="Kamera URL:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        
        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="Kamera URL'sini girin...",
            width=300,
            height=35
        )
        self.url_entry.pack(side="left", padx=5)
        self.url_entry.insert(0, self.video_url)
        
        # Video frame
        video_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b", corner_radius=15)
        video_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Video başlığı
        video_title = ctk.CTkLabel(
            video_frame,
            text="📹 Kamera Görüntüsü",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#00ccff"
        )
        video_title.pack(pady=15)
        
        # Video canvas
        self.video_canvas = tk.Canvas(
            video_frame,
            bg="#1a1a1a",
            highlightthickness=0,
            width=800,
            height=500
        )
        self.video_canvas.pack(pady=(0, 15))
        
        # Bilgi paneli
        info_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b", corner_radius=15)
        info_frame.pack(fill="x")
        
        # Bilgi başlığı
        info_title = ctk.CTkLabel(
            info_frame,
            text="📊 Tespit Edilen Nesneler",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffaa00"
        )
        info_title.pack(pady=15)
        
        # Nesne sayıları
        stats_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        stats_frame.pack(pady=(0, 15))
        
        # Kırmızı nesneler (Enemy)
        enemy_frame = ctk.CTkFrame(stats_frame, fg_color="#440000", corner_radius=10)
        enemy_frame.pack(side="left", padx=10, fill="x", expand=True)
        
        self.enemy_count_label = ctk.CTkLabel(
            enemy_frame,
            text="🔴 Enemy: 0",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ff6666"
        )
        self.enemy_count_label.pack(pady=10)
        
        # Mavi nesneler (Friend)
        friend_frame = ctk.CTkFrame(stats_frame, fg_color="#004400", corner_radius=10)
        friend_frame.pack(side="left", padx=10, fill="x", expand=True)
        
        self.friend_count_label = ctk.CTkLabel(
            friend_frame,
            text="🔵 Friend: 0",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#66ff66"
        )
        self.friend_count_label.pack(pady=10)
        
        # Durum bilgisi
        self.status_label = ctk.CTkLabel(
            info_frame,
            text="⏳ Kamera bekleniyor...",
            font=ctk.CTkFont(size=14),
            text_color="#888888"
        )
        self.status_label.pack(pady=(0, 15))
        
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
            400, 250,
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
                
            while self.is_running:
                ret, frame = self.cap.read()
                if not ret:
                    continue
                    
                # Frame'i işle
                processed_frame = self.process_frame(frame)
                
                # UI'yi güncelle
                self.update_ui(processed_frame)
                
                time.sleep(0.03)  # ~30 FPS
                
        except Exception as e:
            self.status_label.configure(text=f"❌ Hata: {str(e)}")
            self.stop_video()
            
    def process_frame(self, frame):
        """Frame'i işle ve nesneleri tespit et"""
        # Frame boyutunu ayarla
        frame = cv2.resize(frame, (800, 500))
        
        # HSV'ye dönüştür
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Kırmızı nesneleri tespit et (Enemy)
        red_mask1 = cv2.inRange(hsv, self.red_lower1, self.red_upper1)
        red_mask2 = cv2.inRange(hsv, self.red_lower2, self.red_upper2)
        red_mask = red_mask1 + red_mask2
        
        # Mavi nesneleri tespit et (Friend)
        blue_mask = cv2.inRange(hsv, self.blue_lower, self.blue_upper)
        
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
            if area > 500:  # Minimum alan
                x, y, w, h = cv2.boundingRect(contour)
                self.red_objects.append((x, y, w, h))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "ENEMY", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Mavi nesneler (Friend)
        for contour in blue_contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Minimum alan
                x, y, w, h = cv2.boundingRect(contour)
                self.blue_objects.append((x, y, w, h))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, "FRIEND", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        
        # Takip geçmişini güncelle
        self.tracking_history.append({
            'red': len(self.red_objects),
            'blue': len(self.blue_objects),
            'timestamp': time.time()
        })
        
        return frame
        
    def update_ui(self, frame):
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
            
        except Exception as e:
            print(f"UI güncelleme hatası: {e}")
            
    def run(self):
        """Uygulamayı çalıştır"""
        self.root.mainloop()
        
    def __del__(self):
        """Temizlik"""
        if self.cap:
            self.cap.release()

if __name__ == "__main__":
    app = ObjectTracker()
    app.run()