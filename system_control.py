import os
import psutil
import subprocess
import ctypes
from datetime import datetime, timedelta
import win32api
import win32con
import win32gui
import win32process
from PIL import ImageGrab
import pyautogui
import keyboard
import json

def take_screenshot():
    """Take a screenshot and return the file path"""
    try:
        # Create screenshots directory if it doesn't exist
        screenshots_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
            
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(screenshots_dir, filename)
        
        # Take screenshot
        screenshot = ImageGrab.grab()
        screenshot.save(filepath)
        
        # Return file path for sending
        return filepath
    except Exception as e:
        print(f"Screenshot error: {str(e)}")
        return None

def system_action(action):
    """Perform system actions"""
    try:
        if action == "shutdown":
            os.system("shutdown /s /t 1")
            return True, "System will shutdown in 1 second"
        elif action == "restart":
            os.system("shutdown /r /t 1")
            return True, "System will restart in 1 second"
        elif action == "sleep":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return True, "System going to sleep"
        elif action == "lock":
            ctypes.windll.user32.LockWorkStation()
            return True, "System locked"
        elif action == "vol_up":
            for _ in range(2):  # Press twice for more noticeable change
                keyboard.press_and_release('volume up')
            return True, "Volume increased"
        elif action == "vol_down":
            for _ in range(2):  # Press twice for more noticeable change
                keyboard.press_and_release('volume down')
            return True, "Volume decreased"
        elif action == "mute":
            keyboard.press_and_release('volume mute')
            return True, "Volume muted/unmuted"
        return False, "Invalid action"
    except Exception as e:
        return False, str(e)

def get_system_info():
    """Get detailed system information"""
    try:
        # Get CPU info
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Get memory info
        memory = psutil.virtual_memory()
        memory_total = round(memory.total / (1024 * 1024 * 1024), 2)  # Convert to GB
        memory_used = round(memory.used / (1024 * 1024 * 1024), 2)  # Convert to GB
        
        # Get disk info
        disk = psutil.disk_usage('/')
        disk_total = round(disk.total / (1024 * 1024 * 1024), 2)  # Convert to GB
        disk_used = round(disk.used / (1024 * 1024 * 1024), 2)  # Convert to GB
        
        # Get battery info if available
        battery = psutil.sensors_battery()
        battery_str = "N/A"
        if battery:
            battery_str = f"{battery.percent}% {'🔌' if battery.power_plugged else '🔋'}"
        
        # Get uptime
        uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
        uptime_str = str(timedelta(seconds=int(uptime.total_seconds())))
        
        return {
            'cpu_percent': f"{cpu_percent}%",
            'memory_percent': f"{memory.percent}%",
            'memory_usage': f"{memory_used}GB / {memory_total}GB",
            'disk_usage': f"{disk_used}GB / {disk_total}GB ({disk.percent}%)",
            'battery': battery_str,
            'uptime': uptime_str
        }
    except Exception as e:
        print(f"System info error: {str(e)}")
        return None

