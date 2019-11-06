# vbml

Simple usage example:

```python
from vbml import Patcher

# Init your VBML main processor
patcher = Patcher()
# Create a pattern
pattern = patcher.pattern('i am <name> my age is <age:int> years')
# Mind about text sample
text = 'i am vbml my age is 0 years'
text2 = 'amm.. some text'

# Go
print(patcher.check(text, pattern))
# >> {'name': 'vbml', 'age': 0}

print(patcher.check(text2, pattern))
# >> False
```

You can ignore check only pattern, without validator formatting:

```python
print(pattern(text))
# >> {'name': 'vbml', 'age': '0'}
```


