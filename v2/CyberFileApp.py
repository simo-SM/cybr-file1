#!/usr/bin/env python3
# ========================================================
# ===================| CYBER-FILE v2.7 |==================
# ===== Real-Time File Monitor + Modern GUI =============
# ===== CustomTkinter + System Tray + Multi-Icon =========
# ========================================================

import os
import sys
import time
import threading
import ctypes
import json
import itertools
from datetime import datetime
from collections import deque
from PIL import Image, ImageDraw, ImageFont, ImageTk
import customtkinter as ctk
from tkinter import messagebox, filedialog

# File monitoring
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# System Tray (optional)
try:
    import pystray
    PYSTRAY_AVAILABLE = True
except ImportError:
    PYSTRAY_AVAILABLE = False

# Alert systems
try:
    import requests
    REQUESTS_AVAILABLE = True
except:
    REQUESTS_AVAILABLE = False

# ================= CONFIGURATION =================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# ================= COLORS =================
COLORS = {
    'bg': "#0a0a0a",
    'bg_secondary': "#141414",
    'bg_card': "#1a1a1a",
    'border': "#2a2a2a",
    'created': "#00ff88",
    'deleted': "#ff3366",
    'modified': "#ffcc00",
    'moved': "#00d4ff",
    'cyan': "#00d4ff",
    'accent': "#ff00ff",
    'text': "#ffffff",
    'text_secondary': "#888888",
    'success': "#00ff88",
    'warning': "#ffaa00",
    'danger': "#ff3366"
}

EVENT_STYLES = {
    'created': {'color': COLORS['created'], 'icon': '✚', 'name': 'CREATED'},
    'deleted': {'color': COLORS['deleted'], 'icon': '✖', 'name': 'DELETED'},
    'modified': {'color': COLORS['modified'], 'icon': '✎', 'name': 'MODIFIED'},
    'moved':   {'color': COLORS['moved'],    'icon': '➜', 'name': 'MOVED'}
}

# ================= GLOBAL STATE =================
class AppState:
    def __init__(self):
        self.monitoring      = False
        self.admin_paused    = False
        self.events          = deque(maxlen=100)
        self.stats           = {'created': 0, 'deleted': 0, 'modified': 0, 'moved': 0}
        self.watched_dirs    = []
        self.start_time      = None
        self.observers       = []
        self.alert_method    = "telegram"
        self.telegram_chat_id = "6718030667"
        self.telegram_token   = "8722478444:AAHMx4pT2__9fOlbX-yz7HvBwy9tZOKKGcs"
        self.tray_icon       = None
        self.icon_animation  = None

state = AppState()

