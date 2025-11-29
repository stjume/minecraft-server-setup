"""
This script is developed for the SK jugend und medien.

Its purpose is to start a Minecraft server and automatically set a set of
gamerules and custom commands as soon as the server has started.

The gamerules can be configured the same way you would do with server.properties.
The custom commands are expected to be plugged in line by line (w/o a starting /)
Please refer to the variables GAME_RULES_FILE and CUSTOM_COMMANDS_FILE
for the expected location and name of those files

It requires the program `mcrcon` to be present in:
    ./helpers/mcrcon.exe

`mcrcon` can be downloaded from:
    https://github.com/Tiiffi/mcrcon/releases/tag/v0.7.2  (windows-x86-64)

`mcrcon` is used to disable PvP immediately after the server boots.

The following settings **must** exist in `server.properties`:
    enable-rcon=true
    rcon.password=verySecurePasswordThatYouShouldntChange

The password must match the variable `RCON_PASSWORD` defined in this script.

If everything works correctly, you should see the following in the
*Log and Chat* output inside the Minecraft server console:

    [Not Secure] [Rcon] SK Tooling: Everything is ready to go!

(The “not secure” warning is normal — this RCON usage is inside a
local network and should be fine.)

Please also check the messages in the terminal.

If you receive an error message, it means something did not work
as expected.

In normal use, the only part you may need to modify is the server
start command (e.g., if you change Minecraft versions).

Author:
    Chris G
"""

import logging
import subprocess
import sys
import time
import types
from datetime import datetime
from pathlib import Path
from subprocess import CompletedProcess
from typing import Optional

# how long do we want to wait for the server to start up before we display errors (by default)
WAIT_CYCLES = 20
WAIT_TIME_PER_TRY = 3

# how we try to connect to the server
RCON_HOST = "127.0.0.1"
RCON_PORT = "25575"
RCON_PASSWORD = "verySecurePasswordThatYouShouldntChange"

# locations where we expect the config files
GAME_RULES_FILE = 'sk_gamerule.properties'
CUSTOM_COMMANDS_FILE = 'sk_custom_commands.txt'

# logging stuff
now = datetime.now()
LOG_FILE = Path(f"sk_startup_log_{now.year}_{now.month:02d}_{now.day:02d}-{now.hour:02d}:{now.minute:02d}:{now.second:02d}.log")


def build_command(_cmd: str) -> list[str]:
    """assumes mcrcon is located at helpers/mcrcon.exe"""

    c = [
        Path("helpers/mcrcon.exe"),
        "-H", RCON_HOST,
        "-P", RCON_PORT,
        "-p", RCON_PASSWORD,
        _cmd
    ]

    return c


def send_command(cmd: list[str]) -> CompletedProcess[str]:
    """basically a wrapper to run a shell command"""
    return subprocess.run(cmd, capture_output=True, text=True)


def build_error_message(reason: str) -> list[str]:
    """takes a reason and builds a more sophisticated error message (meant to be used in critical failure situations)"""

    return [
        f"1/4 Error: SK-Internal Tooling: {reason} Turning PvP off automatically failed! The server might be running but not configured as expected.",
        f"2/4 Use '/gamerule pvp false' ingame to disable it! Have a look at '{GAME_RULES_FILE}' and '{CUSTOM_COMMANDS_FILE}' to check if any other important configuration might have failed. (Remember.: PvP is not allowed in Workshops).",
        f"3/4 Please report this incident! (What template did you use? Was it the first start of the server? Were '{GAME_RULES_FILE}' and '{CUSTOM_COMMANDS_FILE}' present? Any other remarks?)",
        f"4/4 You can find the full log of this script execution at '{LOG_FILE.as_posix()}'"
    ]


def display_err_msg(msgs: list[str]) -> None:
    """
    Displays a list of error messages via (`msg`)) within a windows error popup (one per list entry)
    Sens a copy both the logger.

    The split into multiple messages is needed bc msg seems to have a text limit...

    Args:
        msgs (list[str]): List of error message strings to be displayed and logged.
    """
    

    logger.error("\n".join(msgs))
    for line in msgs:
        subprocess.run(["msg", "*", line])


# only waiting for connection (aka server start)
def wait_for_server(wait_cyles: int = WAIT_TIME_PER_TRY, wait_time_per_try: float = WAIT_TIME_PER_TRY) -> bool:
    """
    wait until server is up or terminate with warning
    returns True if successfully connected else False
    """
    success = False
    for retry_i in range(1, wait_cyles+1):
        # use any command that returns some value to check response
        cmd = build_command("gamerule keepInventory")
        try:
            result = send_command(cmd)
        except FileNotFoundError:
            msgs = build_error_message("'mcrcon.exe' is not located in ./helpers/ - please download it!")
            display_err_msg(msgs)
            return False

        if result.stderr:
            logger.info(f"Can't connect to server for config, retrying in {wait_time_per_try}s (retry: {retry_i})")
            time.sleep(wait_time_per_try)
            continue

        # break loop as soon as we can establish a connection
        success = True
        break

    if not success:
        err_msgs = build_error_message("Can't connect to server for configuration!")
        logger.error("\n".join(err_msgs))
        display_err_msg(err_msgs)
        return False


    else:
        logger.debug("Server up, can connect!")
        return True


