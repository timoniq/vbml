from .patcher import Patcher
import types


def validator(func):
    patcher = Patcher.get_current()
    setattr(patcher.validators, func.__name__, func)
    Patcher.set_current(patcher)


def match(pattern_text: str, text: str):
    """
    Allow to move and match strings easily
    """
    patcher = Patcher.get_current()
    pattern = patcher.pattern(pattern_text)
    return patcher.check(text, pattern)
