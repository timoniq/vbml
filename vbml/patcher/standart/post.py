from typing import List, Tuple, Sequence, Optional
from ..exceptions import PatternError
import re


def flatten(lis):
    for item in lis:
        if isinstance(item, Sequence) and not isinstance(item, str):
            yield from flatten(item)
        else:
            yield item


SYNTAX: List[str] = ["*", "^"]
UNION: str = "_union"
UNION_CHAR: str = "*"


class PostValidation:

    @staticmethod
    def get_validators(typed_arguments: List[Tuple[str]]) -> dict:
        validation: dict = {}

        for p in typed_arguments:

            validators = re.findall(r":([a-zA-Z0-9_]+)+", p[0])
            validation[p[1]] = dict()

            # Get arguments of validators
            for validator in validators:
                arguments = list(
                    flatten([
                        a.split(",")
                        for a in re.findall(
                            ":" + validator + r"\\\[(.+)+\\\]", p[0]
                        )]
                    )
                )
                validation[p[1]][validator] = arguments

        return validation

    @staticmethod
    def inclusion(argument: str) -> Optional[str]:
        inclusion = re.findall(r"^\((.*?)\)[a-zA-Z0-9_" + "".join(SYNTAX) + "]+[:]?.*?$", argument)
        if len(inclusion):
            return inclusion[0]

    @staticmethod
    def append_inclusions(inclusions: dict, group_dict: dict):
        for arg in group_dict:
            if inclusions.get(arg) is not None:
                group_dict[arg] = inclusions[arg] + group_dict[arg]
        return group_dict

    @staticmethod
    def union(args: list,
              inclusions: dict,
              validation: dict):
        if "*" != args[-1]:
            raise PatternError('Union <*> argument can be only the last argument')
        pattern = "(?P<" + UNION + ">.*)"
        return pattern

