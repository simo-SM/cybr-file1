#========================================================
#===================| CYBER-FILE  |===================
#========================================================

import time
from watchdog.observers import Observer 
from watchdog.events import FileSystemEventHandler
import termcolor

#!=========start function=================

def created(event):
    print("="* 50)
    print(termcolor.colored(f"\033[31mfile {termcolor.colored(f'[ {event.src_path} ]', 'green')}\033[31m created", 'yellow'))

def deleted(event):
    print(termcolor.colored(f'\033[31mfile {termcolor.colored(f'[ {event.src_path} ]', 'green')}\033[31m deleted','red'))

def modified(event):
    print(f'\033[33mfile {termcolor.colored(f'[ {event.src_path} ]', 'green')}\033[33m modified ')

def moved(event):
    print("\u001b[0;33mfile" + f" {termcolor.colored(f'[ {event.src_path} ]', 'green')}"+"\u001b[0;33mmoved" + f" {termcolor.colored(f'[ {event.src_path} ]', 'blue')}")

#!=========end function=================
if _name_ == "_main_":
    
    print('''
\033[33m===================================================================================


\033[32m              _                            _           __ _ _      
\033[32m__      _____| | ___ ___  _ __ ___   ___  | |_ ___    / _(_) | ___ 
\033[32m\ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | |_| | |/ _ \,
\033[32m \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) | |  _| | |  __/
\033[32m  \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  |_| |_|_|\___|
\033[32m _ __ ___   ___  _ __ (_) |_ ___  _ __(_)_ __   __ _               
\033[32m| '_ ` _ \ / _ \| '_ \| | __/ _ \| '__| | '_ \ / _` |              
\033[32m| | | | | | (_) | | | | | || (_) | |  | | | | | (_| |              
\033[32m|_| |_| |_|\___/|_| |_|_|\__\___/|_|  |_|_| |_|\__, |              
                                               |___/                   
\033[31m    _______
\033[31m   /      //
\033[31m  /      //   
\033[31m /______//
\033[31m(______(/


          ''')
    print("\033[33m===================================================================================")

    
    # إضافة قائمة تحتوي على مسارات الملفات التي تريد مراقبتها
    paths = input("Please enter the file paths separated by commas [EX: C:\\Users\\Admin\\Documents,C:\\Users\\Admin\\Pictures]: ").split(',')
    
    evo = FileSystemEventHandler()
    evo.on_created = created
    evo.on_deleted = deleted
    evo.on_modified = modified
    evo.on_moved = moved

    # إنشاء قائمة للمراقبين
    observers = []

    # بدء المراقبة لكل مسار
    for path in paths:
        observer = Observer()
        observer.schedule(evo, path.strip(), recursive=True)
        observers.append(observer)
        observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:  # عند الضغط على Ctrl + C
        for observer in observers:
            observer.stop()

    for observer in observers:
        observer.join()