def send_gamerules(file: Path = Path(GAME_RULES_FILE)) -> int:
    """
    sets gamerules, returns number of errors encountered during that process
    returns number of errors
    """

    if not file.exists():
        err_msgs = build_error_message(f"Can't find file '{file}'.")
        display_err_msg(err_msgs)
        logger.error("\n".join(err_msgs))
        return 1

    text = file.read_text()

    lines = text.split("\n")

    errors = 0
    for l in lines:
        l = l.strip()
        if l.startswith("#") or not l:
            continue

        split = l.split("=")

        if len(split) != 2:
            logger.warning(f"Malformed line '{l}', lines have to follow the format 'rule=value', skipping line")
            errors += 1
            continue

        rule, value = split

        # set value
        cmd = build_command(f"gamerule {rule} {value}")
        result = send_command(cmd)


        # did it work at all
        if f"now set to" not in result.stdout or result.stderr:
            logger.error(
                f"Gamerule '{rule}' couldn't be set to '{value}', full error message: '{result.stderr.strip() or result.stdout.strip()}', (skipping)")
            errors += 1
            continue

        # sanity check
        if f"now set to: {value}" not in result.stdout:
            logger.error(f"Gamerule '{rule}' doesn't have expected value '{value}'! (Set command didn't raise any errors. Please report this incident and try manually!) (skipping)")
            errors += 1
            continue

    return errors


def send_arbitrary_commands(file: Path = Path(CUSTOM_COMMANDS_FILE)) -> int:
    """send arbitrary commands to server (no success validation), returns number of (obvious) errors"""
    if not file.exists():
        logger.error(f"Can't find file '{file}', no commands executed.")
        return 1

    text = file.read_text()
    lines = text.split("\n")

    errors = 0
    for line in lines:
        line = line.strip()
        if line.startswith("#") or not line:
            continue

        if line.startswith("gamerule"):
            logger.warning(f"Please use '{GAME_RULES_FILE}' for specifying gamerules. Rules specified in that file are validated for success. Will still execute your gamerule command.")

        cmd = build_command(line)
        # TODO error handling for failed commands that may come in via stdout
        result = send_command(cmd)

        if result.stderr:
            errors += 1
            logger.error(f"Encountered error '{result.stderr}' for command '{cmd}'")

    return errors


def end_loop(msg: str = None):
    """
    keep shell window open to display log
    msg: optional message (meant to be the final verdict of the execution) to be displayed and sent to log
    """
    if msg:
        if msg.startswith("Error:"):
            logger.error(msg)
        elif msg.startswith("Warning:"):
            logger.warning(msg)
        else:
            logger.info(msg)
    logger.info(f"SK Config script finished. Please check for errors above. You may close this window.")
    while True:
        time.sleep(100)


def setup_logger(log_file: Path, level: int = logging.DEBUG) -> logging.Logger:
    """setup logging"""

    # https://stackoverflow.com/a/60523940
    def exc_handler(exctype: type[BaseException], value: BaseException, tb: Optional[types.TracebackType]) -> None:
        _logger.critical(value, exc_info=(exctype, value, tb))
        sys.__excepthook__(exctype, value, tb)

    sys.excepthook = exc_handler

    _logger = logging.getLogger()
    _logger.setLevel(level)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    # ---- Console Handler ----
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # ---- Formatter ----
    file_formatter = logging.Formatter("[%(asctime)s.%(msecs)03d][%(levelname)s][%(lineno)s] %(message)s")
    stream_formatter = logging.Formatter("[%(asctime)s.%(msecs)03d][%(levelname)s] %(message)s")

    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(stream_formatter)

    # ---- Add handlers to logger ----
    _logger.addHandler(file_handler)
    _logger.addHandler(console_handler)

    return _logger


logger = setup_logger(LOG_FILE)


if __name__ == '__main__':
    logger.info(f"Here is '{__file__}.py', logs are written to '{LOG_FILE.as_posix()}'")

    # connect
    connected = wait_for_server()
    if not connected:
        end_loop("Error: CAN'T CONNECT TO SERVER! Please check above. Server not configured.")

    # send commands
    gamerule_errors = send_gamerules()

    command_errors = send_arbitrary_commands()

    # endgame
    if gamerule_errors or command_errors:
        send_command(build_command(f"say SK Tooling: Game Rule Errors: {gamerule_errors}, Command Errors: {command_errors}. Please check terminal!"))
        end_loop(f"Warning: Game Rule Errors: {gamerule_errors}, Command Errors: {command_errors}")

    send_command(build_command("say SK Tooling: Everything is ready to go! Have fun :D ~chris"))

    end_loop(f"Finished server configuration with {gamerule_errors + command_errors} errors.")
