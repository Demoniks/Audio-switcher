import time
import ctypes
import comtypes
from pycaw.pycaw import AudioUtilities, IAudioMeterInformation

# ---------- CONFIG ----------
CHECK_DELAY = 0.6     # seconds

VK_MEDIA_PLAY_PAUSE = 0xB3
KEYEVENTF_EXTENDEDKEY = 0x1
KEYEVENTF_KEYUP = 0x2

# ---------- STATE ----------
last_chrome = False
last_spotify = False

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
                    return meter.GetPeakValue() > 0.01
                except comtypes.COMError:
                    pass
    return False

print("Spotify Auto Switcher Active")
print(" Chrome pauses Spotify")
print("Chrome stop resumes Spotify")
print("------------------------------")

while True:
    chrome_now = is_app_playing("chrome")
    spotify_now = is_app_playing("spotify")

    # Handle chrome start -> pause SP
    if chrome_now and not last_chrome and spotify_now:
            print("Chrome started -> Pause SP")
            send_media_play_pause()

    # Chrome stopped -> resume SP
    if not chrome_now and last_chrome and not spotify_now:
            print("Chrome stopped -> Resume SP")
            send_media_play_pause()

    last_chrome = chrome_now
    last_spotify = spotify_now

    time.sleep(CHECK_DELAY)