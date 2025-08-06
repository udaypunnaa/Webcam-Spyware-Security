@echo off
echo Enabling webcam immediately...
echo This script requires administrator privileges.
echo.

REM Enable webcam by restoring registry settings
echo Restoring registry settings...
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Class\{6bdd1fc6-810f-11d0-bec7-08002be2092f}" /v "UpperFilters" /t REG_MULTI_SZ /d "ksthunk" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Class\{6bdd1fc6-810f-11d0-bec7-08002be2092f}" /v "LowerFilters" /t REG_MULTI_SZ /d "" /f

REM Enable USB webcam devices
echo Enabling USB storage for webcams...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\USBSTOR" /v "Start" /t REG_DWORD /d 3 /f

REM Enable and start webcam-related services immediately
echo Starting webcam services...
sc config "USBSTOR" start=auto 2>nul
sc start "USBSTOR" 2>nul

REM Enable specific webcam drivers
echo Enabling webcam drivers...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\USBVIDEO" /v "Start" /t REG_DWORD /d 3 /f 2>nul
sc config "USBVIDEO" start=auto 2>nul
sc start "USBVIDEO" 2>nul

REM Enable camera devices in device manager immediately
echo Enabling camera devices...
for /f "tokens=2 delims==" %%i in ('wmic path win32_pnpentity where "name like '%%camera%%' or name like '%%webcam%%' or name like '%%usb video%%'" get deviceid /value ^| find "="') do (
    echo Enabling device: %%i
    pnputil /enable-device "%%i" 2>nul
)

REM Enable camera access through Group Policy
echo Enabling camera access...
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Camera" /v "AllowCamera" /t REG_DWORD /d 1 /f 2>nul

REM Enable camera for all users
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam" /v "Value" /t REG_SZ /d "Allow" /f 2>nul

REM Enable camera for specific apps
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam\NonPackaged" /v "Value" /t REG_SZ /d "Allow" /f 2>nul

REM Force refresh of device manager
echo Refreshing device manager...
devcon refresh 2>nul

REM Restart camera-related services
echo Restarting camera services...
sc stop "USBVIDEO" 2>nul
timeout /t 2 /nobreak >nul
sc start "USBVIDEO" 2>nul

echo.
echo Webcam enabled immediately.
echo.
echo IMPORTANT: The webcam should now be enabled without requiring a restart.
echo If it doesn't work, try closing and reopening the camera app.
echo.
pause 