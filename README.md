# Minecraft Server Tooling

## TL;DR

Automated tooling for starting and configuring a (local) Minecraft server under Windows with a custom set of gamerules and commands.
Designed for SK jugend und medien workshops.

## Features

- **Automatic server startup** with Java configuration
- **Automatic gamerule configuration** and success validation from `sk_gamerule.properties`
- **Custom command execution** from `sk_custom_commands.txt`
- **RCON-based configuration** using [mcrcon](https://github.com/Tiiffi/mcrcon/releases)
- **Error handling** with user-friendly error messages

## How to Use

0. **Requirements**: Ensure that all requirements are present (see [Requirements](#requirements))
1. **Configure**: Specify the gamerules and commands you want to apply at startup in the provided configuration files.
2. **Start the server**: Run `Start.bat`
3. **Wait for configuration**: The script automatically waits for the server to start, then applies gamerules and custom commands
4. **Verify success**: Look for `[Rcon] SK Tooling: Everything is ready to go!` in the server console or check the log file (`sk_startup_log_*`)

### Configuration Files

- **`sk_gamerule.properties`**: Define gamerules in `rule=value` format (one per line, `#` for comments)
- **`sk_custom_commands.txt`**: Add custom server commands (one per line, without leading `/`, `#` for comments)

## Requirements

### Software
- **Java JDK 21** (path configured in `Start.bat`)
- **Python 3** (for configuration script)
- **[Minecraft Server JAR[(https://www.minecraft.net/de-de/download/server)** (e.g., `minecraft_server.1.21.10.jar`)

### Tools
- **mcrcon.exe** must be located at the location specified in `MC_RCON_LOCATION` in `sk_configure_server.py` (default: `helpers/mcrcon.exe`)
  - Download: https://github.com/Tiiffi/mcrcon/releases/tag/v0.7.2 (windows-x86-64)
- You can use our helper script `sk_download_mcrcon.bat` to download it

### Server Configuration
The following settings **must** be present in `server.properties`:
```
enable-rcon=true
rcon.password=verySecurePasswordThatYouShouldntChange
```
This is already configured in the `server.properties` in this repository.

**Note**: The RCON password must match `RCON_PASSWORD` in `sk_configure_server.py` (default: `verySecurePasswordThatYouShouldntChange`).

## Supported Versions
### Tested
- 1.21.10

## About
Since Minecraft `1.21.10`, PvP is no longer a setting in the `server.properties` instead it's a game rule.

PvP is prohibited in our workshops so we had to find a way to reliably disable it, every time a new world is set up.

This is why we developed this tooling for our internal use.
During development, we decided to expand the scope from "just disabling pvp" to a wider, more general approach.

Since we're pretty happy and confident with our solution we decided to open source it and make it available for other institutions as well.


## AI disclosure
- The initial version of this readme was AI generated based on the projects files.
- Some standard documentation of the python code was AI generated.
- All AI-generated code and text was audited by the authors.
- All other usages of AI are clearly disclosed as such in the related files.
