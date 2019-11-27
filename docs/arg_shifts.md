# What argument is
## Make argument
Argument is a simple matching object that is going to be received by pattern. Main argument syntax is: 
```smalltalk
my name is <name>
```
`<name>` means that argument with name `name` will be returned after text matching
## Validators to argument
There is an opportunity to add a validator to the argument
```smalltalk
my age is <age:int>
```
of course we can attach arguments to the validators
```smalltalk
my age is <age:validator[abc]>
```

## Advanced arguments
**Advanced arguments** - arguments which validate information without validators usage
### Unions
Example:
```python
pattern = Pattern("I love <( and )*what>")
print(pattern("I love ice cream and you")) # {"what": ["ice cream", "you"]}
```
**Inclusion value** is splitter. If inclusion is not indicated, splitter will be appointed to the space symbol:  
`I am <*name>` + `I am Marie de Agata` = `{"name": ["Marie", "de", "Agata"]}`  

**Naming after union symbol** is argument name. If naming is not indicated, union will be returned with default union name: `_union`

If value is assigned with validator, list of values will be passed to the validator instead of str value (so validators for union should be special or validators should have corresponding check for value type

### Symbols
Example:
```python
pattern = Pattern("My blood RH is <(+-)^rh>")
print(pattern("My blood RH is +")) # {"rh": "+"}
```
**Inclusion value** is allowed symbols

**Naming after char match symbol** is argument name. If naming is not indicated, char match will be returned with default char match name: `char`

Validators is OK

### Denied symbols
Example:
```python
pattern = Pattern("I am <( )#name> <( )#surname>")
print(pattern("I am Marie Agata")) # {"name": "Marie", "surname": "Agata"}
print(pattern("I am Marie de Agata")) # None
```
**Inclusion value** is denied symbols

**Naming after denied-match symbol** is argument name. If naming is not indicated, exception will be raised

Validators is OK

### Regex minified pattern
Example:
```python
pattern = Pattern("omg <([a-zA-Z1-9]{0,5})$>")
print(pattern("omg ash")) # {}
print(pattern("omg helicopter")) # None
```
**Inclusion value** is regex pattern

**Naming after regex-match symbol** is not needed
