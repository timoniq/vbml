import re
from .post import UNION, UNION_CHAR


class AheadValidation:
    def __init__(self, inclusions: dict, nested: dict):
        self._inclusions = inclusions
        self._nested = nested

    def group(self, match) -> dict:
        groupdict: dict = match.groupdict()
        for inc in self._inclusions:
            if inc[0] == UNION_CHAR:
                union_name = inc.strip(UNION_CHAR) or UNION
                groupdict[union_name] = [
                    a for a in groupdict[union_name].split(self._inclusions[inc]) if a
                ]
        [groupdict.update(self._nested[a](groupdict) or {}) for a in self._nested]
        return groupdict
