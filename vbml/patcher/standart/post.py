from typing import List, Tuple, Sequence, Optional, Callable
from ..exceptions import PatternError
from ..recursion import RecursionArgument
import re


def flatten(lis):
    for item in lis:
        if isinstance(item, Sequence) and not isinstance(item, str):
            yield from flatten(item)
        else:
            yield item


SYNTAX: List[str] = ["*", "^", "#", "$", "!", "&"]
UNION: str = "_union"
UNION_CHAR: str = "*"
ONE_CHAR_CHAR: str = "^"
EXCEPT_CHAR: str = "#"
REGEX_CHAR: str = "$"
IGNORE_CHAR: str = "!"
RECURSION_CHAR: str = "&"

escape = {ord(x): "\\" + x for x in r"\.*+?()[]|^${}&"}


class Syntax:
    @staticmethod
    def union(args: list, arg: str, inclusion: dict, **context):
        pattern = "(?P<" + UNION + ">.*)"
        if len(arg.strip(UNION_CHAR)):
            pattern = "(?P<" + arg.strip(UNION_CHAR) + ">.*)"
        return pattern

    @staticmethod
    def one_char(args: list, arg: str, inclusion: dict, **context):
        if not len(arg.strip(ONE_CHAR_CHAR)):
            raise PatternError("Char argument should be named")

        pattern = "."
        if inclusion.get(arg):
            # inclusions = ["\\" + inc for inc in list(inclusion[arg])]
            pattern = "[" + inclusion[arg].translate(escape) + "]"

        return "(?P<" + arg.strip(ONE_CHAR_CHAR) + ">" + pattern + ")"

    @staticmethod
    def except_of(args: list, arg: str, inclusion: dict, **context):
        if not inclusion.get(arg):
            raise PatternError(
                "Except argument expression have to contain not less than one symbol in inclusion"
            )
        elif not len(arg.strip(EXCEPT_CHAR)):
            raise PatternError("Except expression should be named")

        pattern = "[^" + inclusion[arg].translate(escape) + "]"

        return "(?P<{}>{}+)".format(arg.strip(EXCEPT_CHAR), pattern)

    @staticmethod
    def regex_arg(args: list, arg: str, inclusion: dict, **context):
        if not inclusion.get(arg):
            raise PatternError(
                "Regex argument expression have to contain not less than one symbol in inclusion"
            )
        return inclusion[arg]

    @staticmethod
    def ignore_arg(*a, **k):
        return "(?:.*?)"

    @staticmethod
    def recursion_arg(args: list, arg: str, *a, **k):
        return "(?P<" + arg.strip(RECURSION_CHAR) + ">" + ".*" + ")"

    @staticmethod
    def recursion(args: list, arg: str, inclusion: dict, **context):
        if not inclusion.get(arg):
            raise PatternError('Recursion argument should maintain inclusion in ""')
        recursion = RecursionArgument(inclusion[arg], **context)
        return {arg: recursion}


class PostValidation(Syntax):
    @staticmethod
    def get_validators(
        typed_arguments: List[Tuple[str]], context: dict
    ) -> (dict, dict):
        validation: dict = {}
        nested: dict = {}

        for p in typed_arguments:

            validators: List[str] = re.findall(
                r":([a-zA-Z0-9_, ]+|[\[]+[a-zA-Z0-9_, ]+[\]]+)", p[0]
            )

            # Get arguments of validators
            for validator in validators:
                if (validator[0], validator[-1]) == ("[", "]"):
                    nestings = [
                        n.strip() for n in list(validator.strip("[]").split(",")) if n
                    ]
                    for nesting in nestings:
                        if not isinstance(context.get(nesting), Callable):
                            raise PatternError(
                                '"{}" nesting is missing in context'.format(nesting)
                            )
                        nested.update(**{nesting: context.get(nesting)})
                else:
                    validation[p[1]] = dict()
                    arguments = list(
                        flatten(
                            [
                                a.split(",")
                                for a in re.findall(
                                    ":" + validator + r"\[(.+)+\]", p[0]
                                )
                            ]
                        )
                    )
                    validation[p[1]][validator] = arguments

        return validation, nested

    @staticmethod
    def inclusion(argument: str) -> Optional[str]:
        inclusion: List[str] = re.findall(
            r"^\((.*?)\)[a-zA-Z0-9_" + "".join(SYNTAX) + "]+[:]?.*?$", argument
        )
        if len(inclusion):
            if inclusion[0] == "\\n":
                inclusion[0] = "\n"
            return inclusion[0]

    @staticmethod
    def append_inclusions(inclusions: dict, group_dict: dict):
        for arg in group_dict:
            if inclusions.get(arg) is not None:
                group_dict[arg] = inclusions[arg] + group_dict[arg]
        return group_dict
