import re
from .exceptions import PatternError
from .standart import PostValidation
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

    def __init__(
            self,
            text: str = None,
            pattern: str = "{}$"
    ):
        text = text or ""
        findall = re.findall

        # Find all arguments with validators
        typed_arguments = findall(
            r"(<([a-zA-Z0-9_]+)+:.*?>)", text.translate(self.escape)
        )

        # Delete arguments from regex
        text = re.sub(":.*?>", ">", text)
        text = re.sub(r"<(.*?)>", r"(?P<\1>.*?)", text.translate(self.escape))

        self._compiler = re.compile(pattern.format(text))
        self._validation: dict = PostValidation.get_validators(typed_arguments)
        self._arguments: list = findall("<(.*?)>", text.translate(self.escape))
        self._pregmatch: Optional[dict] = None

    def __call__(self, text: str):
        """
        Check text for current pattern ignoring all features
        :param text:
        :return:
        """
        match = self._compiler.match(text)
        if match is not None:
            self._pregmatch = match.groupdict()
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

    def set_dict(self, new_dict: dict):
        self._pregmatch = new_dict
        return new_dict

    def remove_dict(self):
        self._pregmatch = None

    def dict(self):
        if self._pregmatch is None:
            raise PatternError("Trying to get variables from text before matching text OR MATCHING WAS FAILED")
        return self._pregmatch
