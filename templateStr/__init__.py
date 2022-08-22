import re as regex
from typing import Any, Pattern, Tuple
from distutils.util import strtobool
from time import strftime, localtime

from templateStr.reg import *
from templateStr.error import BadComparatorError, CustomFunctionReturnError, NotAListError, NotFoundVariableError, NotFoundFunctionError

class TemplateStr:

    __functions: list
    __variables: dict
    __regVariable: Pattern = regex.compile(REG_VARIABLE)
    __regFunction: Pattern = regex.compile(REG_FUNCTION)
    __regCondition: Pattern = regex.compile(REG_CONDITION)
    __regSwitch: Pattern = regex.compile(REG_SWITCH)
    __regTyping: Pattern = regex.compile(rf'{REG_STR}|{REG_BOOL}|{REG_INT}|{REG_FLOAT}|{REG_VAR}|{REG_LIST}')

    def __init__(self, functionList: list = [], variableDict: dict = {}):
        '''
        `functionList: list`

        `variableDict: dict`

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
                elif groupParam['int'] != None:
                    numberInt: int = int(groupParam['int'])
                    list_temp.append(numberInt)
                elif groupParam['float'] != None:
                    numberfloat: float = float(groupParam['float'])
                    list_temp.append(numberfloat)
                elif groupParam['variable'] != None:
                    if groupParam['index'] == None:
                        list_temp.append(self.__getVariable(groupParam['variable'])[0])
                    else:
                        list_temp.append(self.__getVariable(groupParam['variable'], int(groupParam['index']))[0])

                elif groupParam['list'] != None:
                    l = groupParam['list'].split(", ")
                    for i, v in enumerate(l):
                        l[i] = self.__typing(v)[0]
                    list_temp.append(l)

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

    def __getVariable(self, key: str, index: int = None) -> Tuple[Any, bool]:

        ok: bool = True

        try:
            if '.' in key and not key.isspace():
                keyList = key.split('.')
                for i, value in enumerate(keyList):
                    if i == 0:
                        temp = self.__variables[value]
                    else:
                        temp = temp[value]
                fvalue = temp
            else:
                fvalue = self.__variables[key]

        except (KeyError, TypeError):
            raise NotFoundVariableError(f"[key '{key}' not exist]")
            # ok = False
            # fvalue = f"[key '{key}' not exist]"
            # return (fvalue, ok)

        if index is not None and isinstance(fvalue, list):
            try: fvalue = fvalue[index]
            except: raise IndexError(f"[index '{index}' out of range]")
        elif index is not None:
            raise NotAListError(f"[key '{key}' is not list]")
            # ok = False
            # fvalue = f"[key '{key}' is not list]"

        return (fvalue, ok)

    def parse(self, text: str) -> str:
        '''
        shortcuts to run all parsers

        return -> str
        '''
        while self.hasOne(text):
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
        parse all the `${variable}` or `${variable[1]}` in the text give in

        return -> str
        '''

        if not self.hasVariable(text): return text

        # parse Variable
        while self.hasVariable(text):
            for m in self.__regVariable.finditer(text):
                group: dict = m.groupdict()

                match: str = group['match']
                key: str = group['variable']
                var: Any
                if group['index'] == None:
                    var = self.__getVariable(key)[0]
                else:
                    var = self.__getVariable(key, int(group['index']))[0]

                text = text.replace(match, str(var))

        return text

    def parseFunction(self, text: str) -> str:
        '''
        parse all the `{{@function param1 param2}}` or `{{@function}}` in the text give in

        return -> str
        '''

        if not self.hasFunction(text): return text

        # parse Function
        while self.hasFunction(text):
            for m in self.__regFunction.finditer(text):
                group: dict = m.groupdict()

                match: str = group['match']
                parameters: str = group['parameters']

                value: str = "none"

                v: Tuple = self.__getVariable(parameters)

                if parameters != None and v[1]:
                    value = v[0]

                functionName: str = group['functionName']

                if functionName == 'uppercase': text = text.replace(match, value.upper())
                elif functionName == 'uppercaseFirst': text = text.replace(match, value.capitalize())
                elif functionName == 'lowercase': text = text.replace(match, value.lower())
                # elif functionName == 'casefold': text = text.replace(match, value.casefold())
                elif functionName == 'swapcase': text = text.replace(match, value.swapcase())
                elif functionName == 'time': text = text.replace(match, strftime("%H:%M:%S", localtime()))
                elif functionName == 'date': text = text.replace(match, strftime("%d/%m/%Y", localtime()))
                elif functionName == 'dateTime': text = text.replace(match, strftime("%d/%m/%Y,%H:%M:%S", localtime()))
                elif functionName in str(self.__functions):
                    for func in self.__functions:
                        
                        if regex.search(r'(?<!\S){}(?!\S)'.format(functionName), str(func)) != None:

                            if parameters != None:

                                listParametre: list = self.__typing(parameters)

                                method = {func:func}
                                resultTextfunc = method[func](listParametre)
                            else:
                                method = {func:func}
                                resultTextfunc = method[func]()

                            if resultTextfunc != None:
                                text = text.replace(m.groupdict()['match'], resultTextfunc)
                            else:
                                raise CustomFunctionReturnError(f'[Function {functionName} must return a string]')
                else:
                    raise NotFoundFunctionError(f'[Function {functionName} not exist]')
            
        return text

    def parseCondition(self, text: str) -> str:
        '''
        parse all the `{{#var1 == var2; value1 | value2}}` in the text give in

        return -> str
        '''

        if not self.hasCondition(text): return text

        # parse Condition
        while self.hasCondition(text):
            for m in self.__regCondition.finditer(text):
                group: dict = m.groupdict()

                match = group['match']
                conditionValue1 = group['conditionValue1']
                conditionValue2 = group['conditionValue2']
                conditionSymbol = group['conditionSymbol']
                trueValue = group['trueValue']
                falseValue = group['falseValue']

                listTyping = self.__typing(conditionValue1 + " " + conditionValue2)

                if conditionSymbol == "==":
                    text = text.replace(match, trueValue if listTyping[0] == listTyping[1] else falseValue)
                elif conditionSymbol == "!=":
                    text = text.replace(match, trueValue if listTyping[0] != listTyping[1] else falseValue)
                else:
                    value1, value2 = self.__convertAnyToFloat(listTyping[0], listTyping[1])
                    if conditionSymbol == "<=":
                        text = text.replace(match, trueValue if value1 <= value2 else falseValue)
                    elif conditionSymbol == ">=":
                        text = text.replace(match, trueValue if value1 >= value2 else falseValue)
                    elif conditionSymbol == "<":
                        text = text.replace(match, trueValue if value1 < value2 else falseValue)
                    elif conditionSymbol == ">":
                        text = text.replace(match, trueValue if value1 > value2 else falseValue)
                    else:
                        raise BadComparatorError(f'[{conditionSymbol} is not valid comparator]')

        return text

    def parseSwitch(self, text: str) -> str:
        '''
        parse all the `{{?var; value1=#0F0, 56=#00F, ..., default=#000}}` or `{{?var:int; 56=#0F0, 32=#00F, ..., default=#000}}` in the text give in

        return -> str
        '''

        if not self.hasSwitch(text): return text

        # parse Switch
        while self.hasSwitch(text):
            for m in self.__regSwitch.finditer(text):
                group: dict = m.groupdict()

                match = group['match']

                dictTemp = {}

                for n in group["values"].split(", "):
                    key, value = n.split("::")
                    dictTemp[key] = value


                if group['variable'] != None:
                    keyVar = group['variable']

                    for key in dictTemp.keys():
                        
                        if key == str(self.__getVariable(keyVar)[0]):
                            result = dictTemp[key]
                            break
                        else:
                            result = group['defaultValue']

                elif group['type'] != None:
                    typeVar = group['type']

                    for key in dictTemp.keys():
                        
                        if self.__typing(key, typeVar)[0] == self.__getVariable(keyVar)[0]:
                            result = dictTemp[key]
                            break
                        else:
                            result = group['defaultValue']

                text = text.replace(match, result)

        return text

    def hasOne(self, text: str) -> bool:
        '''
        Detects if there is the presence of min one syntaxe

        return -> bool
        '''

        if self.hasVariable(text) or self.hasFunction(text) or self.hasCondition(text) or self.hasSwitch(text):
            return True
        return False

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
