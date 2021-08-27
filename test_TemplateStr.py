import unittest
from tempStr import TemplateStr
from time import strftime, localtime

print("\n-------------------------------- Test --------------------------------\n")

varDict: dict = {
    "name": "Jame",
    "age": 32, 
    "bool": True, 
    "lower": "azerty", 
    "upper": "AZERTY", 
    "swap": "AzErTy",
    "cfold": "grüßen",
    "Build": "Succes",
    "dict": {"value": "dict in dict"},
    "dictMaster": {"dict1": {"value": "dict in dict in dict"}},
}

def test() -> str:
    return "Test1"

def testType(list:list) -> str:

    result = "ok"
    
    if type(list[0]) != str: result = "type list[0] != str"
    if type(list[1]) != str: result = "type list[1] != str"
    if type(list[2]) != str: result = "type list[2] != str"
    if type(list[3]) != bool: result = "type list[3] != bool"
    if type(list[4]) != int: result = "type list[4] != int"
    if type(list[5]) != float: result = "type list[5] != float"
    if type(list[6]) != str: result = "type list[6] != str"

    return result

funcs: list = [testType, test]

class TestParseMethode(unittest.TestCase):

    def testAll(self):

        text_1: list = ["Hello my name is {{@uppercase name}}, I am {{$age}} years old. my Dict: {{$dict.value}}. my keyboard: {{#lower == 'azerty': azerty || qwerty}}, {{?cfold; grüßen=yes, grüssen=no, default=anyway}}",
             "Hello my name is JAME, I am 32 years old. my Dict: dict in dict. my keyboard: azerty, yes"]

        parser = TemplateStr(funcs, varDict)

        self.assertEqual(parser.parse(text_1[0]), text_1[1], "text_1")

    def testVariable(self):

        text_1: list = ["var bool = {{$bool}} and name = {{$name}}", "var bool = True and name = Jame"]
        text_2: list = ["{{$dict.value}}", "dict in dict"]
        text_3: list = ["{{$dictMaster.dict1.value}}", "dict in dict in dict"]
        text_4: list = ["{{$word}}", "None"]
        text_5: list = ["{{$dict.dict1.value}}", "None"]

        parser = TemplateStr(variableDict=varDict)

        self.assertEqual(parser.parseVariable(text_1[0]), text_1[1], "text_1")
        self.assertEqual(parser.parseVariable(text_2[0]), text_2[1], "text_2")
        self.assertEqual(parser.parseVariable(text_3[0]), text_3[1], "text_3")
        self.assertEqual(parser.parseVariable(text_4[0]), text_4[1], "text_4")
        self.assertEqual(parser.parseVariable(text_5[0]), text_5[1], "text_5")
    
    def testFunction(self):

        uppercase: list = ["{{@uppercase lower}}", "AZERTY"]
        uppercase2: list = ["{{@uppercase dict.value}}", "DICT IN DICT"]
        uppercaseFirst: list = ["{{@uppercaseFirst lower}}", "Azerty"]
        lowercase: list = ["{{@lowercase upper}}", "azerty"]
        casefold: list = ["{{@casefold cfold}}", "grüssen"]
        swapcase: list = ["{{@swapcase swap}}", "aZeRtY"]
        time: str = "{{@time}}"
        date: str = "{{@date}}"
        dateTime: str = "{{@dateTime}}"

        parser = TemplateStr(variableDict=varDict)

        self.assertEqual(parser.parseFunction(uppercase[0]), uppercase[1], "uppercase")
        self.assertEqual(parser.parseFunction(uppercase2[0]), uppercase2[1], "uppercase2")
        self.assertEqual(parser.parseFunction(uppercaseFirst[0]), uppercaseFirst[1], "uppercaseFirst")
        self.assertEqual(parser.parseFunction(lowercase[0]), lowercase[1], "lowercase")
        self.assertEqual(parser.parseFunction(casefold[0]), casefold[1], "casefold")
        self.assertEqual(parser.parseFunction(swapcase[0]), swapcase[1], "swapcase")
        self.assertEqual(parser.parseFunction(time), strftime("%H:%M:%S", localtime()), "time")
        self.assertEqual(parser.parseFunction(date), strftime("%d/%m/%Y", localtime()), "date")
        self.assertEqual(parser.parseFunction(dateTime), strftime("%d/%m/%Y,%H:%M:%S", localtime()), "dateTime")

    def testCustomFunction(self):
        
        text_1: list = ["{{@test}}", "Test1"]
        testType: list = ["{{@testType \"text\" 'text' `text` <b:True> <n:123> <n:123.4> age}}", "ok"]

        parser = TemplateStr(funcs, varDict)

        self.assertEqual(parser.parseFunction(text_1[0]), text_1[1], "text_1")
        self.assertEqual(parser.parseFunction(testType[0]), testType[1], "testType")

    def testConditionEqual(self):

        str_Equal_Str: list = ["{{#'text' == 'text': yes || no}}", "yes"]
        str_Equal2_Str: list = ["{{#'text' == 'texte': yes || no}}", "no"]
        int_Equal_Str: list = ["{{#<n:4> == 'text': yes || no}}", "no"]
        float_Equal_Str: list = ["{{#<n:4.5> == 'text': yes || no}}", "no"]
        bool_Equal_Str: list = ["{{#<b:True> == 'text': yes || no}}", "no"]
        var_Equal_Str: list = ["{{#age == 'text': yes || no}}", "no"]

        parser = TemplateStr(variableDict=varDict)

        self.assertEqual(parser.parseCondition(str_Equal_Str[0]), str_Equal_Str[1], "str_Equal_Str")
        self.assertEqual(parser.parseCondition(str_Equal2_Str[0]), str_Equal2_Str[1], "str_Equal2_Str")
        self.assertEqual(parser.parseCondition(int_Equal_Str[0]), int_Equal_Str[1], "int_Equal_Str")
        self.assertEqual(parser.parseCondition(float_Equal_Str[0]), float_Equal_Str[1], "float_Equal_Str")
        self.assertEqual(parser.parseCondition(bool_Equal_Str[0]), bool_Equal_Str[1], "bool_Equal_Str")
        self.assertEqual(parser.parseCondition(var_Equal_Str[0]), var_Equal_Str[1], "var_Equal_Str")

    def testConditionNoTEqual(self):

        str_NoT_Equal_Str: list = ["{{#'text' != 'text': yes || no}}", "no"]
        str_NoT_Equal2_Str: list = ["{{#'text' != 'texte': yes || no}}", "yes"]
        int_NoT_Equal_Str: list = ["{{#<n:4> != 'text': yes || no}}", "yes"]
        float_NoT_Equal_Str: list = ["{{#<n:4.5> != 'text': yes || no}}", "yes"]
        bool_NoT_Equal_Str: list = ["{{#<b:True> != 'text': yes || no}}", "yes"]
        var_NoT_Equal_Str: list = ["{{#age != 'text': yes || no}}", "yes"]

        parser = TemplateStr(variableDict=varDict)

        self.assertEqual(parser.parseCondition(str_NoT_Equal_Str[0]), str_NoT_Equal_Str[1], "str_NoT_Equal_Str")
        self.assertEqual(parser.parseCondition(str_NoT_Equal2_Str[0]), str_NoT_Equal2_Str[1], "str_NoT_Equal2_Str")
        self.assertEqual(parser.parseCondition(int_NoT_Equal_Str[0]), int_NoT_Equal_Str[1], "int_NoT_Equal_Str")
        self.assertEqual(parser.parseCondition(float_NoT_Equal_Str[0]), float_NoT_Equal_Str[1], "float_NoT_Equal_Str")
        self.assertEqual(parser.parseCondition(bool_NoT_Equal_Str[0]), bool_NoT_Equal_Str[1], "bool_NoT_Equal_Str")
        self.assertEqual(parser.parseCondition(var_NoT_Equal_Str[0]), var_NoT_Equal_Str[1], "var_NoT_Equal_Str")

    def testConditionSuperiorEqual(self):

        parser = TemplateStr(variableDict=varDict)

        # String
        str_Superior_Equal_Str: list = ["{{#'text' >= 'text': yes || no}}", "yes"]
        str_Superior_Equal_2_Str: list = ["{{#'text' >= 'texte': yes || no}}", "no"]
        str_Superior_Equal_Int: list = ["{{#'text' >= <n:4>: yes || no}}", "yes"]
        str_Superior_Equal_2_Int: list = ["{{#'text' >= <n:123>: yes || no}}", "no"]
        str_Superior_Equal_Float: list = ["{{#'text' >= <n:4.5>: yes || no}}", "no"]
        str_Superior_Equal_2_Float: list = ["{{#'text' >= <n:3.5>: yes || no}}", "yes"]
        str_Superior_Equal_Bool: list = ["{{#'text' >= <b:True>: yes || no}}", "yes"]
        str_Superior_Equal_2_Bool: list = ["{{#'text' >= <b:False>: yes || no}}", "yes"]

        self.assertEqual(parser.parseCondition(str_Superior_Equal_Str[0]), str_Superior_Equal_Str[1], "str_Superior_Equal_Str")
        self.assertEqual(parser.parseCondition(str_Superior_Equal_2_Str[0]), str_Superior_Equal_2_Str[1], "str_Superior_Equal_2_Str")
        self.assertEqual(parser.parseCondition(str_Superior_Equal_Int[0]), str_Superior_Equal_Int[1], "str_Superior_Equal_Int")
        self.assertEqual(parser.parseCondition(str_Superior_Equal_2_Int[0]), str_Superior_Equal_2_Int[1], "str_Superior_Equal_2_Int")
        self.assertEqual(parser.parseCondition(str_Superior_Equal_Float[0]), str_Superior_Equal_Float[1], "str_Superior_Equal_Float")
        self.assertEqual(parser.parseCondition(str_Superior_Equal_2_Float[0]), str_Superior_Equal_2_Float[1], "str_Superior_Equal_2_Float")
        self.assertEqual(parser.parseCondition(str_Superior_Equal_Bool[0]), str_Superior_Equal_Bool[1], "str_Superior_Equal_Bool")
        self.assertEqual(parser.parseCondition(str_Superior_Equal_2_Bool[0]), str_Superior_Equal_2_Bool[1], "str_Superior_Equal_2_Bool")

        # Int
        int_Superior_Equal_Str: list = ["{{#<n:4> >= 'text': yes || no}}", "yes"]
        int_Superior_Equal_2_Str: list = ["{{#<n:4> >= 'texte': yes || no}}", "no"]
        int_Superior_Equal_Int: list = ["{{#<n:4> >= <n:4>: yes || no}}", "yes"]
        int_Superior_Equal_2_Int: list = ["{{#<n:4> >= <n:5>: yes || no}}", "no"]
        int_Superior_Equal_Float: list = ["{{#<n:4> >= <n:3.5>: yes || no}}", "yes"]
        int_Superior_Equal_2_Float: list = ["{{#<n:4> >= <n:4.5>: yes || no}}", "no"]
        int_Superior_Equal_Bool: list = ["{{#<n:4> >= <b:True>: yes || no}}", "yes"]
        int_Superior_Equal_2_Bool: list = ["{{#<n:4> >= <b:False>: yes || no}}", "yes"]

        self.assertEqual(parser.parseCondition(int_Superior_Equal_Str[0]), int_Superior_Equal_Str[1], "int_Superior_Equal_Str")
        self.assertEqual(parser.parseCondition(int_Superior_Equal_2_Str[0]), int_Superior_Equal_2_Str[1], "int_Superior_Equal_2_Str")
        self.assertEqual(parser.parseCondition(int_Superior_Equal_Int[0]), int_Superior_Equal_Int[1], "int_Superior_Equal_Int")
        self.assertEqual(parser.parseCondition(int_Superior_Equal_2_Int[0]), int_Superior_Equal_2_Int[1], "int_Superior_Equal_2_Int")
        self.assertEqual(parser.parseCondition(int_Superior_Equal_Float[0]), int_Superior_Equal_Float[1], "int_Superior_Equal_Float")
        self.assertEqual(parser.parseCondition(int_Superior_Equal_2_Float[0]), int_Superior_Equal_2_Float[1], "int_Superior_Equal_2_Float")
        self.assertEqual(parser.parseCondition(int_Superior_Equal_Bool[0]), int_Superior_Equal_Bool[1], "int_Superior_Equal_Bool")
        self.assertEqual(parser.parseCondition(int_Superior_Equal_2_Bool[0]), int_Superior_Equal_2_Bool[1], "int_Superior_Equal_2_Bool")

        # Float
        float_Superior_Equal_Str: list = ["{{#<n:4.5> >= 'text': yes || no}}", "yes"]
        float_Superior_Equal_2_Str: list = ["{{#<n:4.5> >= 'texte': yes || no}}", "no"]
        float_Superior_Equal_Int: list = ["{{#<n:4.5> >= <n:4>: yes || no}}", "yes"]
        float_Superior_Equal_2_Int: list = ["{{#<n:4.5> >= <n:5>: yes || no}}", "no"]
        float_Superior_Equal_Float: list = ["{{#<n:4.5> >= <n:4.4>: yes || no}}", "yes"]
        float_Superior_Equal_2_Float: list = ["{{#<n:4.5> >= <n:4.6>: yes || no}}", "no"]
        float_Superior_Equal_Bool: list = ["{{#<n:4.5> >= <b:True>: yes || no}}", "yes"]
        float_Superior_Equal_2_Bool: list = ["{{#<n:4.5> >= <b:False>: yes || no}}", "yes"]

        self.assertEqual(parser.parseCondition(float_Superior_Equal_Str[0]), float_Superior_Equal_Str[1], "float_Superior_Equal_Str")
        self.assertEqual(parser.parseCondition(float_Superior_Equal_2_Str[0]), float_Superior_Equal_2_Str[1], "float_Superior_Equal_2_Str")
        self.assertEqual(parser.parseCondition(float_Superior_Equal_Int[0]), float_Superior_Equal_Int[1], "float_Superior_Equal_Int")
        self.assertEqual(parser.parseCondition(float_Superior_Equal_2_Int[0]), float_Superior_Equal_2_Int[1], "float_Superior_Equal_2_Int")
        self.assertEqual(parser.parseCondition(float_Superior_Equal_Float[0]), float_Superior_Equal_Float[1], "float_Superior_Equal_Float")
        self.assertEqual(parser.parseCondition(float_Superior_Equal_2_Float[0]), float_Superior_Equal_2_Float[1], "float_Superior_Equal_2_Float")
        self.assertEqual(parser.parseCondition(float_Superior_Equal_Bool[0]), float_Superior_Equal_Bool[1], "float_Superior_Equal_Bool")
        self.assertEqual(parser.parseCondition(float_Superior_Equal_2_Bool[0]), float_Superior_Equal_2_Bool[1], "float_Superior_Equal_2_Bool")

        # Bool
        bool_Superior_Equal_Str: list = ["{{#<b:True> >= 'text': yes || no}}", "no"]
        bool_Superior_Equal_2_Str: list = ["{{#<b:False> >= 'texte': yes || no}}", "no"]
        bool_Superior_Equal_Int: list = ["{{#<b:True> >= <n:4>: yes || no}}", "no"]
        bool_Superior_Equal_2_Int: list = ["{{#<b:False> >= <n:5>: yes || no}}", "no"]
        bool_Superior_Equal_Float: list = ["{{#<b:True> >= <n:4.4>: yes || no}}", "no"]
        bool_Superior_Equal_2_Float: list = ["{{#<b:False> >= <n:4.6>: yes || no}}", "no"]
        bool_Superior_Equal_Bool: list = ["{{#<b:True> >= <b:True>: yes || no}}", "yes"]
        bool_Superior_Equal_2_Bool: list = ["{{#<b:False> >= <b:False>: yes || no}}", "yes"]

        self.assertEqual(parser.parseCondition(bool_Superior_Equal_Str[0]), bool_Superior_Equal_Str[1], "bool_Superior_Equal_Str")
        self.assertEqual(parser.parseCondition(bool_Superior_Equal_2_Str[0]), bool_Superior_Equal_2_Str[1], "bool_Superior_Equal_2_Str")
        self.assertEqual(parser.parseCondition(bool_Superior_Equal_Int[0]), bool_Superior_Equal_Int[1], "bool_Superior_Equal_Int")
        self.assertEqual(parser.parseCondition(bool_Superior_Equal_2_Int[0]), bool_Superior_Equal_2_Int[1], "bool_Superior_Equal_2_Int")
        self.assertEqual(parser.parseCondition(bool_Superior_Equal_Float[0]), bool_Superior_Equal_Float[1], "bool_Superior_Equal_Float")
        self.assertEqual(parser.parseCondition(bool_Superior_Equal_2_Float[0]), bool_Superior_Equal_2_Float[1], "bool_Superior_Equal_2_Float")
        self.assertEqual(parser.parseCondition(bool_Superior_Equal_Bool[0]), bool_Superior_Equal_Bool[1], "bool_Superior_Equal_Bool")
        self.assertEqual(parser.parseCondition(bool_Superior_Equal_2_Bool[0]), bool_Superior_Equal_2_Bool[1], "bool_Superior_Equal_2_Bool")

    def testConditionSuperior(self):

        parser = TemplateStr(variableDict=varDict)

        # String
        str_Superior_Str: list = ["{{#'text' > 'text': yes || no}}", "no"]
        str_Superior_2_Str: list = ["{{#'text' > 'texte': yes || no}}", "no"]
        str_Superior_Int: list = ["{{#'text' > <n:4>: yes || no}}", "no"]
        str_Superior_2_Int: list = ["{{#'text' > <n:123>: yes || no}}", "no"]
        str_Superior_Float: list = ["{{#'text' > <n:4.5>: yes || no}}", "no"]
        str_Superior_2_Float: list = ["{{#'text' > <n:3.5>: yes || no}}", "yes"]
        str_Superior_Bool: list = ["{{#'text' > <b:True>: yes || no}}", "yes"]
        str_Superior_2_Bool: list = ["{{#'text' > <b:False>: yes || no}}", "yes"]

        self.assertEqual(parser.parseCondition(str_Superior_Str[0]), str_Superior_Str[1], "str_Superior_Str")
        self.assertEqual(parser.parseCondition(str_Superior_2_Str[0]), str_Superior_2_Str[1], "str_Superior_2_Str")
        self.assertEqual(parser.parseCondition(str_Superior_Int[0]), str_Superior_Int[1], "str_Superior_Int")
        self.assertEqual(parser.parseCondition(str_Superior_2_Int[0]), str_Superior_2_Int[1], "str_Superior_2_Int")
        self.assertEqual(parser.parseCondition(str_Superior_Float[0]), str_Superior_Float[1], "str_Superior_Float")
        self.assertEqual(parser.parseCondition(str_Superior_2_Float[0]), str_Superior_2_Float[1], "str_Superior_2_Float")
        self.assertEqual(parser.parseCondition(str_Superior_Bool[0]), str_Superior_Bool[1], "str_Superior_Bool")
        self.assertEqual(parser.parseCondition(str_Superior_2_Bool[0]), str_Superior_2_Bool[1], "str_Superior_2_Bool")

        # Int
        int_Superior_Str: list = ["{{#<n:4> > 'text': yes || no}}", "no"]
        int_Superior_2_Str: list = ["{{#<n:4> > 'texte': yes || no}}", "no"]
        int_Superior_Int: list = ["{{#<n:4> > <n:4>: yes || no}}", "no"]
        int_Superior_2_Int: list = ["{{#<n:4> > <n:5>: yes || no}}", "no"]
        int_Superior_Float: list = ["{{#<n:4> > <n:3.5>: yes || no}}", "yes"]
        int_Superior_2_Float: list = ["{{#<n:4> > <n:4.5>: yes || no}}", "no"]
        int_Superior_Bool: list = ["{{#<n:4> > <b:True>: yes || no}}", "yes"]
        int_Superior_2_Bool: list = ["{{#<n:4> > <b:False>: yes || no}}", "yes"]

        self.assertEqual(parser.parseCondition(int_Superior_Str[0]), int_Superior_Str[1], "int_Superior_Str")
        self.assertEqual(parser.parseCondition(int_Superior_2_Str[0]), int_Superior_2_Str[1], "int_Superior_2_Str")
        self.assertEqual(parser.parseCondition(int_Superior_Int[0]), int_Superior_Int[1], "int_Superior_Int")
        self.assertEqual(parser.parseCondition(int_Superior_2_Int[0]), int_Superior_2_Int[1], "int_Superior_2_Int")
        self.assertEqual(parser.parseCondition(int_Superior_Float[0]), int_Superior_Float[1], "int_Superior_Float")
        self.assertEqual(parser.parseCondition(int_Superior_2_Float[0]), int_Superior_2_Float[1], "int_Superior_2_Float")
        self.assertEqual(parser.parseCondition(int_Superior_Bool[0]), int_Superior_Bool[1], "int_Superior_Bool")
        self.assertEqual(parser.parseCondition(int_Superior_2_Bool[0]), int_Superior_2_Bool[1], "int_Superior_2_Bool")

        # Float
        float_Superior_Str: list = ["{{#<n:4.5> > 'text': yes || no}}", "yes"]
        float_Superior_2_Str: list = ["{{#<n:4.5> > 'texte': yes || no}}", "no"]
        float_Superior_Int: list = ["{{#<n:4.5> > <n:4>: yes || no}}", "yes"]
        float_Superior_2_Int: list = ["{{#<n:4.5> > <n:5>: yes || no}}", "no"]
        float_Superior_Float: list = ["{{#<n:4.5> > <n:4.4>: yes || no}}", "yes"]
        float_Superior_2_Float: list = ["{{#<n:4.5> > <n:4.6>: yes || no}}", "no"]
        float_Superior_Bool: list = ["{{#<n:4.5> > <b:True>: yes || no}}", "yes"]
        float_Superior_2_Bool: list = ["{{#<n:4.5> > <b:False>: yes || no}}", "yes"]

        self.assertEqual(parser.parseCondition(float_Superior_Str[0]), float_Superior_Str[1], "float_Superior_Str")
        self.assertEqual(parser.parseCondition(float_Superior_2_Str[0]), float_Superior_2_Str[1], "float_Superior_2_Str")
        self.assertEqual(parser.parseCondition(float_Superior_Int[0]), float_Superior_Int[1], "float_Superior_Int")
        self.assertEqual(parser.parseCondition(float_Superior_2_Int[0]), float_Superior_2_Int[1], "float_Superior_2_Int")
        self.assertEqual(parser.parseCondition(float_Superior_Float[0]), float_Superior_Float[1], "float_Superior_Float")
        self.assertEqual(parser.parseCondition(float_Superior_2_Float[0]), float_Superior_2_Float[1], "float_Superior_2_Float")
        self.assertEqual(parser.parseCondition(float_Superior_Bool[0]), float_Superior_Bool[1], "float_Superior_Bool")
        self.assertEqual(parser.parseCondition(float_Superior_2_Bool[0]), float_Superior_2_Bool[1], "float_Superior_2_Bool")

        # Bool
        bool_Superior_Str: list = ["{{#<b:True> > 'text': yes || no}}", "no"]
        bool_Superior_2_Str: list = ["{{#<b:False> > 'texte': yes || no}}", "no"]
        bool_Superior_Int: list = ["{{#<b:True> > <n:4>: yes || no}}", "no"]
        bool_Superior_2_Int: list = ["{{#<b:False> > <n:5>: yes || no}}", "no"]
        bool_Superior_Float: list = ["{{#<b:True> > <n:4.4>: yes || no}}", "no"]
        bool_Superior_2_Float: list = ["{{#<b:False> > <n:4.6>: yes || no}}", "no"]
        bool_Superior_Bool: list = ["{{#<b:True> > <b:True>: yes || no}}", "no"]
        bool_Superior_2_Bool: list = ["{{#<b:False> > <b:False>: yes || no}}", "no"]

        self.assertEqual(parser.parseCondition(bool_Superior_Str[0]), bool_Superior_Str[1], "bool_Superior_Str")
        self.assertEqual(parser.parseCondition(bool_Superior_2_Str[0]), bool_Superior_2_Str[1], "bool_Superior_2_Str")
        self.assertEqual(parser.parseCondition(bool_Superior_Int[0]), bool_Superior_Int[1], "bool_Superior_Int")
        self.assertEqual(parser.parseCondition(bool_Superior_2_Int[0]), bool_Superior_2_Int[1], "bool_Superior_2_Int")
        self.assertEqual(parser.parseCondition(bool_Superior_Float[0]), bool_Superior_Float[1], "bool_Superior_Float")
        self.assertEqual(parser.parseCondition(bool_Superior_2_Float[0]), bool_Superior_2_Float[1], "bool_Superior_2_Float")
        self.assertEqual(parser.parseCondition(bool_Superior_Bool[0]), bool_Superior_Bool[1], "bool_Superior_Bool")
        self.assertEqual(parser.parseCondition(bool_Superior_2_Bool[0]), bool_Superior_2_Bool[1], "bool_Superior_2_Bool")

    def testConditionInferiorEqual(self):

        parser = TemplateStr(variableDict=varDict)

        # String
        str_Inferior_Equal_Str: list = ["{{#'text' <= 'text': yes || no}}", "yes"]
        str_Inferior_Equal_2_Str: list = ["{{#'text' <= 'texte': yes || no}}", "yes"]
        str_Inferior_Equal_Int: list = ["{{#'text' <= <n:4>: yes || no}}", "yes"]
        str_Inferior_Equal_2_Int: list = ["{{#'text' <= <n:123>: yes || no}}", "yes"]
        str_Inferior_Equal_Float: list = ["{{#'text' <= <n:4.5>: yes || no}}", "yes"]
        str_Inferior_Equal_2_Float: list = ["{{#'text' <= <n:3.5>: yes || no}}", "no"]
        str_Inferior_Equal_Bool: list = ["{{#'text' <= <b:True>: yes || no}}", "no"]
        str_Inferior_Equal_2_Bool: list = ["{{#'text' <= <b:False>: yes || no}}", "no"]

        self.assertEqual(parser.parseCondition(str_Inferior_Equal_Str[0]), str_Inferior_Equal_Str[1], "str_Inferior_Equal_Str")
        self.assertEqual(parser.parseCondition(str_Inferior_Equal_2_Str[0]), str_Inferior_Equal_2_Str[1], "str_Inferior_Equal_2_Str")
        self.assertEqual(parser.parseCondition(str_Inferior_Equal_Int[0]), str_Inferior_Equal_Int[1], "str_Inferior_Equal_Int")
        self.assertEqual(parser.parseCondition(str_Inferior_Equal_2_Int[0]), str_Inferior_Equal_2_Int[1], "str_Inferior_Equal_2_Int")
        self.assertEqual(parser.parseCondition(str_Inferior_Equal_Float[0]), str_Inferior_Equal_Float[1], "str_Inferior_Equal_Float")
        self.assertEqual(parser.parseCondition(str_Inferior_Equal_2_Float[0]), str_Inferior_Equal_2_Float[1], "str_Inferior_Equal_2_Float")
        self.assertEqual(parser.parseCondition(str_Inferior_Equal_Bool[0]), str_Inferior_Equal_Bool[1], "str_Inferior_Equal_Bool")
        self.assertEqual(parser.parseCondition(str_Inferior_Equal_2_Bool[0]), str_Inferior_Equal_2_Bool[1], "str_Inferior_Equal_2_Bool")

        # Int
        int_Inferior_Equal_Str: list = ["{{#<n:4> <= 'text': yes || no}}", "yes"]
        int_Inferior_Equal_2_Str: list = ["{{#<n:4> <= 'texte': yes || no}}", "yes"]
        int_Inferior_Equal_Int: list = ["{{#<n:4> <= <n:4>: yes || no}}", "yes"]
        int_Inferior_Equal_2_Int: list = ["{{#<n:4> <= <n:5>: yes || no}}", "yes"]
        int_Inferior_Equal_Float: list = ["{{#<n:4> <= <n:3.5>: yes || no}}", "no"]
        int_Inferior_Equal_2_Float: list = ["{{#<n:4> <= <n:4.5>: yes || no}}", "yes"]
        int_Inferior_Equal_Bool: list = ["{{#<n:4> <= <b:True>: yes || no}}", "no"]
        int_Inferior_Equal_2_Bool: list = ["{{#<n:4> <= <b:False>: yes || no}}", "no"]

        self.assertEqual(parser.parseCondition(int_Inferior_Equal_Str[0]), int_Inferior_Equal_Str[1], "int_Inferior_Equal_Str")
        self.assertEqual(parser.parseCondition(int_Inferior_Equal_2_Str[0]), int_Inferior_Equal_2_Str[1], "int_Inferior_Equal_2_Str")
        self.assertEqual(parser.parseCondition(int_Inferior_Equal_Int[0]), int_Inferior_Equal_Int[1], "int_Inferior_Equal_Int")
        self.assertEqual(parser.parseCondition(int_Inferior_Equal_2_Int[0]), int_Inferior_Equal_2_Int[1], "int_Inferior_Equal_2_Int")
        self.assertEqual(parser.parseCondition(int_Inferior_Equal_Float[0]), int_Inferior_Equal_Float[1], "int_Inferior_Equal_Float")
        self.assertEqual(parser.parseCondition(int_Inferior_Equal_2_Float[0]), int_Inferior_Equal_2_Float[1], "int_Inferior_Equal_2_Float")
        self.assertEqual(parser.parseCondition(int_Inferior_Equal_Bool[0]), int_Inferior_Equal_Bool[1], "int_Inferior_Equal_Bool")
        self.assertEqual(parser.parseCondition(int_Inferior_Equal_2_Bool[0]), int_Inferior_Equal_2_Bool[1], "int_Inferior_Equal_2_Bool")

        # Float
        float_Inferior_Equal_Str: list = ["{{#<n:4.5> <= 'text': yes || no}}", "no"]
        float_Inferior_Equal_2_Str: list = ["{{#<n:4.5> <= 'texte': yes || no}}", "yes"]
        float_Inferior_Equal_Int: list = ["{{#<n:4.5> <= <n:4>: yes || no}}", "no"]
        float_Inferior_Equal_2_Int: list = ["{{#<n:4.5> <= <n:5>: yes || no}}", "yes"]
        float_Inferior_Equal_Float: list = ["{{#<n:4.5> <= <n:4.4>: yes || no}}", "no"]
        float_Inferior_Equal_2_Float: list = ["{{#<n:4.5> <= <n:4.6>: yes || no}}", "yes"]
        float_Inferior_Equal_Bool: list = ["{{#<n:4.5> <= <b:True>: yes || no}}", "no"]
        float_Inferior_Equal_2_Bool: list = ["{{#<n:4.5> <= <b:False>: yes || no}}", "no"]

        self.assertEqual(parser.parseCondition(float_Inferior_Equal_Str[0]), float_Inferior_Equal_Str[1], "float_Inferior_Equal_Str")
        self.assertEqual(parser.parseCondition(float_Inferior_Equal_2_Str[0]), float_Inferior_Equal_2_Str[1], "float_Inferior_Equal_2_Str")
        self.assertEqual(parser.parseCondition(float_Inferior_Equal_Int[0]), float_Inferior_Equal_Int[1], "float_Inferior_Equal_Int")
        self.assertEqual(parser.parseCondition(float_Inferior_Equal_2_Int[0]), float_Inferior_Equal_2_Int[1], "float_Inferior_Equal_2_Int")
        self.assertEqual(parser.parseCondition(float_Inferior_Equal_Float[0]), float_Inferior_Equal_Float[1], "float_Inferior_Equal_Float")
        self.assertEqual(parser.parseCondition(float_Inferior_Equal_2_Float[0]), float_Inferior_Equal_2_Float[1], "float_Inferior_Equal_2_Float")
        self.assertEqual(parser.parseCondition(float_Inferior_Equal_Bool[0]), float_Inferior_Equal_Bool[1], "float_Inferior_Equal_Bool")
        self.assertEqual(parser.parseCondition(float_Inferior_Equal_2_Bool[0]), float_Inferior_Equal_2_Bool[1], "float_Inferior_Equal_2_Bool")

        # Bool
        bool_Inferior_Equal_Str: list = ["{{#<b:True> <= 'text': yes || no}}", "yes"]
        bool_Inferior_Equal_2_Str: list = ["{{#<b:False> <= 'texte': yes || no}}", "yes"]
        bool_Inferior_Equal_Int: list = ["{{#<b:True> <= <n:4>: yes || no}}", "yes"]
        bool_Inferior_Equal_2_Int: list = ["{{#<b:False> <= <n:5>: yes || no}}", "yes"]
        bool_Inferior_Equal_Float: list = ["{{#<b:True> <= <n:4.4>: yes || no}}", "yes"]
        bool_Inferior_Equal_2_Float: list = ["{{#<b:False> <= <n:4.6>: yes || no}}", "yes"]
        bool_Inferior_Equal_Bool: list = ["{{#<b:True> <= <b:True>: yes || no}}", "yes"]
        bool_Inferior_Equal_2_Bool: list = ["{{#<b:False> <= <b:False>: yes || no}}", "yes"]

        self.assertEqual(parser.parseCondition(bool_Inferior_Equal_Str[0]), bool_Inferior_Equal_Str[1], "bool_Inferior_Equal_Str")
        self.assertEqual(parser.parseCondition(bool_Inferior_Equal_2_Str[0]), bool_Inferior_Equal_2_Str[1], "bool_Inferior_Equal_2_Str")
        self.assertEqual(parser.parseCondition(bool_Inferior_Equal_Int[0]), bool_Inferior_Equal_Int[1], "bool_Inferior_Equal_Int")
        self.assertEqual(parser.parseCondition(bool_Inferior_Equal_2_Int[0]), bool_Inferior_Equal_2_Int[1], "bool_Inferior_Equal_2_Int")
        self.assertEqual(parser.parseCondition(bool_Inferior_Equal_Float[0]), bool_Inferior_Equal_Float[1], "bool_Inferior_Equal_Float")
        self.assertEqual(parser.parseCondition(bool_Inferior_Equal_2_Float[0]), bool_Inferior_Equal_2_Float[1], "bool_Inferior_Equal_2_Float")
        self.assertEqual(parser.parseCondition(bool_Inferior_Equal_Bool[0]), bool_Inferior_Equal_Bool[1], "bool_Inferior_Equal_Bool")
        self.assertEqual(parser.parseCondition(bool_Inferior_Equal_2_Bool[0]), bool_Inferior_Equal_2_Bool[1], "bool_Superior_2_Bool")

    def testConditionInferior(self):

        parser = TemplateStr(variableDict=varDict)

        # String
        str_Inferior_Str: list = ["{{#'text' < 'text': yes || no}}", "no"]
        str_Inferior_2_Str: list = ["{{#'text' < 'texte': yes || no}}", "yes"]
        str_Inferior_Int: list = ["{{#'text' < <n:4>: yes || no}}", "no"]
        str_Inferior_2_Int: list = ["{{#'text' < <n:123>: yes || no}}", "yes"]
        str_Inferior_Float: list = ["{{#'text' < <n:4.5>: yes || no}}", "yes"]
        str_Inferior_2_Float: list = ["{{#'text' < <n:3.5>: yes || no}}", "no"]
        str_Inferior_Bool: list = ["{{#'text' < <b:True>: yes || no}}", "no"]
        str_Inferior_2_Bool: list = ["{{#'text' < <b:False>: yes || no}}", "no"]

        self.assertEqual(parser.parseCondition(str_Inferior_Str[0]), str_Inferior_Str[1], "str_Inferior_Str")
        self.assertEqual(parser.parseCondition(str_Inferior_2_Str[0]), str_Inferior_2_Str[1], "str_Inferior_2_Str")
        self.assertEqual(parser.parseCondition(str_Inferior_Int[0]), str_Inferior_Int[1], "str_Inferior_Int")
        self.assertEqual(parser.parseCondition(str_Inferior_2_Int[0]), str_Inferior_2_Int[1], "str_Inferior_2_Int")
        self.assertEqual(parser.parseCondition(str_Inferior_Float[0]), str_Inferior_Float[1], "str_Inferior_Float")
        self.assertEqual(parser.parseCondition(str_Inferior_2_Float[0]), str_Inferior_2_Float[1], "str_Inferior_2_Float")
        self.assertEqual(parser.parseCondition(str_Inferior_Bool[0]), str_Inferior_Bool[1], "str_Inferior_Bool")
        self.assertEqual(parser.parseCondition(str_Inferior_2_Bool[0]), str_Inferior_2_Bool[1], "str_Inferior_2_Bool")

        # Int
        int_Inferior_Str: list = ["{{#<n:4> < 'text': yes || no}}", "no"]
        int_Inferior_2_Str: list = ["{{#<n:4> < 'texte': yes || no}}", "yes"]
        int_Inferior_Int: list = ["{{#<n:4> < <n:4>: yes || no}}", "no"]
        int_Inferior_2_Int: list = ["{{#<n:4> < <n:5>: yes || no}}", "yes"]
        int_Inferior_Float: list = ["{{#<n:4> < <n:3.5>: yes || no}}", "no"]
        int_Inferior_2_Float: list = ["{{#<n:4> < <n:4.5>: yes || no}}", "yes"]
        int_Inferior_Bool: list = ["{{#<n:4> < <b:True>: yes || no}}", "no"]
        int_Inferior_2_Bool: list = ["{{#<n:4> < <b:False>: yes || no}}", "no"]

        self.assertEqual(parser.parseCondition(int_Inferior_Str[0]), int_Inferior_Str[1], "int_Inferior_Str")
        self.assertEqual(parser.parseCondition(int_Inferior_2_Str[0]), int_Inferior_2_Str[1], "int_Inferior_2_Str")
        self.assertEqual(parser.parseCondition(int_Inferior_Int[0]), int_Inferior_Int[1], "int_Inferior_Int")
        self.assertEqual(parser.parseCondition(int_Inferior_2_Int[0]), int_Inferior_2_Int[1], "int_Inferior_2_Int")
        self.assertEqual(parser.parseCondition(int_Inferior_Float[0]), int_Inferior_Float[1], "int_Inferior_Float")
        self.assertEqual(parser.parseCondition(int_Inferior_2_Float[0]), int_Inferior_2_Float[1], "int_Inferior_2_Float")
        self.assertEqual(parser.parseCondition(int_Inferior_Bool[0]), int_Inferior_Bool[1], "int_Inferior_Bool")
        self.assertEqual(parser.parseCondition(int_Inferior_2_Bool[0]), int_Inferior_2_Bool[1], "int_Inferior_2_Bool")

        # Float
        float_Inferior_Str: list = ["{{#<n:4.5> < 'text': yes || no}}", "no"]
        float_Inferior_2_Str: list = ["{{#<n:4.5> < 'texte': yes || no}}", "yes"]
        float_Inferior_Int: list = ["{{#<n:4.5> < <n:4>: yes || no}}", "no"]
        float_Inferior_2_Int: list = ["{{#<n:4.5> < <n:5>: yes || no}}", "yes"]
        float_Inferior_Float: list = ["{{#<n:4.5> < <n:4.4>: yes || no}}", "no"]
        float_Inferior_2_Float: list = ["{{#<n:4.5> < <n:4.6>: yes || no}}", "yes"]
        float_Inferior_Bool: list = ["{{#<n:4.5> < <b:True>: yes || no}}", "no"]
        float_Inferior_2_Bool: list = ["{{#<n:4.5> < <b:False>: yes || no}}", "no"]

        self.assertEqual(parser.parseCondition(float_Inferior_Str[0]), float_Inferior_Str[1], "float_Inferior_Str")
        self.assertEqual(parser.parseCondition(float_Inferior_2_Str[0]), float_Inferior_2_Str[1], "float_Inferior_2_Str")
        self.assertEqual(parser.parseCondition(float_Inferior_Int[0]), float_Inferior_Int[1], "float_Inferior_Int")
        self.assertEqual(parser.parseCondition(float_Inferior_2_Int[0]), float_Inferior_2_Int[1], "float_Inferior_2_Int")
        self.assertEqual(parser.parseCondition(float_Inferior_Float[0]), float_Inferior_Float[1], "float_Inferior_Float")
        self.assertEqual(parser.parseCondition(float_Inferior_2_Float[0]), float_Inferior_2_Float[1], "float_Inferior_2_Float")
        self.assertEqual(parser.parseCondition(float_Inferior_Bool[0]), float_Inferior_Bool[1], "float_Inferior_Bool")
        self.assertEqual(parser.parseCondition(float_Inferior_2_Bool[0]), float_Inferior_2_Bool[1], "float_Inferior_2_Bool")

        # Bool
        bool_Inferior_Str: list = ["{{#<b:True> < 'text': yes || no}}", "yes"]
        bool_Inferior_2_Str: list = ["{{#<b:False> < 'texte': yes || no}}", "yes"]
        bool_Inferior_Int: list = ["{{#<b:True> < <n:4>: yes || no}}", "yes"]
        bool_Inferior_2_Int: list = ["{{#<b:False> < <n:5>: yes || no}}", "yes"]
        bool_Inferior_Float: list = ["{{#<b:True> < <n:4.4>: yes || no}}", "yes"]
        bool_Inferior_2_Float: list = ["{{#<b:False> < <n:4.6>: yes || no}}", "yes"]
        bool_Inferior_Bool: list = ["{{#<b:True> < <b:True>: yes || no}}", "no"]
        bool_Inferior_2_Bool: list = ["{{#<b:False> < <b:False>: yes || no}}", "no"]

        self.assertEqual(parser.parseCondition(bool_Inferior_Str[0]), bool_Inferior_Str[1], "bool_Inferior_Str")
        self.assertEqual(parser.parseCondition(bool_Inferior_2_Str[0]), bool_Inferior_2_Str[1], "bool_Inferior_2_Str")
        self.assertEqual(parser.parseCondition(bool_Inferior_Int[0]), bool_Inferior_Int[1], "bool_Inferior_Int")
        self.assertEqual(parser.parseCondition(bool_Inferior_2_Int[0]), bool_Inferior_2_Int[1], "bool_Inferior_2_Int")
        self.assertEqual(parser.parseCondition(bool_Inferior_Float[0]), bool_Inferior_Float[1], "bool_Inferior_Float")
        self.assertEqual(parser.parseCondition(bool_Inferior_2_Float[0]), bool_Inferior_2_Float[1], "bool_Inferior_2_Float")
        self.assertEqual(parser.parseCondition(bool_Inferior_Bool[0]), bool_Inferior_Bool[1], "bool_Inferior_Bool")
        self.assertEqual(parser.parseCondition(bool_Inferior_2_Bool[0]), bool_Inferior_2_Bool[1], "bool_Superior_2_Bool")

    def testSwitch(self):
        text_Switch_1: list = ["{{?name; Jame=#0, Tony:=#1, Marco:=#2, default=#default}}", "#0"]
        text_Switch_2: list = ["{{?age:int; 56=#0, 36=#1, 32=#2, default=#default}}", "#2"]
        text_Switch_3: list = ["{{?lower:str; azertY=#0, Azerty=#1, AzErTy=#2, default=#default}}", "#default"]

        parser = TemplateStr(variableDict=varDict)

        self.assertEqual(parser.parseSwitch(text_Switch_1[0]), text_Switch_1[1], "text_Switch_1")
        self.assertEqual(parser.parseSwitch(text_Switch_2[0]), text_Switch_2[1], "text_Switch_2")
        self.assertEqual(parser.parseSwitch(text_Switch_3[0]), text_Switch_3[1], "text_Switch_3")

