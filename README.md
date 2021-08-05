# TemplateStr-Python

### TemplateStr allows to add variable, function and condition in a string, useful in config files.

<strong>Construtor : </strong>

```python
parser = TemplateStr(functionList: list, variableDict: dict)
```

- `functionList` : is a list of functions you want to pass to be called in your text
- `varaibleDict` : is a dictionary of the variables you want to pass to be called in your text

<strong>Function : </strong>

```python
parser.parse(text)
```

- `parse() -> str` : parse all (variable function and condition)
- `parseVariable() -> str` : parse variable ; {{$variable}}
- `parseFunction() -> str` : parse Function ; {{@function}}
- `parseCondition() -> str` : parse variable ; {{#condition var}} value {{else}} value {{condition#}}
- `hasVariable() -> Tuple[bool, list]` : check if there are any variables
- `hasFunction() -> Tuple[bool, list]` : check if there are any function
- `hasCondition() -> Tuple[bool, list]` : check if there are any condition

<details>
<summary><strong>Variable</strong></summary>

The syntax of the variables is like if : `{{$variable}}`


```python
from tempStr import TemplateStr

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

The syntax of the function is like if : `{{@function variable}}`

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
from tempStr import TemplateStr

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

The syntax of the custom function is like if : `{{@customFunction param1 param2}}`

parameters to be passed in a list

param type:
| format                       | type    | description                                                       | return                 |
|------------------------------|---------|-------------------------------------------------------------------|------------------------|
| keyVariable                  | `*`     | is the key of the value in the dictionary pass to the constructor | value of `keyVariable` |
| \<b:True>                    | `bool`  |                                                                   | True                   |
| \<i:123>                     | `int`   |                                                                   | 123                    |
| \<i:123.4>                   | `float` |                                                                   | 123.4                  |
| "text" or 'text' or \`text\` | `str`   |                                                                   | text                   |


the custom function must necessarily return a str

```python
from tempStr import TemplateStr

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

The syntax of the condition is like if : `{{#test variable}} value1 {{else}} value2 {{test#}}`

`#test` is the str that will be compared with the value of the `variable`

```python
from tempStr import TemplateStr

varDict = {'variable':'no'}

text = 'are you a variable : {{#test variable}} yes {{else}} no {{test#}}'

parser = TemplateStr(variableDict=varDict)

print(parser.parse(text))
```
```python
variable = 'no'

if 'test' == variable:
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

### Install

- Download : [latest](https://github.com/CheeseGrinder/TemplateStr-Python/releases/latest)
- `pip install *.whl`

### TODO

- [ ] : Add exemple

 