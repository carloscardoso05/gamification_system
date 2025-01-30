def cut(text: str, max_length: int = 50, end: str = '...') -> str:
    if len(text) > max_length:
        text = text[:max_length - len(end)] + end
    return text
