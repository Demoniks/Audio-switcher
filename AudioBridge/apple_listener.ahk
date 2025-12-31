#Requires AutoHotKey v2.0
#SingleInstance Force

; Launch AM if not running
if !WinExist("ahk_exe AppleMusic.exe") {
    Run("shell:AppsFolder\AppleInc.AppleMusicWin_nzyj5cx40ttqa!App")
    Sleep 3000
}

; Focus & play
WinActivate("ahk_exe AppleMusic.exe")
Sleep 500

; Play once
Send("{Media_Play_Pause}")

; Return to Chrome
if WinExist("ahk_exe chrome.exe") {
    Sleep 300
    WinActivate("ahk_exe chrome.exe")
}

ExitApp