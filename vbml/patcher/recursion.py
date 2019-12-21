
class RecursionArgument:
    def __init__(self, value: str, **context):
        if (value[0], value[-1]) != ('"', '"'):
            raise ValueError("vbml Recursion argument's inclusion should be maintained by the \"...\" separators")
        self._value = value[1:-2]
        self._pattern = {"text": self.value, **context}

    @property
    def value(self) -> str:
        return self._value

    @property
    def pattern(self) -> dict:
        return self._pattern