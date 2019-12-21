import typing
from .post import UNION, UNION_CHAR, RECURSION_CHAR
from ..recursion import RecursionArgument


class AheadValidation:
    def __init__(self, pattern, inclusions: dict, nested: dict, recursions: dict):
        self._inclusions = inclusions
        self._nested = nested
        self._recursions = recursions
        self.pattern = pattern

    def group(self, match) -> typing.Union[dict, typing.NoReturn]:
        groupdict: dict = match.groupdict()
        print("ahead")
        for inc in self._inclusions:
            if inc[0] == UNION_CHAR:
                union_name = inc.strip(UNION_CHAR) or UNION
                groupdict[union_name] = [
                    a for a in groupdict[union_name].split(self._inclusions[inc]) if a
                ]
            elif inc[0] == RECURSION_CHAR:
                print(self._inclusions, groupdict, inc)
                name = inc
                print(groupdict[name.strip(RECURSION_CHAR)])
                recursion: RecursionArgument = self._recursions[name]
                pattern = self.pattern(**recursion.pattern)
                print(pattern.pattern)
                print(pattern(groupdict[name.strip(RECURSION_CHAR)]))
                if pattern(groupdict[name.strip(RECURSION_CHAR)]):
                    groupdict[name] = {name: pattern.dict()}
                else:
                    return
        [groupdict.update(self._nested[a](groupdict) or {}) for a in self._nested]
        return groupdict
