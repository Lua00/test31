import os
import json
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk

from crypto_manager import (
    encrypt_text,
    decrypt_text,
    encrypt_bytes,
    decrypt_bytes,
    DEFAULT_ITERATIONS,
)


APP_TITLE = "Modern Encryptor"
SETTINGS_DIR = os.path.join(os.path.expanduser("~"), ".modern_encryptor")
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "settings.json")


class Settings:
    def __init__(self) -> None:
        self.appearance_mode = "System"  # "Light" | "Dark" | "System"
        self.color_theme = "blue"  # "blue" | "green" | "dark-blue"
        self.iterations = DEFAULT_ITERATIONS
        self.load()

    def load(self) -> None:
        try:
            if not os.path.exists(SETTINGS_FILE):
                return
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.appearance_mode = data.get("appearance_mode", self.appearance_mode)
            self.color_theme = data.get("color_theme", self.color_theme)
            self.iterations = int(data.get("iterations", self.iterations))
        except Exception:
            pass

    def save(self) -> None:
        try:
            os.makedirs(SETTINGS_DIR, exist_ok=True)
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "appearance_mode": self.appearance_mode,
                        "color_theme": self.color_theme,
                        "iterations": int(self.iterations),
                    },
                    f,
                    indent=2,
                    ensure_ascii=False,
                )
        except Exception as exc:
            print(f"Ayarlar kaydedilemedi: {exc}")


