import re

NEWLINE_REGEX = re.compile(r"\n+")


def truncate_text(text: str, max_length: int) -> str:
    """
    Truncate text to a maximum length.

    Args:
        text (str): The text to truncate.
        max_length (int): The maximum length of the text.

    Returns:
        str: The truncated text.
    """
    if len(text) > max_length:
        return text[: max_length - 3] + "..."
    return text


def deduplicate_newlines(text: str) -> str:
    """
    Deduplicate newlines in a string.

    Args:
        text (str): The text to deduplicate newlines in.

    Returns:
        str: The text with deduplicated newlines.
    """
    return NEWLINE_REGEX.sub("\n", text)
