import os
import sys

try:
    import msvcrt
except ImportError:
    msvcrt = None

try:
    import termios
    import tty
except ImportError:
    termios = None
    tty = None

try:
    from colorama import Back, Fore, Style, just_fix_windows_console

    just_fix_windows_console()
except ImportError:

    class Fore:
        GREEN = "\033[32m"
        BLUE = "\033[34m"
        RED = "\033[31m"

    class Back:
        YELLOW = "\033[43m"
        RED = "\033[41m"
        GREEN = "\033[42m"

    class Style:
        NORMAL = "\033[22m"
        RESET_ALL = "\033[0m"


def clear_screen():
    """Clear the terminal in a way that works outside Replit."""
    os.system("cls" if os.name == "nt" else "clear")


def get_key():
    """Read one keypress without requiring Enter."""
    if msvcrt is not None:
        key = msvcrt.getwch()
        if key in ("\x00", "\xe0"):
            msvcrt.getwch()
            return ""
        return key

    if not sys.stdin.isatty() or termios is None or tty is None:
        return sys.stdin.read(1)

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def print_with_color(string, color, **kwargs):
    """Print a string with an ANSI foreground or background color."""
    brightness = Style.NORMAL
    return print(f"{brightness}{color}{string}{Style.RESET_ALL}", end="", **kwargs)

