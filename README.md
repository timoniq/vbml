# 

<h1 align="center">VBML: can i help you?</h1>
<p align="center"><a href="https://vk.me/join/AJQ1d4n6rRVBAR2PGh8zChFS"><img src="https://img.shields.io/static/v1?message=VK%20Chat&label=&color=blue"></a>
    <blockquote>VBML - it is a strong, easy, fast and full-functionality module for parsing and splitting messages to the smaller parts by just two strings - pattern and compared text</blockquote>
</p>
<hr>

### Features

* Fast parser based on `regex`
* Validation support
* Easy and intellectually clear parser:

### `I am <name>`
### `I am VBML`
### `{"name": "VBML"}`

### Installation
To install use this command:

```shell
pip install vbml
```


### Documentation

You can find full documentation at [wiki pages](https://github.com/timoniq/vbml/wiki/VBML-Usage)

Simple usage example:

```python
from vbml import Patcher
from vbml import PatchedValidators


class Validators(PatchedValidators):

    def int(self, text: str, *args):
        valid = text.isdigit()
        if valid:
         return int(text)


patcher = Patcher(validators=Validators)
# Create a pattern
pattern = patcher.pattern("i am <name> and i love <item>")
# Mind about text sample
text = "i am vasya and i love ice cream"
text2 = "amm.. some text"

print(patcher.check(text, pattern))
# >> {'name': 'vasya', 'item': 'ice cream'}

print(patcher.check(text2, pattern))
# >> None

```

UPD: Documentation was copied into [/docs folder](/docs)

Made with :heart: love by [timoniq](https://github.com/timoniq)
