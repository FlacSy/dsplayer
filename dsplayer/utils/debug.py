import inspect
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)


class Debuger:
    def __init__(self, debug: bool = False):
        self.debug = debug

    def debug_print(self, message, show_time=True, show_location=True):
        if self.debug:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if show_time else ""
            frame = inspect.currentframe().f_back
            location = f"{frame.f_code.co_filename}:{frame.f_lineno}" if show_location else ""

            timestamp_color = Fore.GREEN
            location_color = Fore.MAGENTA
            message_color = Fore.CYAN

            formatted_message = (
                f"{timestamp_color}[{timestamp}]" if show_time else ""
            ) + (
                f" {location_color}[{location}]" if show_location else ""
            ) + f" {message_color}{message}{Style.RESET_ALL}"

            print(formatted_message)
