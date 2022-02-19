import sys
import re as regex
from typing import Any, Pattern, Tuple
from distutils.util import strtobool
from time import strftime, localtime

class TemplateStr:

    __functions: list
    __variables: dict
    __regVariable: Pattern = regex.compile(r'(?P<match>{{\$(?P<key>[^{$}]+)}})')
    __regFunction: Pattern = regex.compile(r'(?P<match>{{@(?P<function>[^{@}\s]+) ?(?P<key>[^{@}]+)?}})')
    __regCondition: Pattern = regex.compile(r'(?P<match>{{#(?P<compValue1>[^{#}]+) (?P<compSymbol>[=!<>][=]?) (?P<compValue2>[^{#}]+): (?P<resultValue1>[^{}]+) \|\| (?P<resultValue2>[^{}]+)}})')
    __regSwitch: Pattern = regex.compile(r'(?P<match>{{\?(?:(?P<key>[^{?}:]+)|(?P<keyTyped>[^{?}]+):(?P<type>str|int|float)); (?P<val>(?:[^{}]+)=(?:[^{}]+)), default=(?P<default>[^{}]+)}})')
    __regTyping: Pattern = regex.compile(r'\"(?P<str_double>[^\"]+)\"|\'(?P<str_single>[^\']+)\'|`(?P<str_back>[^`]+)`|<b:(?P<bool>True|False)>|<n:(?P<number>[0-9_.]+)>|(?P<variable>[^<>\" ]+)')

    def __init__(self, functionList: list = [], variableDict: dict = {}):
        '''
        `functionList: list` is a list of custom functions that can be used when you call a function with: `{{@myCustomFunction}}`

        `variableDict: dict` is a dictionary of the values you want to use when you call: `{{$myVar}}`

        Typing:
            keyVariable  : is the key of the value in the dictionary pass to the constructor (return the value)
            <b:True>     : bool  (return True)
            <n:123>      : int   (return 123)
            <n:123.4>    : float (return 123.4)
            "text"       : str   (return text)
        '''

        self.__functions = functionList
        self.__variables = variableDict

    def __presence(self, listTuple: list) -> bool:
        if listTuple != []:
            return True
        else:
            return False

    def __convertAnyToFloat(self, value1: Any, value2: Any) -> Tuple[float, float]:

        result1: float = 0.0
        result2: float = 0.0

        if isinstance(value1, int) or isinstance(value1, float):
            result1 = float(value1)
        elif isinstance(value1, bool):
            result1 = float(int(value1 == True))
        elif isinstance(value1, str):
            result1 = float(len(value1))
        
        if isinstance(value2, int) or isinstance(value2, float):
            result2 = float(value2)
        elif isinstance(value2, bool):
            result2 = float(int(value2 == True))
        elif isinstance(value2, str):
            result2 = float(len(value2))

        return (result1, result2)

    def __typing(self, string: str, typing: str = "False") -> list:

        list_temp: list = []

        if typing == "False":
            for m in self.__regTyping.finditer(string):
                groupParam: dict = m.groupdict()

                if groupParam['str_double'] != None:
                    list_temp.append(groupParam['str_double'])
                elif groupParam['str_single'] != None:
                    list_temp.append(groupParam['str_single'])
                elif groupParam['str_back'] != None:
                    list_temp.append(groupParam['str_back'])
                elif groupParam['bool'] != None:
                    typeBool: bool = bool(strtobool(groupParam['bool']))
                    list_temp.append(typeBool)
                elif groupParam['number'] != None:
                    if '.' in groupParam['number']:
                        number: float = float(groupParam['number'])
                    else:
                        number: int = int(groupParam['number'])
                    list_temp.append(number)
                elif groupParam['variable'] != None:
                    list_temp.append(str(self.__getVariable(groupParam['variable'])))

        elif typing == "int":
            number: int = int(string)
            list_temp.append(number)

        elif typing == "float":
            number: float = float(string)
            list_temp.append(number)

        elif typing == "str":
            typeStr: str = str(string)
            list_temp.append(typeStr)

        elif typing == "bool":
            typeBool: bool = bool(string)
            list_temp.append(typeBool)

        return list_temp

    def __getVariable(self, key: str) -> Any:
        try:
            if '.' in key and not key.isspace():
                keyList = key.split('.')
                for index, value in enumerate(keyList):
                    if index == 0:
                        temp = self.__variables[value]
                    else:
                        temp = temp[value]
                fvalue = temp
            else:
                fvalue = self.__variables[key]
        except KeyError:
            fvalue = "None"

        return fvalue

    def parse(self, text: str) -> str:
        '''
        shortcuts to run all parsers

        return -> str
        '''

        # parse Variable
        text = self.parseVariable(text)

        # parse Function
        text = self.parseFunction(text)

        # parse Condition
        text = self.parseCondition(text)

        # parse Condition
        text = self.parseSwitch(text)

        return text

    def parseVariable(self, text: str) -> str:
        '''
        parse all the `{{$variable}}` in the text give in

        return -> str
        '''

        if not self.hasVariable(text): return text

        # parse Variable
        for m in self.__regVariable.finditer(text):
            group: dict = m.groupdict()

            match: str = group['match']
            key: str = group['key']

            text = text.replace(match, str(self.__getVariable(key)))

        return text

    def parseFunction(self, text: str) -> str:
        '''
        parse all the `{{@function param1 param2}}` or `{{@function}}` in the text give in

        return -> str
        '''

        if not self.hasFunction(text): return text

        # parse Function
        for m in self.__regFunction.finditer(text):
            group: dict = m.groupdict()

            match: str = group['match']
            key: str = group['key']



            if key != None and self.__getVariable(key) != "None":
                value: str = self.__getVariable(key)

            functionName: str = group['function']

            if functionName == 'uppercase': text = text.replace(match, value.upper())
            elif functionName == 'uppercaseFirst': text = text.replace(match, value.capitalize())
            elif functionName == 'lowercase': text = text.replace(match, value.lower())
            elif functionName == 'casefold': text = text.replace(match, value.casefold())
            # elif functionName == 'swapcase': text = text.replace(match, value.swapcase())
            elif functionName == 'time': text = text.replace(match, strftime("%H:%M:%S", localtime()))
            elif functionName == 'date': text = text.replace(match, strftime("%d/%m/%Y", localtime()))
            elif functionName == 'dateTime': text = text.replace(match, strftime("%d/%m/%Y,%H:%M:%S", localtime()))
            elif functionName in str(self.__functions):
                for func in self.__functions:
                    
                    if regex.search(r'(?<!\S){}(?!\S)'.format(functionName), str(func)) != None:

                        if key != None:

                            listParametre: list = self.__typing(key)

                            method = {func:func}
                            resultTextfunc = method[func](listParametre)
                        else:
                            method = {func:func}
                            resultTextfunc = method[func]()

                        if resultTextfunc != None:
                            text = text.replace(m.groupdict()['match'], resultTextfunc)
                        else:
                            sys.exit('The '+ functionName + ' function must return a string')
            else:
                sys.exit('The ' + functionName + ' function does not exist')
        
        return text

    def parseCondition(self, text: str) -> str:
        '''
        parse all the `{{#var1 == var2: value1 || value2}}` in the text give in

        return -> str
        '''

        if not self.hasCondition(text): return text

        # parse Condition
        for m in self.__regCondition.finditer(text):
            group: dict = m.groupdict()

            match = group['match']
            compValue1 = group['compValue1']
            compValue2 = group['compValue2']
            compSymbol = group['compSymbol']
            resultValue1 = group['resultValue1']
            resultValue2 = group['resultValue2']

            listTyping = self.__typing(compValue1 + " " + compValue2)

            if compSymbol == "==":
                text = text.replace(match, resultValue1 if listTyping[0] == listTyping[1] else resultValue2)
            elif compSymbol == "!=":
                text = text.replace(match, resultValue1 if listTyping[0] != listTyping[1] else resultValue2)
            else:
                value1, value2 = self.__convertAnyToFloat(listTyping[0], listTyping[1])
                if compSymbol == "<=":
                    text = text.replace(match, resultValue1 if value1 <= value2 else resultValue2)
                elif compSymbol == ">=":
                    text = text.replace(match, resultValue1 if value1 >= value2 else resultValue2)
                elif compSymbol == "<":
                    text = text.replace(match, resultValue1 if value1 < value2 else resultValue2)
                elif compSymbol == ">":
                    text = text.replace(match, resultValue1 if value1 > value2 else resultValue2)
                else:
                    sys.exit('The ' + compSymbol + ' is not a valid comparator')

        return text

    def parseSwitch(self, text: str) -> str:
        '''
        parse all the `{{?var; value1=#0F0, 56=#00F, ..., default=#000}}` or `{{?var:int; 56=#0F0, 32=#00F, ..., default=#000}}` in the text give in

        return -> str
        '''

        if not self.hasSwitch(text): return text

        for m in self.__regSwitch.finditer(text):
            group: dict = m.groupdict()

            match = group['match']

            dictTemp = {}

            for n in group["val"].split(", "):
                key, value = n.split("=")
                dictTemp[key] = value


            if group['key'] != None:
                keyVar = group['key']

                for key in dictTemp.keys():
                    
                    if key == str(self.__getVariable(keyVar)):
                        result = dictTemp[key]
                        break
                    else:
                        result = group['default']

            elif group['keyTyped'] != None:
                keyVar = group['keyTyped']
                typeVar = group['type']

                for key in dictTemp.keys():
                    
                    if self.__typing(key, typeVar)[0] == self.__getVariable(keyVar):
                        result = dictTemp[key]
                        break
                    else:
                        result = group['default']

            text = text.replace(match, result)

        return text

    def hasVariable(self, text: str) -> bool:
        '''
        Detects if there is the presence of `{{$variable}}`

        return -> bool
        '''

        find: list = regex.findall(self.__regVariable, text)
        return self.__presence(find)

    def hasFunction(self, text: str) -> bool:
        '''
        Detects if there is the presence of `{{@function param1 param2}}` or `{{@function}}`

        return -> bool
        '''

        find: list = regex.findall(self.__regFunction, text)
        return self.__presence(find)

    def hasCondition(self, text: str) -> bool:
        '''
        Detects if there is the presence of `{{#var1 == var2: value1 || value2}}`

        return -> bool
        '''

        find: list = regex.findall(self.__regCondition, text)
        return self.__presence(find)
    
    def hasSwitch(self, text: str) -> bool:
        '''
        Detects if there is the presence of `{{?var: value1=#0F0, value2=#00F, ..., default=#000}}` or
        `{{?var:int; 56=#0F0, 32=#00F, ..., default=#000}}`

        return -> bool
        '''

        find: list = regex.findall(self.__regSwitch, text)
        return self.__presence(find)