class App(ctk.CTk):
    def __init__(self) -> None:
        self.settings = Settings()
        ctk.set_appearance_mode(self.settings.appearance_mode)
        ctk.set_default_color_theme(self.settings.color_theme)

        super().__init__()
        self.title(APP_TITLE)
        self.geometry("980x640")
        self.minsize(880, 560)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        self.tab_text = self.tabview.add("Metin")
        self.tab_file = self.tabview.add("Dosya")
        self.tab_settings = self.tabview.add("Ayarlar")

        self._build_text_tab()
        self._build_file_tab()
        self._build_settings_tab()

    # ---- Text Tab ----
    def _build_text_tab(self) -> None:
        frame = self.tab_text
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(2, weight=1)

        # Input
        label_in = ctk.CTkLabel(frame, text="Girdi (Düz Metin veya ENCV1$..)")
        label_in.grid(row=0, column=0, sticky="w", padx=(8, 8), pady=(8, 4))
        self.text_input = ctk.CTkTextbox(frame, wrap="word")
        self.text_input.grid(row=1, column=0, sticky="nsew", padx=(8, 8), pady=(0, 8))

        # Output
        label_out = ctk.CTkLabel(frame, text="Çıktı")
        label_out.grid(row=0, column=2, sticky="w", padx=(8, 8), pady=(8, 4))
        self.text_output = ctk.CTkTextbox(frame, wrap="word")
        self.text_output.grid(row=1, column=2, sticky="nsew", padx=(8, 8), pady=(0, 8))

        # Controls
        controls = ctk.CTkFrame(frame)
        controls.grid(row=2, column=0, columnspan=3, sticky="ew", padx=8, pady=(0, 8))
        controls.grid_columnconfigure(5, weight=1)

        self.entry_password_text = ctk.CTkEntry(controls, placeholder_text="Parola", show="*")
        self.entry_password_text.grid(row=0, column=0, padx=8, pady=12)

        self.show_pw_var_text = tk.BooleanVar(value=False)
        self.chk_show_pw_text = ctk.CTkCheckBox(
            controls, text="Parolayı Göster", variable=self.show_pw_var_text, command=self._toggle_pw_text
        )
        self.chk_show_pw_text.grid(row=0, column=1, padx=4)

        self.btn_encrypt_text = ctk.CTkButton(controls, text="Şifrele", command=self._on_encrypt_text)
        self.btn_encrypt_text.grid(row=0, column=2, padx=8)

        self.btn_decrypt_text = ctk.CTkButton(controls, text="Şifre Çöz", command=self._on_decrypt_text)
        self.btn_decrypt_text.grid(row=0, column=3, padx=8)

        self.btn_copy = ctk.CTkButton(controls, text="Kopyala", command=self._copy_output)
        self.btn_copy.grid(row=0, column=4, padx=8)

    def _toggle_pw_text(self) -> None:
        self.entry_password_text.configure(show="" if self.show_pw_var_text.get() else "*")

    def _on_encrypt_text(self) -> None:
        plaintext = self.text_input.get("1.0", "end").strip()
        password = self.entry_password_text.get()
        if not plaintext:
            messagebox.showwarning(APP_TITLE, "Lütfen metin girin.")
            return
        if not password:
            messagebox.showwarning(APP_TITLE, "Lütfen parola girin.")
            return
        try:
            result = encrypt_text(plaintext=plaintext, password=password, iterations=self.settings.iterations)
            self.text_output.delete("1.0", "end")
            self.text_output.insert("1.0", result)
        except Exception as exc:
            messagebox.showerror(APP_TITLE, f"Şifreleme başarısız: {exc}")

    def _on_decrypt_text(self) -> None:
        payload = self.text_input.get("1.0", "end").strip()
        password = self.entry_password_text.get()
        if not payload:
            messagebox.showwarning(APP_TITLE, "Lütfen şifreli metni girin.")
            return
        if not password:
            messagebox.showwarning(APP_TITLE, "Lütfen parola girin.")
            return
        try:
            result = decrypt_text(payload=payload, password=password, iterations=self.settings.iterations)
            self.text_output.delete("1.0", "end")
            self.text_output.insert("1.0", result)
        except Exception as exc:
            messagebox.showerror(APP_TITLE, f"Şifre çözme başarısız: {exc}")

    def _copy_output(self) -> None:
        text = self.text_output.get("1.0", "end").strip()
        if not text:
            return
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()
        messagebox.showinfo(APP_TITLE, "Çıktı panoya kopyalandı.")

    # ---- File Tab ----
    def _build_file_tab(self) -> None:
        frame = self.tab_file
        frame.grid_columnconfigure(1, weight=1)

        # File choose
        lbl_file = ctk.CTkLabel(frame, text="Dosya")
        lbl_file.grid(row=0, column=0, sticky="w", padx=8, pady=(12, 4))
        self.entry_file = ctk.CTkEntry(frame, placeholder_text="Dosya yolu")
        self.entry_file.grid(row=0, column=1, sticky="ew", padx=8, pady=(12, 4))
        btn_browse = ctk.CTkButton(frame, text="Gözat", command=self._browse_file)
        btn_browse.grid(row=0, column=2, padx=8, pady=(12, 4))

        # Password
        self.entry_password_file = ctk.CTkEntry(frame, placeholder_text="Parola", show="*")
        self.entry_password_file.grid(row=1, column=1, sticky="ew", padx=8, pady=8)
        self.show_pw_var_file = tk.BooleanVar(value=False)
        chk_show_pw_file = ctk.CTkCheckBox(
            frame, text="Parolayı Göster", variable=self.show_pw_var_file, command=self._toggle_pw_file
        )
        chk_show_pw_file.grid(row=1, column=2, padx=8, pady=8)

        # Actions
        actions = ctk.CTkFrame(frame)
        actions.grid(row=2, column=0, columnspan=3, sticky="ew", padx=8, pady=8)
        actions.grid_columnconfigure(3, weight=1)

        self.btn_encrypt_file = ctk.CTkButton(actions, text="Şifrele", command=self._on_encrypt_file)
        self.btn_encrypt_file.grid(row=0, column=0, padx=8, pady=12)
        self.btn_decrypt_file = ctk.CTkButton(actions, text="Şifre Çöz", command=self._on_decrypt_file)
        self.btn_decrypt_file.grid(row=0, column=1, padx=8, pady=12)

        self.progress = ctk.CTkProgressBar(actions)
        self.progress.grid(row=0, column=2, sticky="ew", padx=12)
        self.progress.set(0)

        self.status_label = ctk.CTkLabel(actions, text="Hazır")
        self.status_label.grid(row=0, column=3, sticky="e", padx=8)

    def _toggle_pw_file(self) -> None:
        self.entry_password_file.configure(show="" if self.show_pw_var_file.get() else "*")

    def _browse_file(self) -> None:
        path = filedialog.askopenfilename()
        if path:
            self.entry_file.delete(0, "end")
            self.entry_file.insert(0, path)

    def _run_bg(self, fn, on_done):
        def task():
            try:
                fn()
            except Exception as exc:
                self._set_status(f"Hata: {exc}")
                messagebox.showerror(APP_TITLE, str(exc))
            finally:
                self.progress.stop()
                on_done()
        threading.Thread(target=task, daemon=True).start()

    def _set_status(self, text: str) -> None:
        self.status_label.configure(text=text)
        self.update_idletasks()

    def _on_encrypt_file(self) -> None:
        path = self.entry_file.get().strip()
        password = self.entry_password_file.get()
        if not path or not os.path.isfile(path):
            messagebox.showwarning(APP_TITLE, "Lütfen geçerli bir dosya seçin.")
            return
        if not password:
            messagebox.showwarning(APP_TITLE, "Lütfen parola girin.")
            return

        def work():
            with open(path, "rb") as f:
                data = f.read()
            blob = encrypt_bytes(data, password=password, iterations=self.settings.iterations)
            out_path = path + ".enc"
            with open(out_path, "wb") as f:
                f.write(blob)
            self._set_status(f"Kaydedildi: {out_path}")

        self.progress.configure(mode="indeterminate")
        self.progress.start()
        self._set_status("Şifreleniyor...")
        self._run_bg(work, on_done=lambda: None)

    def _on_decrypt_file(self) -> None:
        path = self.entry_file.get().strip()
        password = self.entry_password_file.get()
        if not path or not os.path.isfile(path):
            messagebox.showwarning(APP_TITLE, "Lütfen geçerli bir dosya seçin.")
            return
        if not password:
            messagebox.showwarning(APP_TITLE, "Lütfen parola girin.")
            return

        def work():
            with open(path, "rb") as f:
                blob = f.read()
            data = decrypt_bytes(blob, password=password, iterations=self.settings.iterations)
            # produce filename without .enc if present, else append .dec
            if path.endswith(".enc"):
                out_path = path[:-4]
            else:
                out_path = path + ".dec"
            with open(out_path, "wb") as f:
                f.write(data)
            self._set_status(f"Kaydedildi: {out_path}")

        self.progress.configure(mode="indeterminate")
        self.progress.start()
        self._set_status("Çözülüyor...")
        self._run_bg(work, on_done=lambda: None)

    # ---- Settings Tab ----
    def _build_settings_tab(self) -> None:
        frame = self.tab_settings
        frame.grid_columnconfigure(1, weight=1)

        lbl_theme = ctk.CTkLabel(frame, text="Tema")
        lbl_theme.grid(row=0, column=0, sticky="w", padx=8, pady=(16, 8))
        self.opt_theme = ctk.CTkOptionMenu(
            frame, values=["System", "Light", "Dark"], command=self._on_theme_changed
        )
        self.opt_theme.set(self.settings.appearance_mode)
        self.opt_theme.grid(row=0, column=1, sticky="w", padx=8, pady=(16, 8))

        lbl_color = ctk.CTkLabel(frame, text="Vurgu Rengi")
        lbl_color.grid(row=1, column=0, sticky="w", padx=8, pady=8)
        self.opt_color = ctk.CTkOptionMenu(
            frame, values=["blue", "green", "dark-blue"], command=self._on_color_changed
        )
        self.opt_color.set(self.settings.color_theme)
        self.opt_color.grid(row=1, column=1, sticky="w", padx=8, pady=8)

        lbl_iter = ctk.CTkLabel(frame, text="PBKDF2 Iteration (güvenlik/seçenek)")
        lbl_iter.grid(row=2, column=0, sticky="w", padx=8, pady=8)
        self.iter_var = tk.IntVar(value=self.settings.iterations)
        self.iter_entry = ctk.CTkEntry(frame, textvariable=self.iter_var)
        self.iter_entry.grid(row=2, column=1, sticky="w", padx=8, pady=8)

        save_btn = ctk.CTkButton(frame, text="Kaydet", command=self._save_settings)
        save_btn.grid(row=3, column=0, columnspan=2, sticky="w", padx=8, pady=16)

    def _on_theme_changed(self, value: str) -> None:
        self.settings.appearance_mode = value
        ctk.set_appearance_mode(value)
        self.settings.save()

    def _on_color_changed(self, value: str) -> None:
        self.settings.color_theme = value
        ctk.set_default_color_theme(value)
        self.settings.save()

    def _save_settings(self) -> None:
        try:
            iterations = int(self.iter_var.get())
            if iterations < 50_000:
                raise ValueError("Iteration çok düşük (>= 50000)")
            self.settings.iterations = iterations
            self.settings.save()
            messagebox.showinfo(APP_TITLE, "Ayarlar kaydedildi.")
        except Exception as exc:
            messagebox.showerror(APP_TITLE, f"Geçersiz değer: {exc}")


if __name__ == "__main__":
    app = App()
    app.mainloop()