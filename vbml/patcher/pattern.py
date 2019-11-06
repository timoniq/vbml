import re
from .exceptions import PatternError
from typing import List, Tuple, Sequence, Optional


def flatten(lis):
    for item in lis:
        if isinstance(item, Sequence) and not isinstance(item, str):
            yield from flatten(item)
        else:
            yield item


class Pattern:
    # Make whole text re-invisible
    escape = {ord(x): "\\" + x for x in r"\.*+?()[]|^$"}

    def __init__(self, text: str, prefix: List[str] = None, pattern: str = '{}$'):
        prefix = re.compile(f"[{'|'.join(prefix)}]" if prefix else "")

        # Find all arguments with validators
        typed_arguments = re.findall(r"(<([a-zA-Z0-9_]+)+:.*?>)", text.translate(self.escape))

        # Delete arguments from regex
        text = re.sub(":.*?>", ">", text.translate(self.escape))

        text = re.sub(r"(<.*?>)", r"(?P\1.*?)", text.translate(self.escape))

        self._compiler = re.compile(prefix.pattern + pattern.format(text))
        self._validation: dict = self.__validators__(typed_arguments)
        self._arguments: list = re.findall(r"<(.*?)>", text.translate(self.escape))
        self._pregmatch: Optional[dict] = None

    @staticmethod
    def __validators__(typed_arguments: List[Tuple[str]]) -> dict:
        validation: dict = {}

        for p in typed_arguments:

            validators = re.findall(r":([a-zA-Z0-9_]+)+", p[0])
            validation[p[1]] = dict()

            # Get arguments of validators
            for validator in validators:
                arguments = list(flatten(
                    [
                        a.split(",")
                        for a in re.findall(":" + validator + r"\\\[(.+)+\\\]", p[0])
                    ]))
                validation[p[1]][validator] = arguments

        return validation

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
        return self._compiler

    @property
    def validation(self):
        return self._validation

    @property
    def arguments(self):
        return self._arguments

    def set_dict_after_patcher_check(self, new_dict: dict):
        self._pregmatch = new_dict

    def dict(self):
        if not self._pregmatch:
            raise PatternError('Trying to get variables from text before matching text')
        return self._pregmatch
