#!/usr/bin/env python3
# ========================================================
# ===================| CYBER-FILE v2.7 |==================
# ===== Real-Time File Monitor + Multi-Alert System ======
# ========================================================

import os, sys, time, threading, ctypes, json
from datetime import datetime
from collections import deque
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Rich imports
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from rich import box
from rich.rule import Rule
from rich.columns import Columns
from dotenv import load_dotenv
console = Console()
load_dotenv()
# ================= CONFIG =================
# CHOOSE YOUR ALERT METHOD
ALERT_METHOD = "sound"  # Options: "whatsapp", "telegram", "sound", "log", "none"

# WhatsApp (Twilio) - LIMITED TO 50/DAY
TWILIO_SID = os.getenv("TWILIO_SID") # Get from Twilio Console
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN") # Get from Twilio Console
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")   # Twilio Sandbox Number
user_whatsapp = None

# Telegram (FREE - NO LIMIT)  RECOMMENDED
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") # Get from @BotFather
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") # Get from @userinfobot

# ================= NEON THEME =================
THEME = {
    'cyan': '#00d4ff',
    'green': '#00ff88',
    'red': '#ff3366',
    'yellow': '#ffcc00',
    'blue': '#0099ff',
    'magenta': '#ff00ff',
    'text': '#e6edf3',
    'text_dim': '#7d8590',
    'border': '#30363d'
}

EVENT_COLORS = {
    'created': THEME['green'],
    'deleted': THEME['red'],
    'modified': THEME['yellow'],
    'moved': THEME['blue']
}

EVENT_ICONS = {
    'created': '✚',
    'deleted': '✖',
    'modified': '✎',
    'moved': '➜'
}

ADMIN_PAUSED = False
ALERT_COOLDOWN = {}  # Prevent spam

# ================= ALERT SYSTEMS =================

def send_alert(message, event_type="info"):
    """Universal alert function"""
    global ALERT_COOLDOWN
    
    # Skip if admin paused
    if ADMIN_PAUSED:
        return
    
    # Cooldown check (no spam)
    now = time.time()
    if event_type in ALERT_COOLDOWN:
        if now - ALERT_COOLDOWN[event_type] < 5:  # 5 seconds min between alerts
            return
    ALERT_COOLDOWN[event_type] = now
    
    # Route to chosen method
    if ALERT_METHOD == "whatsapp":
        send_whatsapp(message)
    elif ALERT_METHOD == "telegram":
        send_telegram(message)
    elif ALERT_METHOD == "sound":
        play_sound_alert(event_type)
    elif ALERT_METHOD == "log":
        log_to_file(message)
    # "none" = silent

def send_whatsapp(message):
    """Twilio WhatsApp - LIMITED 50/DAY"""
    try:
        from twilio.rest import Client
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        client.messages.create(
            from_=TWILIO_NUMBER,
            to=f"whatsapp:{user_whatsapp}",
            body=message
        )
    except Exception as e:
        console.print(f"[{THEME['red']}]❌ WhatsApp Failed: {str(e)[:50]}...[/{THEME['red']}]")

def send_telegram(message):
    """Telegram Bot - FREE NO LIMIT """
    try:
        import urllib.request
        import urllib.parse
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }).encode()
        
        urllib.request.urlopen(url, data=data, timeout=5)
    except Exception as e:
        console.print(f"[{THEME['red']}]❌ Telegram Failed: {e}[/{THEME['red']}]")

def play_sound_alert(event_type):
    """Beep sound - NO INTERNET NEEDED"""
    try:
        import winsound
        frequencies = {
            'created': 1000,  # High beep
            'deleted': 400,   # Low beep
            'modified': 800,  # Mid beep
            'moved': 600      # Low-mid beep
        }
        freq = frequencies.get(event_type, 800)
        winsound.Beep(freq, 200)  # 200ms beep
    except:
        # Linux/Mac alternative
        try:
            print('\a')  # Bell character
        except:
            pass

def log_to_file(message):
    """Save to local log file"""
    try:
        with open("cyberfile_alerts.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()}: {message}\n")
    except:
        pass

