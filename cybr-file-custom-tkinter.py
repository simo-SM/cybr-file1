import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import Entry, messagebox, filedialog
from tkinter import scrolledtext
from PIL import Image, ImageTk  # لإضافة الصورة كخلفية

# Function to log messages in the text box with color
def log_message(message, color):
    text_box.config(state=tk.NORMAL)
    text_box.insert(tk.END, message + "\n", color)
    text_box.config(state=tk.DISABLED)
    text_box.see(tk.END)  # Scroll to the end of the text box

# Watchdog event handler functions
def created(event):
    log_message(f"file [ {event.src_path} ] created", "green")

def deleted(event):
    log_message(f"file [ {event.src_path} ] deleted", "red")

def modified(event):
    log_message(f"file [ {event.src_path} ] modified", "yellow")

def moved(event):
    log_message(f"file [ {event.src_path} ] moved to [ {event.dest_path} ]", "blue")

# Function to start observer for each folder in the list
def start_observer():
    global observers
    global is_running
    if not folder_paths:
        messagebox.showwarning("Warning", "Please select at least one folder before starting monitoring.")
        return
    
    if not is_running:
        observers = []  # قائمة لحفظ جميع المراقبين
        
        for path in folder_paths:
            evo = FileSystemEventHandler()
            evo.on_created = created
            evo.on_deleted = deleted
            evo.on_modified = modified
            evo.on_moved = moved

            observer = Observer()
            observer.schedule(evo, path, recursive=True)

            # Start the observer in a separate thread
            observer_thread = threading.Thread(target=observer.start)
            observer_thread.daemon = True
            observer_thread.start()
            
            observers.append(observer)  # أضف كل مراقب إلى القائمة
        
        is_running = True
        messagebox.showinfo("Observer", "Observers started!")
    else:
        messagebox.showinfo("Observer", "Observers are already running.")

# Function to stop all observers
def stop_observer():
    global observers
    global is_running
    if is_running:
        for observer in observers:
            observer.stop()
            observer.join()
        is_running = False
        messagebox.showinfo("Observer", "Observers stopped!")
    else:
        messagebox.showinfo("Observer", "Observers are not running.")

# Function to browse multiple folders
def browse_folder():
    global folder_paths
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_paths.append(folder_path)  # أضف المسار إلى القائمة
        log_message(f"Selected folder: {folder_path}", "blue")

# Creating the Tkinter window with background image
def create_gui():
    global text_box  # تعريف الـ text_box كمتغير عام للوصول إليه في باقي الدوال
    global folder_paths
    
    folder_paths = []  # قائمة لتخزين المسارات المختارة
    
    root = tk.Tk()
    root.title("Cyber File Monitor")
    root.geometry("700x700")  # قم بتعديل الأبعاد حسب الحاجة
    root.resizable(False, False)
    root.configure(bg="#1c1f1c")

    #===========imge is icon ======================
    img=tk.PhotoImage(file="image/grop-file.png")
    root.iconphoto(False,img)
    #===========imge is icon ======================

    # Label for title
    label = tk.Label(root, text="CYBER-FILE MONITOR", font=("Arial", 18), bg='#FFFFFF')
    label.pack(pady=10)

    # Load the background image
    background_image = Image.open("image/bg.jpeg")  # استبدل هذا بالمسار الصحيح للصورة

    # Create a label to hold the background image
    background_image = background_image.resize((700, 800))  # تغيير الحجم ليتناسب مع النافذة
    bg_image = ImageTk.PhotoImage(background_image)

    # Create a label to hold the background image
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1) 

    # Button to browse folder
    browse_button = tk.Button(root, text="Browse Folder", command=browse_folder, width=20, height=2, bg="#808080")
    browse_button.place(x=300, y=15)

    # Buttons to start and stop monitoring
    start_button = tk.Button(root, text="Start Monitoring", command=start_observer, width=20, height=2, bg="#00FF00")
    start_button.place(x=5, y=15)

    stop_button = tk.Button(root, text="Stop Monitoring", command=stop_observer, width=20, height=2, bg="#FF0000")
    stop_button.place(x=150, y=15)

    # Scrollable text box to display logs
    text_box = scrolledtext.ScrolledText(root, width=76, height=85, bg="black",font=("Arial",12), state=tk.DISABLED, wrap=tk.WORD)
    text_box.tag_config("red", foreground="red")
    text_box.tag_config("green", foreground="green")
    text_box.tag_config("yellow", foreground="yellow")
    text_box.tag_config("blue", foreground="blue")
    text_box.place(x=0, y=400)

    root.mainloop()

# Global variables to track observer state
observers = []
is_running = False
folder_paths = []

# Main execution starts here
create_gui()
