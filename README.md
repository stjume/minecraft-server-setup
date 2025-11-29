# Minecraft Server Tooling

## TL;DR

Automated tooling for starting and configuring a (local) Minecraft server with a custom set of gamerules and commands.
Designed for SK jugend und medien workshops.

## Features

- **Automatic server startup** with Java configuration
- **Automatic gamerule configuration** from `sk_gamerule.properties`
- **Custom command execution** from `sk_custom_commands.txt`
- **RCON-based configuration** using mcrcon
- **Comprehensive logging** with timestamped log files
- **Error handling** with user-friendly error messages
- **Server connection retry** mechanism

## How to Use

1. **Start the server**: Run `Start.bat`
2. **Wait for configuration**: The script automatically waits for the server to start, then applies gamerules and custom commands
3. **Verify success**: Look for `[Rcon] SK Tooling: Everything is ready to go!` in the server console

### Configuration Files

- **`sk_gamerule.properties`**: Define gamerules in `rule=value` format (one per line, `#` for comments)
- **`sk_custom_commands.txt`**: Add custom server commands (one per line, without leading `/`, `#` for comments)

## Requirements

### Software
- **Java JDK 21** (path configured in `Start.bat`)
- **Python 3** (for configuration script)
- **Minecraft Server JAR** (e.g., `minecraft_server.1.21.10.jar`)

### Tools
- **mcrcon.exe** must be located at `helpers/mcrcon.exe`
  - Download: https://github.com/Tiiffi/mcrcon/releases/tag/v0.7.2 (windows-x86-64)

### Server Configuration
The following settings **must** be present in `server.properties`:
```
enable-rcon=true
rcon.password=verySecurePasswordThatYouShouldntChange
```

**Note**: The RCON password must match `RCON_PASSWORD` in `sk_configure_server.py` (default: `verySecurePasswordThatYouShouldntChange`).

