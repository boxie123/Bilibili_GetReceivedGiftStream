from time import sleep
from sys import exit

from rich.live import Live

from .console import console


def live_exit(seconds: int = 5):
    console.print("\n")
    with Live(f"感谢使用，程序将在 [b green]{seconds}[/b green] 秒后退出", console=console) as live:
        for i in range(seconds):
            sleep(1)
            live.update(f"感谢使用，程序将在 [b green]{seconds - 1 - i}[/b green] 秒后退出")
    exit(0)