class TestHasMethode(unittest.TestCase):

    def testHasVariable(self):

        text_Has_Variable_1: list = ["{{$bool}} and {{$name}}", True]
        text_Has_Variable_2: list = ["{{$bool}} and {{@uppercase lower}}", True]
        text_Has_Variable_3: list = ["{{@uppercaseFirst bool}} and {{@uppercase lower}}", False]

        parser = TemplateStr()

        self.assertEqual(parser.hasVariable(text_Has_Variable_1[0]), text_Has_Variable_1[1], "text_Has_Variable_1")
        self.assertEqual(parser.hasVariable(text_Has_Variable_2[0]), text_Has_Variable_2[1], "text_Has_Variable_2")
        self.assertEqual(parser.hasVariable(text_Has_Variable_3[0]), text_Has_Variable_3[1], "text_Has_Variable_3")

    def testHasFunction(self):

        text_Has_Function_1: list = ["{{@uppercase lower}} and {{@uppercaseFirst lower}}", True]
        text_Has_Function_2: list = ["{{@uppercase lower}} and {{#'text' > 'text': yes || no}}", True]
        text_Has_Function_3: list = ["{{#'text' > 'text': yes || no}} and {{#'text' < 'text': yes || no}}", False]

        parser = TemplateStr()

        self.assertEqual(parser.hasFunction(text_Has_Function_1[0]), text_Has_Function_1[1], "text_Has_Function_1")
        self.assertEqual(parser.hasFunction(text_Has_Function_2[0]), text_Has_Function_2[1], "text_Has_Function_2")
        self.assertEqual(parser.hasFunction(text_Has_Function_3[0]), text_Has_Function_3[1], "text_Has_Function_3")

    def testHasCondition(self):

        text_Has_Condition_1: list = ["{{#'text' > 'text': yes || no}} and {{#'text' < 'text': yes || no}}", True]
        text_Has_Condition_2: list = ["{{#'text' > 'text': yes || no}} and {{?age:int; 56=#0, 36=#1, 32=#2, default=#default}}", True]
        text_Has_Condition_3: list = ["{{?age:int; 56=#0, 36=#1, 32=#2, default=#default}} and {{?age:int; 56=#0, 36=#1, 32=#2, default=#default}}", False]

        parser = TemplateStr()

        self.assertEqual(parser.hasCondition(text_Has_Condition_1[0]), text_Has_Condition_1[1], "text_Has_Condition_1")
        self.assertEqual(parser.hasCondition(text_Has_Condition_2[0]), text_Has_Condition_2[1], "text_Has_Condition_2")
        self.assertEqual(parser.hasCondition(text_Has_Condition_3[0]), text_Has_Condition_3[1], "text_Has_Condition_3")

    def testHasSwitch(self):

        text_Has_Condition_1: list = ["{{?age:int; 56=#0, 36=#1, 32=#2, default=#default}} and {{?age:int; 56=#0, 36=#1, 32=#2, default=#default}}", True]
        text_Has_Condition_2: list = ["{{?age:int; 56=#0, 36=#1, 32=#2, default=#default}} and {{$bool}}", True]
        text_Has_Condition_3: list = ["{{$bool}} and {{$name}}", False]

        parser = TemplateStr()

        self.assertEqual(parser.hasSwitch(text_Has_Condition_1[0]), text_Has_Condition_1[1], "text_Has_Condition_1")
        self.assertEqual(parser.hasSwitch(text_Has_Condition_2[0]), text_Has_Condition_2[1], "text_Has_Condition_2")
        self.assertEqual(parser.hasSwitch(text_Has_Condition_3[0]), text_Has_Condition_3[1], "text_Has_Condition_3")


if __name__ == '__main__':
    test_order = [
        "testAll",
        "testVariable", 
        "testFunction",
        "testCustomFunction",
        "testConditionEqual",
        "testConditionNoTEqual",
        "testConditionSuperiorEqual",
        "testConditionSuperior",
        "testConditionInferiorEqual",
        "testConditionInferior",
        "testSwitch",
        "testHasVariable",
        "testHasFunction",
        "testHasCondition",
        "testHasSwitch",
    ]
    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = lambda x, y: test_order.index(x) - test_order.index(y)
    unittest.main(testLoader=loader, verbosity=2)