# ================= ICON MANAGER =================
class IconManager:
    """Manage all icons for the application - FIXED VERSION"""
    
    def __init__(self, app):
        self.app = app
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.icons = {}
        self.animation_running = False
        
    def get_icon_path(self, filename):
        """Get full path to icon file"""
        # Check multiple locations
        paths = [
            os.path.join(self.base_path, filename),
            os.path.join(self.base_path, "images", filename),
            os.path.join(self.base_path, "assets", filename),
            os.path.join(self.base_path, "icons", filename),
        ]
        for path in paths:
            if os.path.exists(path):
                return path
        return os.path.join(self.base_path, filename)  # Return default even if not exists
    
    def set_window_icon(self, icon_name="hacking.ico"):
        """
        Set window icon - WORKING METHOD for CustomTkinter
        Supports: .ico (Windows), .png (Linux/Mac), .xbm
        """
        icon_path = self.get_icon_path(icon_name)
        
        if not os.path.exists(icon_path):
            print(f"[Icon] File not found: {icon_path}")
            # Try with different extensions
            for ext in ['.png', '.jpg', '.gif', '.bmp']:
                alt_path = icon_path.replace('.ico', ext)
                if os.path.exists(alt_path):
                    icon_path = alt_path
                    break
            else:
                print("[Icon] Creating default icon...")
                self._create_default_icon()
                return
        
        try:
            # Method 1: Windows .ico file (BEST for Windows)
            if icon_path.endswith('.ico') and sys.platform == 'win32':
                try:
                    self.app.wm_iconbitmap(icon_path)
                    print(f"[Icon] Windows .ico set: {icon_path}")
                    return
                except Exception as e:
                    print(f"[Icon] wm_iconbitmap failed: {e}")
            
            # Method 2: PIL PhotoImage (Universal)
            img = Image.open(icon_path)
            
            # Resize to standard icon sizes
            img_16 = img.resize((16, 16), Image.Resampling.LANCZOS)
            img_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
            img_48 = img.resize((48, 48), Image.Resampling.LANCZOS)
            
            # Create PhotoImage
            self.icon_16 = ImageTk.PhotoImage(img_16)
            self.icon_32 = ImageTk.PhotoImage(img_32)
            self.icon_48 = ImageTk.PhotoImage(img_48)
            
            # Apply to window
            self.app.iconphoto(False, self.icon_16, self.icon_32, self.icon_48)
            print(f"[Icon] PIL icon set: {icon_path}")
            
            # Keep references to prevent garbage collection
            self.icons['window_16'] = self.icon_16
            self.icons['window_32'] = self.icon_32
            self.icons['window_48'] = self.icon_48
            
        except Exception as e:
            print(f"[Icon] Error setting icon: {e}")
            self._create_default_icon()
    
    def _create_default_icon(self):
        """Create and set a default icon programmatically"""
        try:
            # Create icon image
            size = 64
            img = Image.new('RGBA', (size, size), (10, 10, 10, 255))
            draw = ImageDraw.Draw(img)
            
            # Draw cyber symbol
            margin = 8
            draw.rectangle([margin, margin, size-margin, size-margin], 
                          outline=(0, 255, 65), width=3)
            draw.line([size//2, margin+5, size//2, size-margin-5], 
                     fill=(255, 0, 255), width=3)
            draw.line([margin+5, size//2, size-margin-5, size//2], 
                     fill=(0, 212, 255), width=3)
            
            # Convert to PhotoImage
            self.default_icon = ImageTk.PhotoImage(img.resize((32, 32)))
            self.app.iconphoto(True, self.default_icon)
            print("[Icon] Default icon created")
            
        except Exception as e:
            print(f"[Icon] Default icon failed: {e}")
    
    def set_taskbar_icon(self):
        """Set taskbar icon (Windows only)"""
        try:
            if sys.platform == 'win32':
                # Change app ID for custom taskbar icon
                myappid = 'cyberfile.app.v2.7'
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
                print("[Icon] Taskbar icon configured")
        except Exception as e:
            print(f"[Icon] Taskbar error: {e}")
    
    def create_tray_icon(self, icon_name="hacking.png"):
        """Create system tray icon"""
        if not PYSTRAY_AVAILABLE:
            print("[Icon] PyStray not available, skipping tray icon")
            return None
        
        try:
            icon_path = self.get_icon_path(icon_name)
            
            # If .ico not found, try .png
            if not os.path.exists(icon_path):
                icon_path = icon_path.replace('.ico', '.png')
            
            if not os.path.exists(icon_path):
                # Create default tray icon
                img = Image.new('RGBA', (64, 64), (10, 10, 10, 255))
                draw = ImageDraw.Draw(img)
                draw.rectangle([8, 8, 56, 56], outline=(0, 255, 65), width=3)
            else:
                img = Image.open(icon_path).resize((64, 64))
            
            menu = pystray.Menu(
                pystray.MenuItem("🔓 Show", self.show_app),
                pystray.MenuItem("⏸ Pause", self.toggle_pause),
                pystray.MenuItem("⏹ Exit", self.quit_app)
            )
            
            tray = pystray.Icon(
                "cyberfile",
                img,
                "Cyber-File v2.7 - Monitoring",
                menu
            )
            
            threading.Thread(target=tray.run, daemon=True).start()
            state.tray_icon = tray
            self.icons['tray'] = tray
            print("[Icon] Tray icon created")
            return tray
            
        except Exception as e:
            print(f"[Icon] Tray error: {e}")
            return None
    
    def show_app(self):
        """Show main window from tray"""
        self.app.deiconify()
        self.app.lift()
        self.app.focus_force()
    
    def toggle_pause(self):
        """Toggle pause from tray"""
        self.app.toggle_pause()
    
    def quit_app(self):
        """Quit from tray"""
        if state.tray_icon:
            state.tray_icon.stop()
        self.app.quit()

# ================= ALERT SYSTEM =================
def send_alert(message, event_type):
    if state.admin_paused:
        return
    if state.alert_method == "telegram" and REQUESTS_AVAILABLE and state.telegram_token and state.telegram_chat_id:
        try:
            url = f"https://api.telegram.org/bot{state.telegram_token}/sendMessage"
            data = {
                'chat_id': state.telegram_chat_id,
                'text': message
            }
            requests.post(url, data=data, timeout=10)
        except Exception as e:
            print(f"[Telegram Error] {e}")

# ================= FILE MONITOR =================
class FileMonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and not state.admin_paused:
            self.log_event("created", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory and not state.admin_paused:
            self.log_event("deleted", event.src_path)

    def on_modified(self, event):
        if not event.is_directory and not state.admin_paused:
            self.log_event("modified", event.src_path)

    def on_moved(self, event):
        if not event.is_directory and not state.admin_paused:
            self.log_event("moved", event.src_path, event.dest_path)

    def log_event(self, event_type, path, dest=None):
        event_data = {
            'time': datetime.now().strftime("%H:%M:%S"),
            'type': event_type,
            'path': path,
            'dest': dest
        }
        state.events.append(event_data)
        state.stats[event_type] += 1

        if hasattr(app, 'event_frame'):
            app.event_frame.add_event(event_data)
        if hasattr(app, 'stats_frame'):
            app.stats_frame.update_stats()

        if state.tray_icon:
            total = sum(state.stats.values())
            state.tray_icon.title = f"Cyber-File - {total} events detected"

        msg = f"🚨 {event_type.upper()}: {os.path.basename(path)}"
        threading.Thread(target=send_alert, args=(msg, event_type), daemon=True).start()

# ================= CUSTOM WIDGETS =================
class StatCard(ctk.CTkFrame):
    def __init__(self, parent, title, color, icon, **kwargs):
        super().__init__(parent, fg_color=COLORS['bg_card'], corner_radius=15, **kwargs)
        self.color = color
        self.count = 0

        self.border_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=15)
        self.border_frame.pack(fill="both", expand=True, padx=2, pady=2)

        ctk.CTkLabel(self.border_frame, text=icon, font=("Segoe UI", 32),
                     text_color=color).pack(pady=(15, 5))
        ctk.CTkLabel(self.border_frame, text=title, font=("Segoe UI", 12, "bold"),
                     text_color=COLORS['text_secondary']).pack()

        self.count_label = ctk.CTkLabel(self.border_frame, text="0",
                                        font=("Segoe UI", 36, "bold"), text_color=color)
        self.count_label.pack(pady=(5, 15))

        self.progress = ctk.CTkProgressBar(self.border_frame, width=120, height=6,
                                           corner_radius=3, progress_color=color,
                                           fg_color=COLORS['bg_secondary'])
        self.progress.pack(pady=(0, 15))
        self.progress.set(0)

    def update_count(self, count, percentage):
        self.count = count
        self.count_label.configure(text=str(count))
        self.progress.set(percentage / 100)
        self.animate_pulse()

    def animate_pulse(self):
        def pulse():
            for _ in range(3):
                self.border_frame.configure(fg_color=self.color + "30")
                time.sleep(0.1)
                self.border_frame.configure(fg_color="transparent")
                time.sleep(0.1)
        threading.Thread(target=pulse, daemon=True).start()


class EventItem(ctk.CTkFrame):
    def __init__(self, parent, event_data, **kwargs):
        super().__init__(parent, fg_color=COLORS['bg_secondary'], corner_radius=8, height=60 , **kwargs)
        self.pack_propagate(False)
        event_type = event_data['type']
        style = EVENT_STYLES[event_type]

        ctk.CTkFrame(self, width=4, fg_color=style['color'],
                     corner_radius=2).pack(side="left", fill="y")

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="x", expand=False, padx=10, pady=3)

        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x")

        ctk.CTkLabel(header, text=style['icon'], font=("Segoe UI", 14),
                     text_color=style['color']).pack(side="left")
        ctk.CTkLabel(header, text=style['name'], font=("Segoe UI", 11, "bold"),
                     text_color=style['color']).pack(side="left", padx=(5, 0))
        ctk.CTkLabel(header, text=event_data['time'], font=("Segoe UI", 10),
                     text_color=COLORS['text_secondary']).pack(side="right")

        path = event_data['path']
        if len(path) > 60:
            path = "..." + path[-57:]
        ctk.CTkLabel(content, text=path, font=("Consolas", 10),
                     text_color=COLORS['text'], wraplength=420,
                     anchor="w").pack(anchor="w", pady=(2, 0))


class AnimatedButton(ctk.CTkButton):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, corner_radius=12, font=("Segoe UI", 14, "bold"),
                         height=45, **kwargs)

