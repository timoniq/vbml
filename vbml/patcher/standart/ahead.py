import typing
from .post import UNION, UNION_CHAR, RECURSION_CHAR
from ..recursion import RecursionArgument

if typing.TYPE_CHECKING:
    from ..pattern import Pattern


class AheadValidation:
    def __init__(
        self, pattern: "Pattern", inclusions: dict, nested: dict, recursions: dict
    ):
        self._inclusions = inclusions
        self._nested = nested
        self._recursions = recursions
        self.pattern: "Pattern" = pattern

    def group(self, match) -> typing.Union[dict, None]:
        groupdict: dict = match.groupdict()
        for inc in self._inclusions:
            if inc[0] == UNION_CHAR:
                union_name = inc.strip(UNION_CHAR) or UNION
                groupdict[union_name] = [
                    a for a in groupdict[union_name].split(self._inclusions[inc]) if a
                ]
            elif inc[0] == RECURSION_CHAR:
                name = inc.strip(RECURSION_CHAR)
                recursion: RecursionArgument = self._recursions[inc]
                pattern = self.pattern(**recursion.pattern)
                if pattern(groupdict[name]):
                    groupdict.update({name: pattern.dict()})
                else:
                    return
        [groupdict.update(self._nested[a](groupdict) or {}) for a in self._nested]
        return groupdict