# ================= ADMIN FUNCTIONS =================
ADMIN_CODE = "1234"  # Change this code for admin access

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def hide_console():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

def show_console():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
    except:
        pass

def admin_unlock(monitor):
    """Admin mode: Pause → Code → Hide → Resume"""
    global ADMIN_PAUSED
    
    if not os.path.exists("admin.unlock"):
        return False
    
    ADMIN_PAUSED = True
    monitor.running = False
    
    show_console()
    
    console.print(f"\n[{THEME['magenta']}]🔐 ADMIN MODE ACTIVATED[/{THEME['magenta']}]")
    console.print(f"[{THEME['yellow']}]⏸️  Monitoring PAUSED[/{THEME['yellow']}]")
    console.print(f"[{THEME['text_dim']}]───────────────────────────────[/{THEME['text_dim']}]\n")
    
    code = console.input(f"[{THEME['magenta']}]Enter Admin Code: [/{THEME['magenta']}]")
    
    if code == ADMIN_CODE:
        console.print(f"\n[{THEME['green']}]✅ Access Granted[/{THEME['green']}]")
        console.print(f"[{THEME['cyan']}]💤 Hiding in 4s...[/{THEME['cyan']}]")
        
        for i in range(4, 0, -1):
            console.print(f"[{THEME['cyan']}]   {i}...[/{THEME['cyan']}]")
            time.sleep(1)
        
        console.print(f"[{THEME['green']}] Hidden! Resuming...[/{THEME['green']}]")
        time.sleep(0.5)
        hide_console()
        
        os.remove("admin.unlock")
        ADMIN_PAUSED = False
        monitor.running = True
        return True
    else:
        console.print(f"\n[{THEME['red']}]❌ Wrong Code![/{THEME['red']}]")
        os.remove("admin.unlock")
        ADMIN_PAUSED = False
        monitor.running = True
        time.sleep(2)
        return False

