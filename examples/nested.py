from vbml import Pattern, Patcher

# Assign manager and patcher
patcher = Patcher()

# Create a pattern
pattern = Pattern('i am <("<first_name> <second_name>")&name>')  # or use r"\n" (in raw mode)

text = "i am Arsenii Timoniq"

res = patcher.check(text, pattern)
print(res)  # {'name': {'first_name': 'Arsenii', 'second_name': 'Timoniq'}}
