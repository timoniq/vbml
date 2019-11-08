# vbml

To install use this command:

```shell
pip install https://github.com/timoniq/vbml/archive/master.zip --upgrade
```

To add this project to your project requirements:

* add string **-e https://github.com/timoniq/vbml/archive/master.zip** to your requirements file

* add element **vbml @ https://github.com/timoniq/vbml/archive/master.zip** to your install_requires list

Simple usage example:

```python
from vbml import Patcher
import typing
from vbml.validators import ValidatorManager, AbstractAsynchronousValidator


class MyValidator(AbstractAsynchronousValidator):
    key = "int"

    async def check(self, text: str, *args) -> typing.Union[typing.Any, None]:
        if text.isdigit():
            return int(text)


# Init your VBML main processor
manager = ValidatorManager([MyValidator()])
patcher = Patcher()
# Create a pattern
pattern = patcher.pattern("i am <name> my age is <age:int> years")
# Mind about text sample
text = "i am vbml my age is 0 years"
text2 = "amm.. some text"


def main():
    # Go
    print(patcher.check(text, pattern))
    # >> {'name': 'vbml', 'age': 0}

    print(patcher.check(text2, pattern))
    # >> None


main()
```

You can ignore check only pattern, without validator formatting:

```python
print(pattern(text))
# >> {'name': 'vbml', 'age': '0'}
```

Made with :heart:love by [timoniq](https://github.com/timoniq)
