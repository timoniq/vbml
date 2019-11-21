## `Pattern` usage
First purpose of `VBML` is splitting text with patterned scheme of arguments  
Arguments in VBML can be assigned with `<>` operators. To define argument make your argument behind the operators:
```python
from vbml import Pattern
# Create a pattern
pattern = Pattern("define <qwerty>")
```
Now argument `qwerty` is going to be returned after text pattern matching:  
```python
# Match pattern with text
matching = pattern("define hello")
print(matching) # True
```
Distance between 2 arguments should be not less than one symbol:  
:-1: `<arg1><arg2>`  
:corn: `<arg1> <arg2>`  

After pattern matching with text, matching save as pregmatch value in it, pregmatch can be received by the `pattern.dict()`.  
Text escapes with regex escape `\.*+?()[]|^${}`. 

After pattern matching dict with arguments can be retrieved like this:  
```python
pattern = Pattern("define <qwerty>")
if pattern("define hello"):
    print(pattern.dict()) # {"qwerty": "hello"}
else:
    print("matching failed")
```
### Pattern options
3 Options are available for `Pattern`: main option `text`, `pattern` and `lazy`  
**text** - main pattern for VBML  
**pattern** - regex pattern, can be used instead of VBML (`text`), pattern is going to be formatted with `text`. It is needed to make pattern case ignorable, change mode of matching  
**lazy** - change mode of arguments:  

If `lazy` is `True` - `Pattern("I am <name> <surname>")` with text `I am Kate Isobelle Furler` will be matched with dict `{"name": "Kate", "surname": "Isobelle Furler"}` (**default**)

If `lazy` is `False` - `Pattern("I am <name> <surname>")` with text `I am Kate Isobelle Furler` will be matched with dict `{"name": "Kate Isobelle", "surname": "Furler"}`

## `Patcher` usage
Patcher is `Pattern` comfortable wrapper. It supports validators. `ValidatorManager` is required to work with patcher. Lets import something:
```python
from vbml import Patcher
from vbml.validators import ValidatorManager, AbstractSyncValidator
```
### Abstract validators creation
Firstly, make an abstract validator:  
```python
# ...
class MyValidator(AbstractAsynchronousValidator):
    key = "int" # key is name of your validator

    async def check(self, text: str, *args):
        # Check function is main function of your validator 
        # text is value of argument
        valid = text.isdigit()
            if valid:
                # If validator returns something
                return int(text)
```
Than, create a manager:  
```python
# ...
manager = ValidatorManager([MyValidator()])
```
**Validator is ready!**

### Patched Validators creation
Instead of an abstract class for each validator, patched validators can be assigned only in one class.  
Main rule for Patched Validators - your custom validators class should inherit standard `PatchedValidators` class:
```python
from vbml import PatchedValidators, Patcher, Pattern

class MyValidators(PatchedValidators):
    def my_validator(value: str, *args): # Name of validator is name of function
        print('oh my god! received value', value)
        return value
``` 
`PatchedValidators` custom class can be only one:  
```python
# ...
manager = ValidatorManager(MyValidators)
```
**Validators are ready!**

### Check patterns with patcher
```python
# ...
pattern = Pattern("i am <age:int> years old")
patcher = Patcher()
if patcher.check("i am 5 years old", pattern):
    print(pattern.dict()) # {"age": 5}
else:
    print("fail!")
```
