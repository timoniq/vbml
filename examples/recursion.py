from vbml import Pattern, Patcher

# Assign manager and patcher
patcher = Patcher()

# Create a pattern
pattern = Pattern('i am <("<a> <b>")&shue>')  # or use r"\n" (in raw mode)
# pattern = patcher.pattern(...)

# Input text
text = "i am shue ppsh"

# Match pattern and text, print result
res = patcher.check(text, pattern)
print(res)  # {'shue': {'a': 'shue', 'b': 'ppsh'}}
