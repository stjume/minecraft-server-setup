@echo off
setlocal

:: This script is developed for the stiftung jugend und medien
:: Its purpose is to start a minecraft server and automatically set the gamerules and custom commands.
:: It requires this program mcrcon to be present at .\helper 
:: -> .\helpers\mcrcon.exe

:: mcrcon can be downloaded here.: https://github.com/Tiiffi/mcrcon/releases/tag/v0.7.2 (windows-x86-64)
:: mcrcon is used to disable PvP as soon as the server is started.

:: It is also required to have the following settings in the server.properties:
:: enable-rcon=true
:: rcon.password=verySecurePasswordThatYouShouldntChange
:: The latter must match 'RCON_PASSWORD' in the called python script

:: If everything goes to plan you should see the following in 'Log and Chat' in the Minecraft Server Window:
:: [Not Secure] [Rcon] jume Tooling: Everything is ready to go!

:: Don't worry about the 'not secure' part too much. We're in a local network. It _should_ be fine :P
:: If you get an error message this means that something *did not work*.

:: Generally you shouldn't need to touch anything in this script except the start command (when exchanging the version)

:: Author: Chris G


:: Test if python is installed
where python >nul 2>nul
if errorlevel 1 (
    msg * "ERROR: Python is not installed! The minecraft server will start, but no Gamerules or Commands will be set on startup. Disable PvP manually with /gamerule pvp false"
)

:: IF python is installed.
:: IF mcrcon is NOT installed AND no custom path to mcrcon is set.
:: Ask in a popup whether it shall be installed right now.
:: (We call powershell here because it can do GUI dialogues)
:: If yes: Then call .\jume_download_mcrcon.bat
where python >nul 2>nul
if not errorlevel 1 if "%MC_RCON_LOCATION%"=="" if not exist ".\helpers\mcrcon.exe" (
    powershell -NoProfile -Command ^
      "[void][System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms');" ^
      "$r = [System.Windows.Forms.MessageBox]::Show('mcrcon.exe is missing at default location. Download and install now?', 'mcrcon installer', 'YesNo', 'Question');" ^
      "if ($r -eq [System.Windows.Forms.DialogResult]::Yes) { exit 0 } else { exit 1 }"

    if %errorlevel%==0 (
        :: blocking call until finished
        call ".\jume_download_mcrcon.bat"
    ) else (
        echo Skipping mcrcon installation. Gamerules and commands will not be executed. Disable PvP manually with /gamerule pvp false 
    )
)


:: Start the server
set JAVA_HOME="C:\Program Files\Java\jdk-21"
:: Our standard server is started by calling a server.jar directly
::  Forge servers bring their own run.bat that you should run to start
if exist "server.jar" (
    start "" %JAVA_HOME%\bin\java -Xmx2048M -Xms2048M -jar server.jar
) else if exist "run.bat" (
    call run.bat
) else (
    msg * "ERROR: server.jar (standard servers) or run.bat (forge servers) not found! Cannot start the server."
    exit /b 1
)


:: PROMPT: add a check if an eula.txt exists and if there's a value eula=true in it. before the server is started
:: if not use the msg popup to notifiy the user and exit the script.

:: Check EULA acceptance
if not exist "eula.txt" (
    msg * "ERROR: eula.txt not found! The minecraft server process should create it in a few seconds. Please then set eula=true in it and re-run this script. Otherwise the server won't start."
    exit /b 1
)

findstr /C:"eula=true" "eula.txt" >nul
if errorlevel 1 (
    msg * "ERROR: EULA not accepted! Please set eula=true in eula.txt and re-run this script. Otherwise the server won't start."
    exit /b 1
)

:: Custom server config
python jume_configure_server.py

pause

endlocal
