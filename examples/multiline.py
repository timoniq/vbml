from vbml import Pattern, Patcher
from vbml.validators import ValidatorManager

# Assign manager and patcher
manager = ValidatorManager()
patcher = Patcher()

# Create a pattern
pattern = Pattern("strings:\n<(\\n)*statements>")  # or use r"\n" (in raw mode)
# pattern = patcher.pattern(...)

# Input text
text = """strings:
i like ice cream
i am dummy
wo are you?
amm"""

# Match pattern and text, print result
res = patcher.check(text, pattern)
print(res)  # {'statements': ['i like ice cream', 'i am dummy', 'wo are you?', 'amm']}