def get_process_list():
    """Get list of running processes"""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                # Get process info
                proc_info = proc.info
                memory_mb = round(proc_info['memory_info'].rss / (1024 * 1024), 1)
                
                # Add to list if using resources
                if proc_info['cpu_percent'] > 0 or memory_mb > 50:
                    processes.append({
                        'pid': proc_info['pid'],
                        'name': proc_info['name'],
                        'cpu': round(proc_info['cpu_percent'], 1),
                        'memory': memory_mb
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        # Sort by CPU usage and return top processes
        return sorted(processes, key=lambda x: x['cpu'], reverse=True)[:10]
    except Exception as e:
        print(f"Process list error: {str(e)}")
        return None

def kill_process(pid):
    """Kill a process by PID"""
    try:
        process = psutil.Process(pid)
        process.kill()
        return True, f"Process {pid} killed successfully"
    except psutil.NoSuchProcess:
        return False, f"Process {pid} not found"
    except psutil.AccessDenied:
        return False, f"Access denied to kill process {pid}"
    except Exception as e:
        return False, str(e)

def list_files(path=None):
    """List files in directory"""
    try:
        if path is None:
            path = os.path.expanduser('~')
            
        files = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                stats = os.stat(item_path)
                size = stats.st_size
                
                # Convert size to human readable format
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if size < 1024:
                        break
                    size /= 1024
                size = f"{round(size, 1)}{unit}"
                
                files.append({
                    'name': item,
                    'path': item_path,
                    'size': size,
                    'is_dir': os.path.isdir(item_path)
                })
            except:
                continue
                
        return sorted(files, key=lambda x: (not x['is_dir'], x['name'].lower()))
    except Exception as e:
        print(f"List files error: {str(e)}")
        return None

def media_control(action):
    """Control media playback"""
    try:
        if action == "play_pause":
            keyboard.press_and_release('play/pause media')
            return True, "Media play/pause toggled"
        elif action == "next":
            keyboard.press_and_release('next track')
            return True, "Next track"
        elif action == "prev":
            keyboard.press_and_release('previous track')
            return True, "Previous track"
        elif action == "stop":
            keyboard.press_and_release('stop media')
            return True, "Media stopped"
        return False, "Invalid media action"
    except Exception as e:
        return False, str(e)

def get_clipboard_text():
    """Get clipboard contents"""
    try:
        import win32clipboard
        win32clipboard.OpenClipboard()
        try:
            text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
            return True, text
        except:
            return False, "No text in clipboard"
        finally:
            win32clipboard.CloseClipboard()
    except Exception as e:
        return False, str(e)

def remote_control(action):
    """Remote control functions"""
    try:
        if action == "left_click":
            pyautogui.click()
            return True, "Left click"
        elif action == "right_click":
            pyautogui.rightClick()
            return True, "Right click"
        elif action == "double_click":
            pyautogui.doubleClick()
            return True, "Double click"
        elif action.startswith("move_"):
            direction = action.split("_")[1]
            distance = 20  # pixels to move
            if direction == "up":
                pyautogui.moveRel(0, -distance)
            elif direction == "down":
                pyautogui.moveRel(0, distance)
            elif direction == "left":
                pyautogui.moveRel(-distance, 0)
            elif direction == "right":
                pyautogui.moveRel(distance, 0)
            return True, f"Moved {direction}"
        elif action == "scroll_up":
            pyautogui.scroll(2)
            return True, "Scrolled up"
        elif action == "scroll_down":
            pyautogui.scroll(-2)
            return True, "Scrolled down"
        return False, "Invalid remote control action"
    except Exception as e:
        return False, str(e)

def file_transfer(file_path, action="download"):
    """Handle file transfer"""
    try:
        if action == "download":
            if os.path.exists(file_path):
                return True, file_path
            return False, "File not found"
        elif action == "upload":
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            return True, file_path
        return False, "Invalid file transfer action"
    except Exception as e:
        return False, str(e)

def search_files(query, path=None):
    """Search for files by name"""
    try:
        if path is None:
            path = os.path.expanduser('~')
            
        results = []
        for root, dirs, files in os.walk(path):
            # Skip system and hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and not d.startswith('$')]
            
            for name in files:
                if query.lower() in name.lower():
                    file_path = os.path.join(root, name)
                    try:
                        stats = os.stat(file_path)
                        size = stats.st_size
                        
                        # Convert size to human readable format
                        for unit in ['B', 'KB', 'MB', 'GB']:
                            if size < 1024:
                                break
                            size /= 1024
                        size = f"{round(size, 1)}{unit}"
                        
                        results.append({
                            'name': name,
                            'path': file_path,
                            'size': size
                        })
                    except:
                        continue
                        
            if len(results) >= 20:  # Limit results
                break
                
        return results
    except Exception as e:
        print(f"Search files error: {str(e)}")
        return None
