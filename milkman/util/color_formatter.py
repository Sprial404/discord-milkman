import logging


class CustomFormatter(logging.Formatter):
    """
    Custom formatter for the logging module that adds color to the log messages.
    """

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    RESET = "\033[0m"
    BOLD = "\033[1m"

    COLORS = {
        logging.DEBUG: WHITE + BOLD,
        logging.INFO: GREEN + BOLD,
        logging.WARNING: YELLOW + BOLD,
        logging.ERROR: RED,
        logging.CRITICAL: RED + BOLD,
    }

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log message.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message.
        """
        log_color = self.COLORS.get(record.levelno, self.RESET)
        format_str = (
            "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (white){name}(reset) - {message}".replace(
                "(black)", self.BLACK
            )
            .replace("(reset)", self.RESET)
            .replace("(levelcolor)", log_color)
            .replace("(white)", self.WHITE + self.BOLD)
        )
        formatter = logging.Formatter(format_str, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)
