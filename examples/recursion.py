from vbml import Pattern, Patcher
from vbml.validators import ValidatorManager

# Assign manager and patcher
manager = ValidatorManager()
patcher = Patcher()

# Create a pattern
pattern = Pattern('i am <("<a>")&shue>')  # or use r"\n" (in raw mode)
# pattern = patcher.pattern(...)

# Input text
text = "i am shue ppsh"

# Match pattern and text, print result
res = patcher.check(text, pattern)
print(res)  # {'statements': ['i like ice cream', 'i am dummy', 'wo are you?', 'amm']}
