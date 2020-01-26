from ..exceptions import LoaderError
from ..pattern import Pattern
import typing
import re


class Loader:
    def __init__(
        self, arguments_creation_mode: int = 1, use_validators: bool = False, **context
    ):
        """
        Create loader
        :param arguments_creation_mode: Set arg mode to:
        1 - Numerate mode (args creation such as item_1, item_2
        2 - Ignore mode (args created as ignored - <!>)
        :param use_validators: BETA
        :param context: pattern params from patcher
        """
        if arguments_creation_mode not in [1, 2]:
            raise LoaderError(
                "Available modes:\n" "1 - numerate mode\n" "2 - ignore mode"
            )
        self.use_validators: bool = use_validators
        self.undefined = "%"
        self.context: dict = context
        self.acm = arguments_creation_mode

    def merge(self, *items: str) -> typing.Union[Pattern, None]:
        """
        Load items as matches and merge it to pattern
        :param items: Strings to merge
        :return: Pattern or none
        """
        if not items:
            raise LoaderError("Items count should be not less than 1")
        if not all(items):
            raise LoaderError("Items can't be empty!")

        first = list(items[0])

        for i, symbol in enumerate(first):
            for item in items:
                if len(item) >= i + 1:
                    if item[i] != symbol:
                        first[i] = self.undefined
                else:
                    first = first[:i]
                    first.append(self.undefined)
                    continue

        queue = 1
        first = list(re.sub(r"(%)+", "%", "".join(first)))

        for i, nested in enumerate(first):
            if nested == self.undefined:
                if self.acm == 1:
                    first[i] = "<item_{}>".format(queue)
                    queue += 1
                elif self.acm == 2:
                    first[i] = "<!>"

        pattern = "".join(first)

        return Pattern(pattern, **self.context)
