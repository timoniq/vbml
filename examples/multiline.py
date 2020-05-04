from vbml import Pattern, Patcher

patcher = Patcher()

pattern = Pattern("strings:\n<(\\n)*statements>")  # or use r"\n" (in raw mode)

text = """strings:
i like ice cream
i am dummy
wo are you?
amm"""

res = patcher.check(text, pattern)
print(res)  # {'statements': ['i like ice cream', 'i am dummy', 'wo are you?', 'amm']}
