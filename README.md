# TemplateStr-Python

### TemplateStr allows to add variable, function and condition in a string, useful in config files.

![Python](https://img.shields.io/badge/Python-v3.8%5E-green?style=flat-square&logo=python&logoColor=00ccff)

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

- `parse(text: str) -> str` : parse all (variable function and condition)
- `parseVariable(text: str) -> str` : parse Variable ; {{$variable}}
- `parseFunction(text: str) -> str` : parse Function ; {{@function}}
- `parseCondition(text: str) -> str` : parse Condition ; {{#var1 == var2: value1 || value2 }}
- `hasVariable(text: str) -> Tuple[bool, list]` : check if there are any Variable
- `hasFunction(text: str) -> Tuple[bool, list]` : check if there are any Function
- `hasCondition(text: str) -> Tuple[bool, list]` : check if there are any Condition

<details>
<summary><strong>Variable</strong></summary>
</br>

The syntax of the Variables is like if : `{{$variable}}`


```python
from PyTempStr import TemplateStr

varDict = {'variable':'yes'}

text = 'are you a variable : {{$variable}}'

parser = TemplateStr(variableDict=varDict)

print(parser.parse(text))
```

```python
variable = 'yes'

print('are you a variable : ' + variable)
```

The two codes will return

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
- `{{@casefold variable}}`
- `{{@swapcase variable}}`
- `{{@time}}`
- `{{@date}}`
- `{{@dateTime}}`

```python
from PyTempStr import TemplateStr

varDict = {'variable':'no'}

text = 'are you a variable : {{@uppercase variable}}'

parser = TemplateStr(variableDict=varDict)

print(parser.parse(text))
```

```python
variable = 'no'

print('are you a variable : ' + variable.upper())
```

The two codes will return

```text
are you a variable : NO
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

text = 'are you a variable : {{@customFunc "no"}}'

parser = TemplateStr(functionList=[customFunc])

print(parser.parse(text))
```
Return

```text
are you a variable : maybe
```

</details>

<details>
<summary><strong>Condition</strong></summary>
</br>

The syntax of the Condition is like if : `{{#var1 == var2: value1 || value2 }}`

comparator:
- `==`
- `!=`
- `<=`
- `<`
- `>=`
- `>`

`var1` is compared with `var2`

`Typing` can be used at `var1` and `var2` level

```python
from PyTempStr import TemplateStr

varDict = {'var1':'no', 'var2':'o2'}

text = 'are you a variable : {{#"test" == var2: yes || no }}'

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

The two codes will return

```text
are you a variable : no
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
- [ ] : Add test

 