# ================= MONITOR =================
class CyberFileMonitor:
    def __init__(self):
        self.events = deque(maxlen=100)
        self.stats = {'created': 0, 'deleted': 0, 'modified': 0, 'moved': 0}
        self.active_monitors = []
        self.start_time = datetime.now()
        self.lock = threading.Lock()
        self.running = True

    def generate_banner(self):
        banner = r"""
             ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗██╗██╗     ███████╗
            ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██║██║     ██╔════╝
            ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝█████╗  ██║██║     █████╗
            ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██╔══╝  ██║██║     ██╔══╝
            ╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║     ██║███████╗███████╗
             ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝
                                Real-Time File Monitor v2.0
        """
        return Panel(
            Align.center(Text(banner, style="bold orange1")),
            box=box.DOUBLE,
            border_style="orange1"
        )

    def get_elapsed(self):
        elapsed = datetime.now() - self.start_time
        hours, rem = divmod(elapsed.seconds, 3600)
        minutes, seconds = divmod(rem, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def create_slider_stats(self):
        total = sum(self.stats.values()) or 1
        panels = []
        
        for event_type in ['created', 'deleted', 'modified', 'moved']:
            count = self.stats[event_type]
            percentage = (count / total) * 100
            color = EVENT_COLORS[event_type]
            icon = EVENT_ICONS[event_type]
            name = event_type.upper()
            
            bar_width = 15
            filled = int((percentage / 100) * bar_width)
            bar = "█" * filled + "░" * (bar_width - filled)
            
            content = f"""[{color}]{icon}[/{color}] {name}
[{color}]{count:>4}[/{color}] [{THEME['text_dim']}]│[/{THEME['text_dim']}] [{color}]{bar}[/{color}] [{THEME['text_dim']}]%{percentage:.1f}[/{THEME['text_dim']}]"""
            
            panel = Panel(
                content,
                border_style=color,
                box=box.SQUARE,
                padding=(1, 2)
            )
            panels.append(panel)
        
        return Columns(panels, equal=True, expand=True)

    def create_events_panel(self):
        table = Table(expand=True, show_header=True, header_style=f"bold {THEME['cyan']}")
        table.add_column("Time", width=10, style=THEME['text_dim'])
        table.add_column("Event", width=12)
        table.add_column("Path", style=THEME['text'])
        
        with self.lock:
            recent = list(self.events)[-20:][::-1]
        
        if not recent:
            status = "ADMIN PAUSED" if ADMIN_PAUSED else "Waiting..."
            color = THEME['red'] if ADMIN_PAUSED else THEME['cyan']
            table.add_row("--:--:--", f"[{color}]{status}[/]", "Monitor active...")
        
        for e in recent:
            event_type = e['type']
            color = EVENT_COLORS.get(event_type, THEME['text'])
            icon = EVENT_ICONS.get(event_type, '•')
            
            path = e['path']
            if e['type'] == "moved" and e.get('dest'):
                path = f"{path} -> {e['dest']}"
            if len(path) > 45:
                path = "..." + path[-42:]
            
            table.add_row(
                e['time'],
                Text(f"{icon} {event_type.upper()}", style=f"bold {color}"),
                path
            )
        
        return Panel(
            table, 
            title=f"[{THEME['cyan']}]⚡ LIVE EVENTS[/{THEME['cyan']}]",
            border_style=THEME['cyan'],
            box=box.ROUNDED
        )

    def create_monitors_panel(self):
        table = Table(show_header=False, box=None)
        table.add_column(style=f"bold {THEME['green']}", width=4)
        table.add_column(style=THEME['text'])
        
        for i, path in enumerate(self.active_monitors, 1):
            table.add_row(f"{i}.", path)
        
        # Alert method indicator
        alert_colors = {
            "whatsapp": THEME['green'],
            "telegram": THEME['blue'],
            "sound": THEME['yellow'],
            "log": THEME['text_dim'],
            "none": THEME['red']
        }
        alert_color = alert_colors.get(ALERT_METHOD, THEME['text'])
        
        return Panel(
            table,
            title=f"[{THEME['green']}]👁 WATCHED[/{THEME['green']}]",
            subtitle=f"[{alert_color}]● {ALERT_METHOD.upper()}[/{alert_color}]",
            border_style=THEME['green'],
            box=box.ROUNDED
        )

    def create_header_panel(self):
        if ADMIN_PAUSED:
            status = f"[{THEME['red']}]⏸️ ADMIN MODE[/{THEME['red']}]"
        else:
            status = f"[{THEME['green']}]● LIVE[/{THEME['green']}]" if self.running else f"[{THEME['red']}]○ STOPPED[/{THEME['red']}]"
        
        return Panel(
            f"{status}  Runtime: [{THEME['cyan']}]{self.get_elapsed()}[/{THEME['cyan']}]  Events: [{THEME['yellow']}]{sum(self.stats.values())}[/{THEME['yellow']}]",
            border_style=THEME['cyan'],
            box=box.ROUNDED
        )

    def create_footer_panel(self):
        mode = f"[{THEME['red']}]ADMIN[/{THEME['red']}]" if ADMIN_PAUSED else f"[{THEME['text_dim']}]Ctrl+C=Stop[/{THEME['text_dim']}]"
        return Panel(
            f"{mode} │ admin.unlock=Admin │ Alert: {ALERT_METHOD}",
            border_style=THEME['text_dim'],
            box=box.SQUARE
        )

    def log_event(self, event_type, path, dest=None):
        if ADMIN_PAUSED:
            return
            
        with self.lock:
            self.events.append({
                'time': datetime.now().strftime("%H:%M:%S"),
                'type': event_type,
                'path': path,
                'dest': dest
            })
            self.stats[event_type] += 1
        
        # Send alert
        color = EVENT_COLORS.get(event_type, THEME['text'])
        icon = EVENT_ICONS.get(event_type, '•')
        message = f"""🚨 Cyber-File Alert

{icon} {event_type.upper()}
📄 {path}
⏰ {datetime.now().strftime("%H:%M:%S")}"""
        
        threading.Thread(target=send_alert, args=(message, event_type), daemon=True).start()

    def on_created(self, event): 
        if not event.is_directory:
            self.log_event("created", event.src_path)
    
    def on_deleted(self, event): 
        if not event.is_directory:
            self.log_event("deleted", event.src_path)
    
    def on_modified(self, event): 
        if not event.is_directory:
            self.log_event("modified", event.src_path)
    
    def on_moved(self, event): 
        if not event.is_directory:
            self.log_event("moved", event.src_path, event.dest_path)

# ================= SETUP =================
def setup_directories(monitor):
    console.print(Rule("CONFIGURATION"))
    
    paths_input = console.input(f"[{THEME['cyan']}]Enter directories (comma separated): [/{THEME['cyan']}]")
    paths = [p.strip() for p in paths_input.split(",") if p.strip()]
    
    valid = [p for p in paths if os.path.isdir(p)]
    
    if not valid:
        console.print(f"[{THEME['red']}]❌ No valid directories[/{THEME['red']}]")
        sys.exit(1)
    
    monitor.active_monitors = valid
    console.print(f"[{THEME['green']}]✅ Monitoring {len(valid)} directories[/{THEME['green']}]")
    return valid

# ================= MAIN =================
def main():
    global user_whatsapp, ALERT_METHOD
    
    monitor = CyberFileMonitor()
    
    console.clear()
    console.print(monitor.generate_banner())
    
    # Choose alert method
    console.print(f"\n[{THEME['cyan']}]📢 Alert Methods:[/{THEME['cyan']}]")
    console.print(f"  [{THEME['green']}]1. WhatsApp[/{THEME['green']}] (Limited 50/day)")
    console.print(f"  [{THEME['blue']}]2. Telegram[/{THEME['blue']}] (FREE - Recommended)")
    console.print(f"  [{THEME['yellow']}]3. Sound[/{THEME['yellow']}] (Beep only)")
    console.print(f"  [{THEME['text_dim']}]4. Log File[/{THEME['text_dim']}]")
    console.print(f"  [{THEME['red']}]5. None[/{THEME['red']}] (Silent)\n")
    
    choice = console.input(f"[{THEME['cyan']}]Choose (1-5) or press Enter for [{ALERT_METHOD}]: [/{THEME['cyan']}]")
    
    methods = {"1": "whatsapp", "2": "telegram", "3": "sound", "4": "log", "5": "none"}
    if choice in methods:
        ALERT_METHOD = methods[choice]
    
    # Setup chosen method
    if ALERT_METHOD == "whatsapp":
        user_whatsapp = console.input(f"[{THEME['green']}]WhatsApp (+countrycode): [/{THEME['green']}]")
        console.print(f"[{THEME['yellow']}]⚠️ Limited 50 messages/day![/{THEME['yellow']}]")
    elif ALERT_METHOD == "telegram":
        console.print(f"[{THEME['blue']}]ℹ️  Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in code[/{THEME['blue']}]")
        console.print(f"[{THEME['cyan']}]   Get bot: @BotFather | Get ID: @userinfobot[/{THEME['cyan']}]")
    
    if not is_admin():
        hide_console()
    
    paths = setup_directories(monitor)
    
    event_handler = FileSystemEventHandler()
    event_handler.on_created = monitor.on_created
    event_handler.on_deleted = monitor.on_deleted
    event_handler.on_modified = monitor.on_modified
    event_handler.on_moved = monitor.on_moved
    
    observers = []
    for path in paths:
        obs = Observer()
        obs.schedule(event_handler, path, recursive=True)
        obs.start()
        observers.append(obs)
    
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="stats", size=7),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    
    layout["main"].split_row(
        Layout(name="events"),
        Layout(name="dirs", size=40)
    )
    
    try:
        with Live(layout, refresh_per_second=4):
            while True:
                if os.path.exists("admin.unlock"):
                    admin_unlock(monitor)
                
                if monitor.running:
                    layout["header"].update(monitor.create_header_panel())
                    layout["stats"].update(monitor.create_slider_stats())
                    layout["events"].update(monitor.create_events_panel())
                    layout["dirs"].update(monitor.create_monitors_panel())
                    layout["footer"].update(monitor.create_footer_panel())
                
                time.sleep(0.25)
                
    except KeyboardInterrupt:
        monitor.running = False
        for obs in observers:
            obs.stop()
        for obs in observers:
            obs.join()
        
        console.print(f"[{THEME['yellow']}]Monitor stopped[/{THEME['yellow']}]")

if __name__ == "__main__":
    main()