# ================= MAIN APPLICATION =================
class CyberFileApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CYBER-FILE v2.0")
        self.geometry("1200x800")
        self.configure(fg_color=COLORS['bg'])
        self.minsize(900, 600)

        # Initialize Icon Manager - SET ICON FIRST (before window shows)
        self.icon_manager = IconManager(self)
        
        # Set window icon (try multiple formats)
        self.icon_manager.set_window_icon("hacking.ico")  # Windows
        # OR self.icon_manager.set_window_icon("hacking.png")  # Linux/Mac
        
        # Set taskbar icon
        self.icon_manager.set_taskbar_icon()
        
        # Create tray icon
        self.icon_manager.create_tray_icon("hacking.png")

        # Background Image
        try:
            bg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bb")
            if os.path.exists(bg_path):
                bg_img = Image.open(bg_path).resize((1200, 800))
                self._bg_ctk = ctk.CTkImage(bg_img, size=(1200, 800))
                self._bg_lbl = ctk.CTkLabel(self, image=self._bg_ctk, text="")
                self._bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)
                self._bg_lbl.lower()
        except Exception as e:
            print(f"[Background] {e}")

        # Build UI
        self.create_header()
        self.create_stats_section()
        self.create_main_content()
        self.create_control_panel()

        # Start timers
        self.after(1000, self.update_timer)
        self.check_admin_file()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_header(self):
        self.header = ctk.CTkFrame(self, fg_color="transparent", height=80)
        self.header.pack(fill="x", padx=20, pady=(20, 10))
        self.header.pack_propagate(False)

        title_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        title_frame.pack(side="left")

        ctk.CTkLabel(title_frame, text="⚡ CYBER-FILE",
                     font=("Segoe UI", 28, "bold"),
                     text_color=COLORS['accent']).pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Real-Time File Monitor v2.7",
                     font=("Segoe UI", 12),
                     text_color=COLORS['text_secondary']).pack(anchor="w")

        self.status_frame = ctk.CTkFrame(self.header, fg_color=COLORS['bg_card'],
                                         corner_radius=20)
        self.status_frame.pack(side="right", padx=10)

        self.status_dot = ctk.CTkLabel(self.status_frame, text="●",
                                       font=("Segoe UI", 20),
                                       text_color=COLORS['success'])
        self.status_dot.pack(side="left", padx=(15, 5), pady=10)

        self.status_text = ctk.CTkLabel(self.status_frame, text="ACTIVE",
                                        font=("Segoe UI", 12, "bold"),
                                        text_color=COLORS['success'])
        self.status_text.pack(side="right", padx=(5, 15), pady=10)

        self.runtime_label = ctk.CTkLabel(self.header, text="00:00:00",
                                          font=("Consolas", 16),
                                          text_color=COLORS['cyan'])
        self.runtime_label.pack(side="right", padx=20)

    def create_stats_section(self):
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(fill="x", padx=20, pady=10)

        self.stat_cards = {}
        for i, event in enumerate(['created', 'deleted', 'modified', 'moved']):
            style = EVENT_STYLES[event]
            card = StatCard(self.stats_frame, style['name'], style['color'], style['icon'])
            card.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")
            self.stats_frame.grid_columnconfigure(i, weight=1)
            self.stat_cards[event] = card

        self.stats_frame.update_stats = self.update_stats

    def update_stats(self):
        total = sum(state.stats.values()) or 1
        for event, card in self.stat_cards.items():
            count = state.stats[event]
            card.update_count(count, (count / total) * 100)

    def create_main_content(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Events panel
        self.events_panel = ctk.CTkFrame(self.main_frame, fg_color=COLORS['bg_card'],
                                         corner_radius=15)
        self.events_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        events_header = ctk.CTkFrame(self.events_panel, fg_color="transparent")
        events_header.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(events_header, text="📊 LIVE EVENTS",
                     font=("Segoe UI", 16, "bold"),
                     text_color=COLORS['text']).pack(side="left")

        self.event_count = ctk.CTkLabel(events_header, text="0 events",
                                        font=("Segoe UI", 12),
                                        text_color=COLORS['text_secondary'])
        self.event_count.pack(side="right")

        self.events_container = ctk.CTkScrollableFrame(self.events_panel,
                                                       fg_color="transparent",
                                                       corner_radius=0)
        self.events_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.event_frame = self
        self.event_frame.add_event = self.add_event

        # Directories panel
        self.dirs_panel = ctk.CTkFrame(self.main_frame, fg_color=COLORS['bg_card'],
                                       corner_radius=15, width=300)
        self.dirs_panel.pack(side="right", fill="y", padx=(10, 0))
        self.dirs_panel.pack_propagate(False)

        dirs_header = ctk.CTkFrame(self.dirs_panel, fg_color="transparent")
        dirs_header.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(dirs_header, text="👁 WATCHED",
                     font=("Segoe UI", 16, "bold"),
                     text_color=COLORS['text']).pack(side="left")

        ctk.CTkButton(dirs_header, text="+", width=30, height=30, corner_radius=8,
                      font=("Segoe UI", 16, "bold"),
                      fg_color=COLORS['accent'],
                      hover_color=COLORS['accent'] + "80",
                      command=self.add_directory).pack(side="right")

        self.dirs_list = ctk.CTkScrollableFrame(self.dirs_panel, fg_color="transparent",
                                                corner_radius=0)
        self.dirs_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def add_event(self, event_data):
        item = EventItem(self.events_container, event_data)
        item.pack(fill="x", expand=False, pady=1)
        self.event_count.configure(text=f"{len(state.events)} events")
        self.events_container._parent_canvas.yview_moveto(0)

    def add_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path and dir_path not in state.watched_dirs:
            state.watched_dirs.append(dir_path)
            self.update_dirs_list()
            self.start_monitoring_dir(dir_path)

    def update_dirs_list(self):
        for w in self.dirs_list.winfo_children():
            w.destroy()
        for i, dir_path in enumerate(state.watched_dirs, 1):
            f = ctk.CTkFrame(self.dirs_list, fg_color=COLORS['bg_secondary'], corner_radius=8)
            f.pack(fill="x", pady=2)
            ctk.CTkLabel(f, text=f"{i}.", font=("Segoe UI", 12, "bold"),
                         text_color=COLORS['accent'], width=30).pack(side="left", padx=10, pady=8)
            ctk.CTkLabel(f, text=dir_path, font=("Consolas", 10),
                         text_color=COLORS['text']).pack(side="left", padx=(0, 10), pady=8)

    def create_control_panel(self):
        self.control_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_card'],
                                          corner_radius=15, height=110)
        self.control_frame.pack(fill="x", padx=20, pady=(10, 20))
        self.control_frame.pack_propagate(False)

        # Left: Alert method + Telegram credentials
        left = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        left.pack(side="left", padx=15, pady=10)

        # Row 1 — Alert method selector
        row1 = ctk.CTkFrame(left, fg_color="transparent")
        row1.pack(anchor="w")

        ctk.CTkLabel(row1, text="Alert Method:",
                     font=("Segoe UI", 12),
                     text_color=COLORS['text_secondary']).pack(side="left", padx=(0, 8))

        self.method_menu = ctk.CTkOptionMenu(
            row1, values=["Telegram", "None"],
            command=self.change_alert_method,
            width=120, font=("Segoe UI", 12)
        )
        self.method_menu.pack(side="left")
        self.method_menu.set("Telegram")

        # Row 2 — Telegram Chat ID
        row2 = ctk.CTkFrame(left, fg_color="transparent")
        row2.pack(anchor="w", pady=(6, 0))

        ctk.CTkLabel(row2, text="📱 Chat ID:",
                     font=("Segoe UI", 12),
                     text_color=COLORS['text_secondary']).pack(side="left", padx=(0, 8))

        self.chat_id_entry = ctk.CTkEntry(
            row2, width=170, height=32, corner_radius=8,
            font=("Consolas", 12),
            placeholder_text="123456789",
            fg_color=COLORS['bg_secondary'],
            border_color=COLORS['accent']
        )
        self.chat_id_entry.pack(side="left")

        ctk.CTkButton(
            row2, text="✔ Save", width=70, height=32, corner_radius=8,
            font=("Segoe UI", 12, "bold"),
            fg_color=COLORS['success'],
            hover_color=COLORS['success'] + "80",
            command=self.save_telegram_config
        ).pack(side="left", padx=(6, 0))

        # Row 3 — Telegram Bot Token
        row3 = ctk.CTkFrame(left, fg_color="transparent")
        row3.pack(anchor="w", pady=(6, 0))

        ctk.CTkLabel(row3, text="🔑 Token:",
                     font=("Segoe UI", 11),
                     text_color=COLORS['text_secondary']).pack(side="left")

        self.token_entry = ctk.CTkEntry(
            row3, width=260, height=28, corner_radius=8,
            font=("Consolas", 10),
            placeholder_text="your_bot_token_here",
            fg_color=COLORS['bg_secondary'],
            border_color=COLORS['border'],
            show="●"
        )
        self.token_entry.pack(side="left", padx=(4, 0))

        # Right: action buttons
        buttons_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=15, pady=15)

        self.pause_btn = AnimatedButton(
            buttons_frame, text="⏸ Pause",
            fg_color=COLORS['warning'],
            hover_color=COLORS['warning'] + "80",
            command=self.toggle_pause
        )
        self.pause_btn.pack(side="left", padx=5)

        AnimatedButton(
            buttons_frame, text="🔐 Admin",
            fg_color=COLORS['accent'],
            hover_color=COLORS['accent'] + "80",
            command=self.show_admin
        ).pack(side="left", padx=5)

        AnimatedButton(
            buttons_frame, text="🗕 Tray",
            fg_color=COLORS['cyan'],
            hover_color=COLORS['cyan'] + "80",
            command=self.minimize_to_tray
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons_frame, text="⏹ Stop",
            width=100, height=45, corner_radius=12,
            font=("Segoe UI", 14, "bold"),
            fg_color=COLORS['danger'],
            hover_color=COLORS['danger'] + "80",
            command=self.quit
        ).pack(side="left", padx=5)

    def save_telegram_config(self):
        chat_id = self.chat_id_entry.get().strip()
        token = self.token_entry.get().strip()

        if chat_id and token:
            state.telegram_chat_id = chat_id
            state.telegram_token = token
            state.alert_method = "telegram"
            self.chat_id_entry.configure(border_color=COLORS['success'])
            self.token_entry.configure(border_color=COLORS['success'])
            self.method_menu.set("Telegram")
            messagebox.showinfo("Telegram ✅", f"Alerts will be sent to Chat ID: {chat_id}")
        else:
            self.chat_id_entry.configure(border_color=COLORS['danger'])
            messagebox.showerror("Invalid Config", "Enter both Chat ID and Bot Token")

    def change_alert_method(self, method):
        state.alert_method = method.lower()

    def toggle_pause(self):
        state.admin_paused = not state.admin_paused
        if state.admin_paused:
            self.pause_btn.configure(text="▶ Resume", fg_color=COLORS['success'])
            self.status_dot.configure(text_color=COLORS['warning'])
            self.status_text.configure(text="PAUSED", text_color=COLORS['warning'])
            if state.tray_icon:
                state.tray_icon.title = "Cyber-File - PAUSED"
        else:
            self.pause_btn.configure(text="⏸ Pause", fg_color=COLORS['warning'])
            self.status_dot.configure(text_color=COLORS['success'])
            self.status_text.configure(text="ACTIVE", text_color=COLORS['success'])
            if state.tray_icon:
                state.tray_icon.title = "Cyber-File - ACTIVE"

    def minimize_to_tray(self):
        if state.tray_icon:
            self.withdraw()
            state.tray_icon.notify("Cyber-File", "Running in background. Click tray icon to restore.")
        else:
            messagebox.showinfo("Tray", "System tray not available. Install pystray: pip install pystray")

    def show_admin(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Admin Access")
        dialog.geometry("400x200")
        dialog.configure(fg_color=COLORS['bg'])

        ctk.CTkLabel(dialog, text="🔐 Enter Admin Code",
                     font=("Segoe UI", 18, "bold"),
                     text_color=COLORS['text']).pack(pady=20)

        entry = ctk.CTkEntry(dialog, width=200, height=40, corner_radius=10,
                             font=("Consolas", 16), show="●")
        entry.pack(pady=10)
        entry.focus()

        def check_code():
            if entry.get() == "1234":
                dialog.destroy()
                self.enter_admin_mode()
            else:
                entry.configure(border_color=COLORS['danger'])

        ctk.CTkButton(dialog, text="Unlock", width=200, height=40, corner_radius=10,
                      font=("Segoe UI", 14, "bold"),
                      fg_color=COLORS['accent'],
                      command=check_code).pack(pady=10)

    def enter_admin_mode(self):
        state.admin_paused = True
        self.pause_btn.configure(text="▶ Resume", fg_color=COLORS['success'])

        dialog = ctk.CTkToplevel(self)
        dialog.title("Admin Mode")
        dialog.geometry("300x150")
        dialog.configure(fg_color=COLORS['bg'])

        label = ctk.CTkLabel(dialog, text="Hiding in 4...",
                             font=("Segoe UI", 24, "bold"),
                             text_color=COLORS['accent'])
        label.pack(expand=True)

        def countdown(n=4):
            if n > 0:
                label.configure(text=f"Hiding in {n}...")
                self.after(1000, lambda: countdown(n-1))
            else:
                dialog.destroy()
                self.hide_console()
                state.admin_paused = False
                self.pause_btn.configure(text="⏸ Pause", fg_color=COLORS['warning'])

        countdown()

    def hide_console(self):
        try:
            ctypes.windll.user32.ShowWindow(
                ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass

    def start_monitoring_dir(self, path):
        if not state.monitoring:
            state.monitoring = True
            state.start_time = datetime.now()

        handler = FileMonitorHandler()
        observer = Observer()
        observer.schedule(handler, path, recursive=True)
        observer.start()
        state.observers.append(observer)

    def update_timer(self):
        if state.start_time and not state.admin_paused:
            elapsed = datetime.now() - state.start_time
            h, rem = divmod(elapsed.seconds, 3600)
            m, s = divmod(rem, 60)
            self.runtime_label.configure(text=f"{h:02d}:{m:02d}:{s:02d}")
        self.after(1000, self.update_timer)

    def check_admin_file(self):
        if os.path.exists("admin.unlock"):
            self.show_admin()
            os.remove("admin.unlock")
        self.after(1000, self.check_admin_file)

    def on_closing(self):
        state.monitoring = False
        for obs in state.observers:
            obs.stop()
        for obs in state.observers:
            obs.join()
        if state.tray_icon:
            state.tray_icon.stop()
        self.destroy()

# ================= MAIN =================
if __name__ == "__main__":
    app = CyberFileApp()
    app.mainloop()