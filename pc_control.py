import os
import subprocess
import ctypes
import pyautogui
import psutil
from PIL import ImageGrab
import win32api
import win32con
import win32gui
import win32process
from datetime import datetime

def take_screenshot():
    """Take a screenshot and return the file path"""
    screenshot = ImageGrab.grab()
    filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(os.path.expanduser('~'), 'Pictures', filename)
    screenshot.save(filepath)
    return filepath

def get_process_list():
    """Get list of running processes with details"""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            process = proc.info
            process['cpu_percent'] = proc.cpu_percent()
            processes.append(process)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)

def kill_process(pid):
    """Kill a process by PID"""
    try:
        process = psutil.Process(pid)
        process.kill()
        return True, "Process terminated successfully"
    except psutil.NoSuchProcess:
        return False, "Process not found"
    except psutil.AccessDenied:
        return False, "Access denied"

def get_system_info():
    """Get detailed system information"""
    cpu = psutil.cpu_percent(interval=1, percpu=True)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Get network information
    network = psutil.net_io_counters()
    
    # Get battery information if available
    battery = None
    if hasattr(psutil, "sensors_battery"):
        battery = psutil.sensors_battery()
    
    return {
        "cpu": {
            "total": sum(cpu) / len(cpu),
            "per_cpu": cpu
        },
        "memory": {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent,
            "used": memory.used
        },
        "disk": {
            "total": disk.total,
            "free": disk.free,
            "used": disk.used,
            "percent": disk.percent
        },
        "network": {
            "bytes_sent": network.bytes_sent,
            "bytes_recv": network.bytes_recv
        },
        "battery": battery
    }

def set_volume(volume_level):
    """Set system volume (0-100)"""
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        # Convert volume level from 0-100 to -65.25-0
        volume_scalar = float(volume_level) / 100.0
        volume.SetMasterVolumeLevelScalar(volume_scalar, None)
        return True, f"Volume set to {volume_level}%"
    except Exception as e:
        return False, f"Failed to set volume: {str(e)}"

def system_action(action):
    """Perform system actions"""
    try:
        if action == "shutdown":
            os.system("shutdown /s /t 1")
            return True, "System shutting down..."
        elif action == "restart":
            os.system("shutdown /r /t 1")
            return True, "System restarting..."
        elif action == "sleep":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return True, "System going to sleep..."
        elif action == "lock":
            ctypes.windll.user32.LockWorkStation()
            return True, "System locked"
        return False, "Invalid action"
    except Exception as e:
        return False, f"Action failed: {str(e)}"

def get_display_info():
    """Get information about displays"""
    displays = []
    try:
        for i in range(win32api.GetSystemMetrics(win32con.SM_CMONITORS)):
            monitor = win32api.EnumDisplayMonitors(None, None)[i]
            info = win32api.GetMonitorInfo(monitor[0])
            displays.append({
                "device": info["Device"],
                "resolution": (
                    info["Monitor"][2] - info["Monitor"][0],
                    info["Monitor"][3] - info["Monitor"][1]
                ),
                "work_area": info["Work"]
            })
        return displays
    except Exception as e:
        return []

def search_files(directory, pattern, max_results=50):
    """Search for files in directory"""
    results = []
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if pattern.lower() in file.lower():
                    file_path = os.path.join(root, file)
                    try:
                        stats = os.stat(file_path)
                        results.append({
                            "name": file,
                            "path": file_path,
                            "size": stats.st_size,
                            "modified": datetime.fromtimestamp(stats.st_mtime)
                        })
                        if len(results) >= max_results:
                            return results
                    except:
                        continue
    except Exception as e:
        pass
    return results
