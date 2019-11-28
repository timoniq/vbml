# 

<h1 align="center">VBML: can i help you?</h1>
<p align="center"><a href="https://vk.me/join/AJQ1d4n6rRVBAR2PGh8zChFS"><img src="https://img.shields.io/static/v1?message=VK%20Chat&label=&color=blue"></a>
    <blockquote>VBML - it is a strong, easy, fast and full-functionality module for parsing and splitting messages to the smaller parts by just two strings - pattern and compared text</blockquote>
</p>
<hr>

### Features

* Fast and asynchronous parser
* Abstract validators support
* Easy and intellectually clear parser:

### `I am <name>`
### `I am VBML`
### `{"name": "VBML"}`

### Installation
To install use this command:

```shell
pip install https://github.com/timoniq/vbml/archive/master.zip --upgrade
```
or:  

```shell
pip install vbml
```

To add this project to your project requirements:

* add string `vbml` to your requirements file

* add element `vbml` to your install_requires list

### Documentation

You can find full documentation at [wiki pages](https://github.com/timoniq/vbml/wiki/VBML-Usage)

Simple usage example:

```python
from vbml import Patcher
from vbml.validators import ValidatorManager, AbstractAsynchronousValidator


class MyValidator(AbstractAsynchronousValidator):
 key = "int"

 async def check(self, text: str, *args):
     valid = text.isdigit()
     if valid:
         return int(text)


# Init your VBML main processor
manager = ValidatorManager([MyValidator()])

patcher = Patcher()
# Create a pattern
pattern = patcher.pattern("i am <name> and i love <item>")
# Mind about text sample
text = "i am vasya and i love ice cream"
text2 = "amm.. some text"


def main():
    # Go
    print(patcher.check(text, pattern))
    # >> {'name': 'vasya', 'item': 'ice cream'}

    print(patcher.check(text2, pattern))
    # >> None


main()
```

UPD: Documentation was copied into [/docs folder](/docs)

Made with :heart: love by [timoniq](https://github.com/timoniq)
