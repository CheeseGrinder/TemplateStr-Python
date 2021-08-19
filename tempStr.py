import sys
import re as regex
from typing import Pattern, Tuple
from distutils.util import strtobool
from time import strftime, localtime

class TemplateStr:

    __functions: list
    __variables: dict
    __regVariable: Pattern = regex.compile(r'(?P<match>{{\$(?P<key>[^{{$}}]+)}})')
    __regFunction: Pattern = regex.compile(r'(?P<match>{{@(?P<function>[^{@}\s]+) ?(?P<key>[^{@}]+)?}})')
    __regCondition: Pattern = regex.compile(r'(?P<match>{{#(?P<compValue1>[^{#}]+) (?P<compSymbol>[=!<>][=]?) (?P<compValue2>[^{#}]+): (?P<resultValue1>[^{}]+) \|\| (?P<resultValue2>[^{}]+) }})')
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

    def __presence(self, lists: list) -> Tuple[bool, list]:
        presences: list = []
        if lists != []:
            for value in lists:
                presences.append(value[0])
            
            return (True, presences)
        else:
            return (False, lists)

    def __convertAnyToFloat(self, value1, value2) -> Tuple[float, float]:

        if isinstance(value1, int) or isinstance(value1, float):
            if isinstance(value2, int) or isinstance(value2, float):
                return (float(value1), float(value2))
            elif isinstance(value2, bool):
                return (float(value1), float(int(value2 == True)))
            elif isinstance(value2, str):
                return (float(value1), float(len(value2)))
            else:
                return (0, 0)
        elif isinstance(value1, bool):
            value1 = float(int(value1 == True))
            if isinstance(value2, int) or isinstance(value2, float):
                return (value1, float(value2))
            elif isinstance(value2, bool):
                return (value1, float(int(value2 == True)))
            elif isinstance(value2, str):
                return (value1, float(len(value2)))
            else:
                return (0, 0)
        elif isinstance(value1, str):
            value1 = float(len(value1))
            if isinstance(value2, int) or isinstance(value2, float):
                return (value1, float(value2))
            elif isinstance(value2, bool):
                return (value1, float(int(value2 == True)))
            elif isinstance(value2, str):
                return (value1, float(len(value2)))
            else:
                return (0, 0)
        else:
            return (0, 0)

    def __typing(self, string: str) -> list:

        list_temp: list = []

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
                list_temp.append(str(self.__variables[groupParam['variable']]))

        return list_temp

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

        return text

    def parseVariable(self, text: str) -> str:
        '''
        parse all the `{{$variable}}` in the text give in

        return -> str
        '''

        if not self.hasVariable(text)[0]: return text

        # parse Variable
        for m in self.__regVariable.finditer(text):
            group: dict = m.groupdict()

            match: str = group['match']
            key: str = group['key']

            text = text.replace(match, str(self.__variables[key]))

        return text

    def parseFunction(self, text: str) -> str:
        '''
        parse all the `{{@function param1 param2}}` or `{{@function}}` in the text give in

        return -> str
        '''

        if not self.hasFunction(text)[0]: return text

        # parse Function
        for m in self.__regFunction.finditer(text):
            group: dict = m.groupdict()

            match: str = group['match']

            if group['key'] != None and group['key'] in self.__variables: key: str = self.__variables[group['key']]
            functionName: str = group['function']

            if functionName == 'uppercase': text = text.replace(match, key.upper())
            elif functionName == 'uppercaseFirst': text = text.replace(match, key.capitalize())
            elif functionName == 'lowercase': text = text.replace(match, key.lower())
            elif functionName == 'casefold': text = text.replace(match, key.casefold())
            elif functionName == 'swapcase': text = text.replace(match, key.swapcase())
            elif functionName == 'time': text = text.replace(match, strftime("%H:%M:%S", localtime()))
            elif functionName == 'date': text = text.replace(match, strftime("%d/%m/%Y", localtime()))
            elif functionName == 'dateTime': text = text.replace(match, strftime("%d/%m/%Y,%H:%M:%S", localtime()))
            elif functionName in str(self.__functions):
                for func in self.__functions:
                    
                    if regex.search(r'(?<!\S){}(?!\S)'.format(functionName), str(func)) != None:

                        if group['key'] != None:

                            listParametre: list = self.__typing(group['key'])

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
        parse all the `{{#var1 == var2: value1 || value2 }}` in the text give in

        return -> str
        '''

        if not self.hasCondition(text)[0]: return text

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
                if listTyping[0] == listTyping[1]:
                    text = text.replace(match, resultValue1)
                else:
                    text = text.replace(match, resultValue2)
            elif compSymbol == "!=":
                if listTyping[0] != listTyping[1]:
                    text = text.replace(match, resultValue1)
                else:
                    text = text.replace(match, resultValue2)
            else:
                value = self.__convertAnyToFloat(listTyping[0], listTyping[1])
                if compSymbol == "<=":
                    if value[0] <= value[1]:
                        text = text.replace(match, resultValue1)
                    else:
                        text = text.replace(match, resultValue2)
                elif compSymbol == ">=":
                    if value[0] >= value[1]:
                        text = text.replace(match, resultValue1)
                    else:
                        text = text.replace(match, resultValue2)
                elif compSymbol == "<":
                    if value[0] < value[1]:
                        text = text.replace(match, resultValue1)
                    else:
                        text = text.replace(match, resultValue2)
                elif compSymbol == ">":
                    if value[0] > value[1]:
                        text = text.replace(match, resultValue1)
                    else:
                        text = text.replace(match, resultValue2)
                else:
                    sys.exit('The ' + compSymbol + ' is not a valid comparator')
        
        return text

    def hasVariable(self, text: str) -> Tuple[bool, list]:
        '''
        Detects if there is the presence of `{{$variable}}`

        bool : `true` or `false`
        list : `[match1, match2, ...]`

        return -> Tuple[bool, list]
        '''

        find: list = regex.findall(self.__regVariable, text)
        return self.__presence(find)

    def hasFunction(self, text: str) -> Tuple[bool, list]:
        '''
        Detects if there is the presence of `{{@function param1 param2}}` or `{{@function}}`

        return -> Tuple[bool, list]
        '''

        find: list = regex.findall(self.__regFunction, text)
        return self.__presence(find)

    def hasCondition(self, text: str) -> Tuple[bool, list]:
        '''
        Detects if there is the presence of `{{#condition var}} value1 {{else}} value2 {{condition#}}`

        return -> Tuple[bool, list]
        '''

        find: list = regex.findall(self.__regCondition, text)
        return self.__presence(find)

