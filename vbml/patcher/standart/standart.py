from urllib import parse


class PatchedValidators:
    def _find_validator(self, key: str):
        return getattr(self, key, None)

    def int(self, value: str):
        if value.isdigit():
            return int(value)
        return

    def float(self, value: str):
        try:
            return float(value)
        except ValueError:
            return

    def url(self, value: str):
        scheme = parse.urlparse(value)
        if scheme.netloc != "":
            return value
        return

    def validator(self, value: str, *args):
        print(
            "Value {} was validated by default validator! Hold on.\nReceived args: {}".format(
                value, args
            )
        )
        return value
