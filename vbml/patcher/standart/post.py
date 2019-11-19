from typing import List, Tuple, Sequence, Optional
from ..exceptions import PatternError
import re


def flatten(lis):
    for item in lis:
        if isinstance(item, Sequence) and not isinstance(item, str):
            yield from flatten(item)
        else:
            yield item


SYNTAX: List[str] = ["*", "^", "#"]
UNION: str = "_union"
UNION_CHAR: str = "*"
ONE_CHAR_CHAR: str = "^"
EXCEPT_CHAR: str = "#"


class Syntax:
    @staticmethod
    def union(
            args: list,
            arg: str,
            inclusion: dict
    ):
        pattern = "(?P<" + UNION + ">.*)"
        if len(arg.strip(UNION_CHAR)):
            pattern = "(?P<" + arg.strip(UNION_CHAR) + ">.*)"
        return pattern

    @staticmethod
    def one_char(
            args: list,
            arg: str,
            inclusion: dict
    ):
        pattern = "."
        if inclusion.get(arg):
            inclusions = ["\\" + inc for inc in list(inclusion[arg])]
            pattern = "[" + "|".join(inclusions) + "]"
        if len(arg.strip(ONE_CHAR_CHAR)):
            return "(?P<" + arg.strip(ONE_CHAR_CHAR) + ">" + pattern + ")"
        return "(?P<char>.)"

    @staticmethod
    def except_of(
            args: list,
            arg: str,
            inclusion: dict
    ):
        if not inclusion.get(arg):
            raise PatternError("Except argument expression have to contain not less than one symbol in inclusion")
        elif not len(arg.strip(EXCEPT_CHAR)):
            raise PatternError("Except expression should be named")

        inclusions = ["\\" + inc for inc in list(inclusion[arg])]
        pattern = "[^" + "|".join(inclusions) + "]"
        return "(?P<{}>{}+)".format(
            arg.strip(EXCEPT_CHAR),
            pattern
        )


class PostValidation(Syntax):

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
