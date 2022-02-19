# TemplateStr-Python

### TemplateStr allows to add variable, function and condition in a string.

<div align="center">
    <img src="https://img.shields.io/badge/Python-v3.8%5E-green?style=flat-square&logo=python&logoColor=ffd13e&labelColor=3470a2&color=5c5c5c"/>
    <img src="https://img.shields.io/github/downloads/CheeseGrinder/TemplateStr-Python/total?label=Download&style=flat-square"/>
    <a href="https://github.com/CheeseGrinder/TemplateStr-Python/actions/workflows/python-app.yml">
        <img src="https://img.shields.io/github/workflow/status/CheeseGrinder/TemplateStr-Python/Python test?label=Test&style=flat-square"/>
    </a>
</div>

<strong>Import : </strong>

```python
from PyTempStr import TemplateStr
```

<strong>Construtor : </strong>

```python
parser = TemplateStr(functionList: list, variableDict: dict)
```

- `functionList` : is a list of Functions you want to pass to be called in your text
- `varaibleDict` : is a dictionary of the Variables you want to pass to be called in your text

<strong>Function : </strong>

```python
parser.parse(text)
```

- `parse(text: str) -> str` : parse all (variable, function, condition and switch)
- `parseVariable(text: str) -> str` : parse Variable ; {{$variable}}
- `parseFunction(text: str) -> str` : parse Function ; {{@function}}
- `parseCondition(text: str) -> str` : parse Condition ; {{#var1 == var2: value1 || value2}}
- `parseSwitch(text: str) -> str` : parse Switch ; {{?var; value1=#0F0, 56=#00F, ..., default=#000}}
- `hasVariable(text: str) -> bool` : check if there are any Variable
- `hasFunction(text: str) -> bool` : check if there are any Function
- `hasCondition(text: str) -> bool` : check if there are any Condition
- `hasSwitch(text: str) -> bool` : check if there are any Switch

#### Exemple Syntaxe

<details>
<summary><strong>Variable</strong></summary>
</br>

The syntax of the Variables is like if : 
- `{{$variable}}` 
- `{{$dict.variable}}`
- `{{$dictM.dict1.variable. ...}}`

if the value does not exist then `None` is return

```python
from PyTempStr import TemplateStr

varDict = {
    'variable':'yes'
}

text = 'are you a variable : {{$variable}}'

parser = TemplateStr(variableDict=varDict)

print(parser.parse(text))
```

```python
from PyTempStr import TemplateStr

varDict = {
    'variable': {
        'value': 'yes'
    }
}

text = 'are you a variable : {{$variable.value}}'

parser = TemplateStr(variableDict=varDict)

print(parser.parse(text))
```

```python
variable = 'yes'

print('are you a variable : ' + variable)
```

The three codes will return

```text
are you a variable : yes
```

</details>

<details>
<summary><strong>Function</strong></summary>
</br>

The syntax of the Function is like if : `{{@function variable}}`

list of basic functions : 
- `{{@uppercase variable}}`
- `{{@uppercaseFirst variable}}`
- `{{@lowercase variable}}`
<!-- - `{{@casefold variable}}` -->
- `{{@swapcase variable}}`
- `{{@time}}`
- `{{@date}}`
- `{{@dateTime}}`

```python
from PyTempStr import TemplateStr

varDict = {'variable':'no'}

text = 'is lower case : {{@uppercase variable}}'

parser = TemplateStr(variableDict=varDict)

print(parser.parse(text))
```

```python
variable = 'no'

print('is lower case : ' + variable.upper())
```

The two codes will return

```text
is lower case : NO
```
</details>

<details>
<summary><strong>Custom Function</strong></summary>
</br>

The syntax of the Custom Function is like if : `{{@customFunction param1 param2 ...}}`

`Typing` can be used at the parameter level of custom functions

parameters to be passed in a list

the custom function must necessarily return a str

```python
from PyTempStr import TemplateStr

def customFunc(list: list) -> str:
    return list[0].replace('no', 'maybe')

text = 'are you a customFunction : {{@customFunc "no"}}'

parser = TemplateStr(functionList=[customFunc])

print(parser.parse(text))
```
The codes will return

```text
are you a customFunction : maybe
```

</details>

<details>
<summary><strong>Condition</strong></summary>
</br>

The syntax of the Condition is like if : 
- `{{#var1 == var2: value1 || value2}}`

comparator:
- `==`
- `!=`
- `<=`*
- `<`*
- `>=`*
- `>`*

*for this comparator the type `string` and `bool` are modified :
- `string` it's the number of characters that is compared ('text' = 4)
- `bool` it's the value in int that is compared (True = 1)


`var1` is compared with `var2`

`Typing` can be used at `var1` and `var2` level

```python
from PyTempStr import TemplateStr

varDict = {'var1':'no', 'var2':'o2'}

text = 'are you a variable : {{#"test" == var2: yes || no}}'

parser = TemplateStr(variableDict=varDict)

print(parser.parse(text))
```
```python
var1 = 'no'
var2 = 'o2'

if "test" == var2:
    text = 'yes'
else:
    text = 'no'
print('are you a variable : ' + text)
```

The 2 codes will return

```text
are you a variable : no
```

</details>

<details>
<summary><strong>Switch</strong></summary>
</br>

The syntax of the Switch is like if : 
- `{{?var; value1=#0F0, 56=#00F, ..., default=#000}}`
- `{{?var:type; 16=#0F0, 56=#00F, ..., default=#000}}`

`var` can be typed, if it is typed then all the `values` will be typed of the same type

type accept :
- `str`
- `int`
- `float`

```python
from PyTempStr import TemplateStr

varDict = {
    'variable':'yes'
}

text = '=( {{?variable; yes=#A, no=#B, maybe=#C, default=#000}} )='

parser = TemplateStr(variableDict=varDict)

print(parser.parse(text))
```

```python
from PyTempStr import TemplateStr

varDict = {
    'variable': 42
}

text = '=( {{?variable:int; 42=#A, 32=#B, 22=#C, default=#000}} )='

parser = TemplateStr(variableDict=varDict)

print(parser.parse(text))
```

```python
variable = 'yes'

if variable == "yes":
    result = "#A"
elif variable == "no":
    result = "#B"
elif variable == "maybe":
    result = "#C"
else
    result = "#000"

print('=( ' + result + ' )=')
```

The 3 codes will return

```text
=( #A )=
```

</details>

<details>
<summary><strong>Typing</strong></summary>
</br>

| format                       | type    | description                                                       | return                 |
|------------------------------|---------|-------------------------------------------------------------------|------------------------|
| keyVariable                  | `*`     | is the key of the value in the dictionary pass to the constructor | value of `keyVariable` |
| \<b:True>                    | `bool`  |                                                                   | True                   |
| \<n:123>                     | `int`   |                                                                   | 123                    |
| \<n:123.4>                   | `float` |                                                                   | 123.4                  |
| "text" or 'text' or \`text\` | `str`   |                                                                   | text                   |

</details>


### Install

- Download : [latest](https://github.com/CheeseGrinder/TemplateStr-Python/releases/latest)
- `pip install *.whl`

### TODO

- [ ] : Add exemple
- [x] : Add test

 
