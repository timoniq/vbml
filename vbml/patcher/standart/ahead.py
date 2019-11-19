import re
from .post import UNION, UNION_CHAR


class AheadValidation:
    def __init__(self, inclusions: dict):
        self._inclusions = inclusions

    def group(self, match) -> dict:
        groupdict: dict = match.groupdict()
        for inc in self._inclusions:
            if inc[0] == UNION_CHAR:
                union_name = inc.strip(UNION_CHAR) or UNION
                groupdict[union_name] = groupdict[union_name].split(self._inclusions[inc])
        return groupdict
