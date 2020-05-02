from vbml.blanket import validator
from vbml import Patcher

patcher = Patcher()

@validator
def super_validator(value: str):
    if "," in value:
        return value.split(",")


pattern = patcher.pattern("i am <who:super_validator>")
if patcher.check("i am joe, mary, edith", pattern):
    print("Split personality confirmed")
    print(pattern.dict())
