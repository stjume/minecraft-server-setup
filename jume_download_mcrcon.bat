:: AI generated. prompt:
:: give me a windows bat file to download this file and unzip its contents to .\helpers https://github.com/Tiiffi/mcrcon/releases/download/v0.7.2/mcrcon-0.7.2-windows-x86-64.zip

@echo off
set URL=https://github.com/Tiiffi/mcrcon/releases/download/v0.7.2/mcrcon-0.7.2-windows-x86-64.zip
set ZIPFILE=mcrcon.zip
set DEST=helpers

echo Creating destination folder...
mkdir "%DEST%" >nul 2>&1

echo Downloading mcrcon...
powershell -Command "Invoke-WebRequest '%URL%' -OutFile '%ZIPFILE%'"

echo Unzipping...
powershell -Command "Expand-Archive -Path '%ZIPFILE%' -DestinationPath '%DEST%' -Force"

echo Cleaning up...
del "%ZIPFILE%"

echo Done! Files extracted to .\%DEST%
pause
