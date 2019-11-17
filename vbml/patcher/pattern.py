import re
from .exceptions import PatternError
from .standart import PostValidation, AheadValidation, SYNTAX, UNION_CHAR, ONE_CHAR_CHAR
from typing import List, Tuple, Sequence, Optional


def flatten(lis):
    for item in lis:
        if isinstance(item, Sequence) and not isinstance(item, str):
            yield from flatten(item)
        else:
            yield item


ARG_PREFIX = '<'
ARG_SUFFIX = '>'


class Pattern:
    # Make whole text re-invisible
    escape = {ord(x): "\\" + x for x in r"\.*+?()[]|^${}"}
    syntax = SYNTAX
    syntax_proc = {
        UNION_CHAR: PostValidation.union,
        ONE_CHAR_CHAR: PostValidation.one_char,
    }

    def __init__(
            self,
            text: str = None,
            pattern: str = "{}$",
            lazy: bool = True
    ):
        text = text or ""
        findall = re.findall

        # Find all arguments with validators
        typed_arguments = findall(
            r"(<([a-zA-Z0-9_]+)+:.*?>)", text.translate(self.escape)
        )
        # Save validators. Parse arguments
        self._validation: dict = PostValidation.get_validators(typed_arguments)

        # Delete arguments from regex
        text = re.sub(r":.*?>", ">", text)

        # Get all inclusions from regex
        inclusions: List[Optional[str]] = [PostValidation.inclusion(inc) for inc in findall("<(.*?)>", text)]

        # Delete inclusion from regex
        text = re.sub(r"<\(.*?\)", "<", text)

        ### Investigate final pattern
        # Set pattern constants
        self._arguments: list = findall("<(.*?)>", text)
        self._inclusions: dict = dict(zip(self.arguments, inclusions))
        self._ahead = AheadValidation(self.inclusions)

        # Remove regex-incompatible symbols
        text = text.translate(self.escape)

        # Reveal arguments
        for arg in self.arguments:
            if arg == '':
                raise PatternError("Argument can't be empty")
            if arg[0] in self.syntax:
                text = text.replace(
                    "<{}>".format(arg.translate(self.escape)),
                    self.syntax_proc[arg[0]](self.arguments, arg, self.inclusions)
                )
            else:
                text = text.replace(
                    "<{}>".format(arg),
                    '(?P<{arg}>{pre}.*{lazy})'.format(
                        arg=arg,
                        pre=self.inclusions.get(arg, "") or "",
                        lazy="?" if lazy else ""
                    ))

        self._compiler = re.compile(pattern.format(text))
        self._pregmatch: Optional[dict] = None

    def __call__(self, text: str):
        """
        Check text for current pattern ignoring all features
        :param text:
        :return:
        """
        match = self._compiler.match(text)
        if match is not None:
            self._pregmatch = self._ahead.group(match)
            return True

    @property
    def pattern(self):
        return self._compiler.pattern

    @property
    def validation(self):
        return self._validation

    @property
    def arguments(self):
        return self._arguments

    @property
    def inclusions(self):
        return self._inclusions

    def set_dict(self, new_dict: dict):
        self._pregmatch = new_dict
        return new_dict

    def remove_dict(self):
        self._pregmatch = None

    def dict(self):
        if self._pregmatch is None:
            raise PatternError("Trying to get variables from text before matching text OR MATCHING WAS FAILED")
        return self._pregmatch
