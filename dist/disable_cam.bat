@echo off
echo Disabling webcam immediately...
echo This script requires administrator privileges.
echo.

REM Kill any processes using the camera
echo Stopping camera processes...
taskkill /f /im "CameraApp.exe" 2>nul
taskkill /f /im "WindowsCamera.exe" 2>nul
taskkill /f /im "Microsoft.WindowsCamera.exe" 2>nul
taskkill /f /im "HoloCamera.exe" 2>nul

REM Disable webcam by modifying registry
echo Modifying registry settings...
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Class\{6bdd1fc6-810f-11d0-bec7-08002be2092f}" /v "UpperFilters" /t REG_MULTI_SZ /d "" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Class\{6bdd1fc6-810f-11d0-bec7-08002be2092f}" /v "LowerFilters" /t REG_MULTI_SZ /d "" /f

REM Disable USB webcam devices
echo Disabling USB storage for webcams...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\USBSTOR" /v "Start" /t REG_DWORD /d 4 /f

REM Stop and disable webcam-related services immediately
echo Stopping webcam services...
sc stop "USBSTOR" 2>nul
sc config "USBSTOR" start=disabled 2>nul

REM Disable specific webcam drivers
echo Disabling webcam drivers...
reg add "HKLM\SYSTEM\CurrentControlSet\Services\USBVIDEO" /v "Start" /t REG_DWORD /d 4 /f 2>nul
sc stop "USBVIDEO" 2>nul
sc config "USBVIDEO" start=disabled 2>nul

REM Disable camera devices in device manager immediately
echo Disabling camera devices...
for /f "tokens=2 delims==" %%i in ('wmic path win32_pnpentity where "name like '%%camera%%' or name like '%%webcam%%' or name like '%%usb video%%'" get deviceid /value ^| find "="') do (
    echo Disabling device: %%i
    pnputil /disable-device "%%i" 2>nul
)

REM Disable camera access through Group Policy
echo Disabling camera access...
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Camera" /v "AllowCamera" /t REG_DWORD /d 0 /f 2>nul

REM Disable camera for all users
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam" /v "Value" /t REG_SZ /d "Deny" /f 2>nul

REM Disable camera for specific apps
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam\NonPackaged" /v "Value" /t REG_SZ /d "Deny" /f 2>nul

REM Force refresh of device manager
echo Refreshing device manager...
devcon refresh 2>nul

echo.
echo Webcam disabled immediately.
echo.
echo IMPORTANT: The webcam should now be disabled without requiring a restart.
echo If it still works, try closing and reopening the camera app.
echo.
pause 