@echo off
set "root_folder=C:\osed-scripts"

@REM Check if Root folder exists, if not create it
if not exist "%root_folder%" (
    echo Root folder does not exist, creating it...
    mkdir "%root_folder%"
    mkdir "%root_folder%\rp-win"
    mkdir "%root_folder%\scripts"
    mkdir "%root_folder%\windbg-scripts"

    echo Copying everything, except rsrc/, to %root_folder%...
    copy /Y /V \\tsclient\osed-scripts\rp-win %root_folder%\rp-win >NUL
    copy /Y /V \\tsclient\osed-scripts\scripts %root_folder%\scripts >NUL
    copy /Y /V \\tsclient\osed-scripts\windbg-scripts %root_folder%\windbg-scripts >NUL

    REM Create a backup of the original file
    copy c:\windbg_custom.WEW c:\windbg_custom.WEW.bak >NUL
    echo Windbg workspace Backup created at: c:\windbg_custom.WEW.bak

    REM Perform the copy
    echo Copying the custom Windbg workspace...
    copy /Y /V \\tsclient\osed-scripts\rsrc\windbg_custom.WEW c:\windbg_custom.WEW >NUL
    REM Set Black theme
    \\tsclient\osed-scripts\rsrc\windbg.reg

    REM Copy windbg-scripts to where pykd (python) can find them without a absolute path
    echo Copying windbg-scripts to python path so you don't need absolute paths from pykd...
    copy /Y /V %root_folder%\windbg-scripts\* C:\Users\Offsec\AppData\Local\Programs\Python\Python37-32\Scripts\ >NUL
)
