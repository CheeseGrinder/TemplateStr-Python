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
    __regFunctionParam: Pattern = regex.compile(r'\"(?P<str_double>[^\"]+)\"|\'(?P<str_single>[^\']+)\'|`(?P<str_back>[^`]+)`|<b:(?P<bool>True|False)>|<i:(?P<int>[0-9_.]+)>|(?P<variable>[^<>\" ]+)')
    __regCondition: Pattern = regex.compile(r'(?P<match>{{#(?P<keyStart>[^{#}]+) (?P<variable>[^{}]+)}} (?P<resultValue1>[^{}]+) {{else}} (?P<resultValue2>[^{}]+) {{(?P<keyEnd>[^{}]+)#}})')

    def __init__(self, functionList: list = [], variableDict: dict = {}):
        '''
        `functionList: list` is a list of custom functions that can be used when you call a function with: `{{@myCustomFunction}}`

        `variableDict: dict` is a dictionary of the values you want to use when you call: `{{$myVar}}`
        '''

        self.__functions = functionList
        self.__variables = variableDict

        # VariableExemple : {{$var1}}
        # VariableExemple : {{@var1}} {{@var1 arg1 arg2}}
        # VariableExemple : {{#succes var1}} oui {{else}} non {{succes#}}

    def __presence(self, list: list) -> Tuple[bool, list]:
        presences: list = []
        if list != []:
            for value in list:
                presences.append(value[0])
            
            return [True, presences]
        else:
            return [False, None]

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

            text = text.replace(match, self.__variables[key])

        return text

    def parseFunction(self, text: str) -> str:
        '''
        parse all the `{{@function param1 param2}}` or `{{@function}}` in the text give in

        param type:

            keyVariable : is the key of the value in the dictionary pass to the constructor (return the value)
            <b:True>     : bool  (return True)
            <i:123>      : int   (return 123)
            <i:123.4>    : float (return 123.4)
            "text"      : str   (return text)

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
                            listParametre: list = []

                            for m2 in self.__regFunctionParam.finditer(group['key']):
                                groupParam: dict = m2.groupdict()

                                if groupParam['str_double'] != None:
                                    listParametre.append(groupParam['str_double'])
                                elif groupParam['str_single'] != None:
                                    listParametre.append(groupParam['str_single'])
                                elif groupParam['str_back'] != None:
                                    listParametre.append(groupParam['str_back'])
                                elif groupParam['bool'] != None:
                                    typeBool: bool = bool(strtobool(groupParam['bool']))
                                    listParametre.append(typeBool)
                                elif groupParam['int'] != None:
                                    if '.' in groupParam['int']:
                                        number: float = float(groupParam['int'])
                                    else:
                                        number: int = int(groupParam['int'])
                                    listParametre.append(number)
                                elif groupParam['variable'] != None:
                                    listParametre.append(self.__variables[groupParam['variable']])

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
        parse all the `{{#condition var}} value1 {{else}} value2 {{condition#}}` in the text give in

        return -> str
        '''

        if not self.hasCondition(text)[0]: return text

        # parse Condition
        for m in self.__regCondition.finditer(text):
            group: dict = m.groupdict()

            match: str = group['match']
            variable: str = group['variable']
            keyStart: str = group['keyStart']
            keyEnd: str = group['keyEnd']

            if keyStart == keyEnd:
                if keyStart == str(self.__variables[variable]):
                    text = text.replace(match, group['resultValue1'])
                else:
                    text = text.replace(match, group['resultValue2'])
            else:
                sys.exit('The start key is different from the end key ({{#startKey}} ... {{endKey#}}) : ' + keyStart + ' != ' + keyEnd)
        
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





