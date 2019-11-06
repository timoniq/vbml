class VBMLValidators:
    def __init__(self):
        pass

    def int(self, value: str):
        if value.isdigit():
            return int(value)
