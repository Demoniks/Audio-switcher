import time
import ctypes
import comtypes
import subprocess
from pycaw.pycaw import AudioUtilities, IAudioMeterInformation

# ---------- CONFIG ----------
CHECK_DELAY = 0.25     # seconds

VK_MEDIA_PLAY_PAUSE = 0xB3
KEYEVENTF_EXTENDEDKEY = 0x1
KEYEVENTF_KEYUP = 0x2

# ---------- STATE ----------
last_chrome_playing = False

def trigger_apple_macro():
    subprocess.Popen([
        r"C:\Program Files\AutoHotkey\v2\Autohotkey64.exe",
        r"C:\AudioBridge\apple_listener.ahk"
    ])

def send_media_play_pause():
    ctypes.windll.user32.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, KEYEVENTF_EXTENDEDKEY, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(
        VK_MEDIA_PLAY_PAUSE,
        0,
        KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP,
        0,
    )

def is_app_playing(app_keyword: str) -> bool:
    sessions = AudioUtilities.GetAllSessions()

    for session in sessions:
        if session.Process:
            name = session.Process.name().lower()

            if app_keyword.lower() in name:
                try:
                    meter = session._ctl.QueryInterface(IAudioMeterInformation)
                    peak = meter.GetPeakValue()
                    if peak > 0.01:
                        return True
                except comtypes.COMError:
                    pass
    return False

print("Chrome -> Auto-pause Apple Music")
print(" Apple will NEVER stop Chrome")
print("AutoHotkey bridge enabled")

# Stability Timers
chrome_start_time = None
chrome_stop_time = None

MIN_ACTIVE_TIME = 0.25
MIN_STOP_TIME = 1.0

while True:
    chrome_playing = is_app_playing("chrome")
    now = time.time()

    # Handle chrome start -> pause am
    if chrome_playing:
        chrome_stop_time = None

        if not last_chrome_playing:
            if chrome_start_time is None:
                chrome_start_time = now

            elif now - chrome_start_time >= MIN_ACTIVE_TIME:
                print("Chrome started -> Pause AM")
                send_media_play_pause()
                last_chrome_playing = True
                chrome_start_time = None

    # Chrome stopped -> fire ahk directly
    else:
        chrome_start_time = None

        if last_chrome_playing:
            if chrome_stop_time is None:
                chrome_stop_time = now

            elif now - chrome_stop_time >= MIN_STOP_TIME:
                print("Chrome stopped -> Launch AM via AHK")
                trigger_apple_macro()

                last_chrome_playing = False
                chrome_stop_time = None

    time.sleep(0.6)
