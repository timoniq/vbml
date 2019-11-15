# 

<h1 align="center">VBML: can i help you?</h1>
<p align="center"><a href="https://pypi.org/project/vkbottle/"><img alt="downloads" src="https://img.shields.io/static/v1?label=pypi%20package&message=0.13&color=brightgreen"></a> <a href="https://github.com/timoniq/vkbottle"><img src="https://img.shields.io/static/v1?label=version&message=opensource&color=yellow" alt="service-test status"></a> <a href="https://vk.me/join/AJQ1d4n6rRVBAR2PGh8zChFS"><img src="https://img.shields.io/static/v1?message=VK%20Chat&label=&color=blue"></a>
    <blockquote>VBML - it is a strong, easy, fast and full-functionality module for parsing and splitting messages to the smaller parts by just two strings - pattern and compared text</blockquote>
</p>
<hr>

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

You don't need to assign special version because syntax in all versions of VBML is similar

### Documentation

You can find full documentation at [wiki](https://github.com/timoniq/vbml/wiki/VBML-Usage)

Simple usage example:

```python
from vbml import Patcher

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

Made with :heart: love by [timoniq](https://github.com/timoniq)
