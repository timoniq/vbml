import re
from .post import UNION, UNION_CHAR


class AheadValidation:
    def __init__(self, inclusions: dict):
        self._inclusions = inclusions

    def group(self, match) -> dict:
        groupdict: dict = match.groupdict()
        if UNION_CHAR in self._inclusions:
            groupdict[UNION] = groupdict[UNION].split(self._inclusions[UNION_CHAR])
        return groupdict
