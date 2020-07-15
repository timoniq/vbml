# vbml - beautiful parser :sparkles:

## Features

* Fast parser based on `regex`
* Validation support
* Easy and intellectually clear parser:

Pattern `I am <name>` + Text `I am VBML` = `{"name": "VBML"}`

## Installation

Install with pip:

```shell
pip install vbml
```


## Documentation

You can find full documentation [here](/docs)

Make validators:

```python
from vbml import PatchedValidators


class Validators(PatchedValidators):
    def int(self, text: str, *args):
        valid = text.isdigit()
        if valid:
            return int(text)
```

Init patcher and make a simple pattern:

```python
from vbml import Patcher

patcher = Patcher(validators=Validators)
pattern = patcher.pattern("i am <name> and i love <item>")
```

Match texts:

```python
>> patcher.check("i am vasya and i love ice cream", pattern)
{'name': 'vasya', 'item': 'ice cream'}

>> patcher.check("damn) haha lmfao, lol!", pattern)
None
```

Made with :heart: by [timoniq](https://github.com/timoniq)
