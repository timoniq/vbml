from .patcher import Patcher


def match(pattern_text: str, text: str):
    """
    Allow to move and match strings easily
    """
    patcher = Patcher.get_current()
    pattern = patcher.pattern(pattern_text)
    return patcher.check(text, pattern)
