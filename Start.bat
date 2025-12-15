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


:: Start the server
set JAVA_HOME="C:\Program Files\Java\jdk-21"
start "" %JAVA_HOME%\bin\java -Xmx2048M -Xms2048M -jar minecraft_server.1.21.10.jar


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
