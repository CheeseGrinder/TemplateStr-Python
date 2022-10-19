import unittest
from templateStr import TemplateStr
from templateStr.error import NotFoundVariableError
from time import strftime, localtime

def test() -> str:
    return "Test1"

def testType(array:list) -> str:

    result = "ok"

    # print(array)

    a = array[0]
    b = array[1]
    c = array[2]
    d = array[3]
    e = array[4]
    f = array[5]
    g = array[6]
    h = array[7]
    i = array[8]
    j = array[9]
    
    # test a

    if type(a) != str: 
        result = "type a != str"
    else:
        if a != "text":
            result = "a != text"

    #  test b

    if type(b) != str: 
        result = "type b != str"
    else:
        if b != "text":
            result = "b != text"

    #  test c

    if type(c) != str: 
        result = "type c != str"
    else:
        if c != "text":
            result = "c != text"

    #  test d

    if type(d) != bool: 
        result = "type d != bool"
    else:
        if d != True:
            result = "d != True"

    #  test e

    if type(e) != int: 
        result = "type e != int"
    else:
        if e != 123:
            result = "e != 123"

    # test f

    if type(f) != float:
        result = "type f != float"
    else:
        if f != 123.4:
            result = "f != 123.4"

    # test g

    if type(g) != int:
        result = "type g != int"
    else:
        if g != 32:
            result = "g != 32"

    # test h

    if type(h) != int:
        result = "type h != int"
    else:
        if h != 42:
            result = "h != 42"

    # test i

    if type(i) != list:
        result = "type i != list"
    else:
        if i[1] != 56:
            result = "i != '56'"

    # test j

    if type(j) != str:
        result = "type j != str"
    else:
        if j != "Dict in Dict":
            result = "j != 'Dict in Dict'"

    return result

funcs: list = [testType, test]
varDict: dict = {
    "Build": "Succes",
    "var": "int",
    "str": "Jame",
    "int": 32,
    "float": 4.2,
    "bool": True, 
    "lower": "azerty", 
    "upper": "AZERTY", 
    "swap": "AzErTy",
    "list": ["test", 42],
    # "cfold": "grüßen",
    "Dict": {"value": "Dict in Dict"},
    "MasterDict": {"SecondDict": {"value": "Dict in Dict in Dict"}},
}

class TestParseMethode(unittest.TestCase):

    def testAll(self):

        text_1: list = ["Name is @{uppercase; str}, ${int} years old. Dict: ${Dict.value}. my keyboard: #{lower == 'azerty'; azerty | qwerty}, ?{lower; azerty::yes, AZERTY::yo, _::ynyway}",
             "Name is JAME, 32 years old. Dict: Dict in Dict. my keyboard: azerty, yes"]
        text_2: list = ["test var in var ${${var}}", "test var in var 32"]
        text_3: list = ["test if in if #{lower == 'azerty2'; azerty | #{lower == 'querty'; yes | no}}", "test if in if no"]
        text_4: list = ["test switch in switch ?{str; Jame::?{Build; Succes::#0, Failed::#1, _::#default}, Tony::#1, Marco::#2, _::#default}", "test switch in switch #0"]
        text_5: list = ["test wtf ?{str; Jame::?{int/${var}; 32::#0, 36::#1, _::#default}, Tony::#1, Marco::#2, _::#default2}", "test wtf #0"]

        text_error_1: list = ["test func in func @{lowercase; @{uppercase; str}}", "[key 'JAME' not exist]"]

        parser = TemplateStr(funcs, varDict)

        self.assertEqual(parser.parse(text_1[0]), text_1[1], "text_1")
        self.assertEqual(parser.parse(text_2[0]), text_2[1], "text_2")
        self.assertEqual(parser.parse(text_3[0]), text_3[1], "text_3")
        self.assertEqual(parser.parse(text_4[0]), text_4[1], "text_4")
        self.assertEqual(parser.parse(text_5[0]), text_5[1], "text_5")

        try:
            parser.parse(text_error_1[0])
        except NotFoundVariableError as err:
            self.assertEqual(str(err), text_error_1[1], "text_error_1")

    def testVariable(self):

        text_1: list = ["var bool = ${bool} and name = ${str}", "var bool = True and name = Jame"]
        text_2: list = ["${Dict.value}", "Dict in Dict"]
        text_3: list = ["${MasterDict.SecondDict.value}", "Dict in Dict in Dict"]
        text_4: list = ["${list[1]}", "42"]

        text_error_1: list = ["${word}", "[key 'word' not exist]"]
        text_error_2: list = ["${dict.dict1.value}", "[key 'dict.dict1.value' not exist]"]
        text_error_3: list = ["${lists[1]}", "[key 'lists' not exist]"]
        text_error_4: list = ["${list[2]}", "[index '2' out of range]"]

        parser = TemplateStr(variableDict=varDict)

        self.assertEqual(parser.parseVariable(text_1[0]), text_1[1], "text_1")
        self.assertEqual(parser.parseVariable(text_2[0]), text_2[1], "text_2")
        self.assertEqual(parser.parseVariable(text_3[0]), text_3[1], "text_3")
        self.assertEqual(parser.parseVariable(text_4[0]), text_4[1], "text_4")

        try:
            parser.parseVariable(text_error_1[0])
        except NotFoundVariableError as err:
            self.assertEqual(str(err), text_error_1[1], "text_error_1")

        try:
            parser.parseVariable(text_error_2[0])
        except NotFoundVariableError as err:
            self.assertEqual(str(err), text_error_2[1], "text_error_2")

        try:
            parser.parseVariable(text_error_3[0])
        except NotFoundVariableError as err:
            self.assertEqual(str(err), text_error_3[1], "text_error_3")

        try:
            parser.parseVariable(text_error_4[0])
        except IndexError as err:
            self.assertEqual(str(err), text_error_4[1], "text_error_4")
    
    def testInternFunction(self):

        uppercase: list = ["@{uppercase; lower}", "AZERTY"]
        uppercase2: list = ["@{uppercase; Dict.value}", "DICT IN DICT"]
        uppercaseFirst: list = ["@{uppercaseFirst; lower}", "Azerty"]
        lowercase: list = ["@{lowercase; upper}", "azerty"]
        # casefold: list = ["@{casefold cfold}", "grüssen"]
        swapcase: list = ["@{swapcase; swap}", "aZeRtY"]
        time: str = "@{time}"
        date: str = "@{date}"
        dateTime: str = "@{dateTime}"

        parser = TemplateStr(variableDict=varDict)

        self.assertEqual(parser.parseFunction(uppercase[0]), uppercase[1], "uppercase")
        self.assertEqual(parser.parseFunction(uppercase2[0]), uppercase2[1], "uppercase2")
        self.assertEqual(parser.parseFunction(uppercaseFirst[0]), uppercaseFirst[1], "uppercaseFirst")
        self.assertEqual(parser.parseFunction(lowercase[0]), lowercase[1], "lowercase")
        # self.assertEqual(parser.parseFunction(casefold[0]), casefold[1], "casefold")
        self.assertEqual(parser.parseFunction(swapcase[0]), swapcase[1], "swapcase")
        self.assertEqual(parser.parseFunction(time), strftime("%H:%M:%S", localtime()), "time")
        self.assertEqual(parser.parseFunction(date), strftime("%d/%m/%Y", localtime()), "date")
        self.assertEqual(parser.parseFunction(dateTime), strftime("%d/%m/%Y,%H:%M:%S", localtime()), "dateTime")

    def testCustomFunction(self):
        
        text_1: list = ["@{test}", "Test1"]
        testType: list = ["@{testType; \"text\" 'text' `text` b/True i/123 f/123.4 int list[1] ('test', i/56) Dict.value}", "ok"]

        parser = TemplateStr(funcs, varDict)

        self.assertEqual(parser.parseFunction(text_1[0]), text_1[1], "text_1")
        self.assertEqual(parser.parseFunction(testType[0]), testType[1], "testType")

    def testConditionEqual(self):

        str_Equal_Str: list = ["#{'text' == 'text'; yes | no}", "yes"]
        str_Equal2_Str: list = ["#{'text' == 'texte'; yes | no}", "no"]
        int_Equal_Str: list = ["#{i/4 == 'text'; yes | no}", "no"]
        float_Equal_Str: list = ["#{f/4.5 == 'text'; yes | no}", "no"]
        bool_Equal_Str: list = ["#{b/True == 'text'; yes | no}", "no"]
        var_Equal_Str: list = ["#{int == 'text'; yes | no}", "no"]

        parser = TemplateStr(variableDict=varDict)

        self.assertEqual(parser.parseCondition(str_Equal_Str[0]), str_Equal_Str[1], "str_Equal_Str")
        self.assertEqual(parser.parseCondition(str_Equal2_Str[0]), str_Equal2_Str[1], "str_Equal2_Str")
        self.assertEqual(parser.parseCondition(int_Equal_Str[0]), int_Equal_Str[1], "int_Equal_Str")
        self.assertEqual(parser.parseCondition(float_Equal_Str[0]), float_Equal_Str[1], "float_Equal_Str")
        self.assertEqual(parser.parseCondition(bool_Equal_Str[0]), bool_Equal_Str[1], "bool_Equal_Str")
        self.assertEqual(parser.parseCondition(var_Equal_Str[0]), var_Equal_Str[1], "var_Equal_Str")

    def testConditionNoTEqual(self):

        str_NoT_Equal_Str: list = ["#{'text' != 'text'; yes | no}", "no"]
        str_NoT_Equal2_Str: list = ["#{'text' != 'texte'; yes | no}", "yes"]
        int_NoT_Equal_Str: list = ["#{i/4 != 'text'; yes | no}", "yes"]
        float_NoT_Equal_Str: list = ["#{f/4.5 != 'text'; yes | no}", "yes"]
        bool_NoT_Equal_Str: list = ["#{b/True != 'text'; yes | no}", "yes"]
        var_NoT_Equal_Str: list = ["#{int != 'text'; yes | no}", "yes"]

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
        str_Superior_Equal_Str: list = ["#{'text' >= 'text'; yes | no}", "yes"]
        str_Superior_Equal_2_Str: list = ["#{'text' >= 'texte'; yes | no}", "no"]
        str_Superior_Equal_Int: list = ["#{'text' >= i/4; yes | no}", "yes"]
        str_Superior_Equal_2_Int: list = ["#{'text' >= i/123; yes | no}", "no"]
        str_Superior_Equal_Float: list = ["#{'text' >= f/4.5; yes | no}", "no"]
        str_Superior_Equal_2_Float: list = ["#{'text' >= f/3.5; yes | no}", "yes"]
        str_Superior_Equal_Bool: list = ["#{'text' >= b/True; yes | no}", "yes"]
        str_Superior_Equal_2_Bool: list = ["#{'text' >= b/False; yes | no}", "yes"]

        self.assertEqual(parser.parseCondition(str_Superior_Equal_Str[0]), str_Superior_Equal_Str[1], "str_Superior_Equal_Str")
        self.assertEqual(parser.parseCondition(str_Superior_Equal_2_Str[0]), str_Superior_Equal_2_Str[1], "str_Superior_Equal_2_Str")
        self.assertEqual(parser.parseCondition(str_Superior_Equal_Int[0]), str_Superior_Equal_Int[1], "str_Superior_Equal_Int")
        self.assertEqual(parser.parseCondition(str_Superior_Equal_2_Int[0]), str_Superior_Equal_2_Int[1], "str_Superior_Equal_2_Int")
        self.assertEqual(parser.parseCondition(str_Superior_Equal_Float[0]), str_Superior_Equal_Float[1], "str_Superior_Equal_Float")
        self.assertEqual(parser.parseCondition(str_Superior_Equal_2_Float[0]), str_Superior_Equal_2_Float[1], "str_Superior_Equal_2_Float")
        self.assertEqual(parser.parseCondition(str_Superior_Equal_Bool[0]), str_Superior_Equal_Bool[1], "str_Superior_Equal_Bool")
        self.assertEqual(parser.parseCondition(str_Superior_Equal_2_Bool[0]), str_Superior_Equal_2_Bool[1], "str_Superior_Equal_2_Bool")

        # Int
        int_Superior_Equal_Str: list = ["#{i/4 >= 'text'; yes | no}", "yes"]
        int_Superior_Equal_2_Str: list = ["#{i/4 >= 'texte'; yes | no}", "no"]
        int_Superior_Equal_Int: list = ["#{i/4 >= i/4; yes | no}", "yes"]
        int_Superior_Equal_2_Int: list = ["#{i/4 >= i/5; yes | no}", "no"]
        int_Superior_Equal_Float: list = ["#{i/4 >= f/3.5; yes | no}", "yes"]
        int_Superior_Equal_2_Float: list = ["#{i/4 >= f/4.5; yes | no}", "no"]
        int_Superior_Equal_Bool: list = ["#{i/4 >= b/True; yes | no}", "yes"]
        int_Superior_Equal_2_Bool: list = ["#{i/4 >= b/False; yes | no}", "yes"]

        self.assertEqual(parser.parseCondition(int_Superior_Equal_Str[0]), int_Superior_Equal_Str[1], "int_Superior_Equal_Str")
        self.assertEqual(parser.parseCondition(int_Superior_Equal_2_Str[0]), int_Superior_Equal_2_Str[1], "int_Superior_Equal_2_Str")
        self.assertEqual(parser.parseCondition(int_Superior_Equal_Int[0]), int_Superior_Equal_Int[1], "int_Superior_Equal_Int")
        self.assertEqual(parser.parseCondition(int_Superior_Equal_2_Int[0]), int_Superior_Equal_2_Int[1], "int_Superior_Equal_2_Int")
        self.assertEqual(parser.parseCondition(int_Superior_Equal_Float[0]), int_Superior_Equal_Float[1], "int_Superior_Equal_Float")
        self.assertEqual(parser.parseCondition(int_Superior_Equal_2_Float[0]), int_Superior_Equal_2_Float[1], "int_Superior_Equal_2_Float")
        self.assertEqual(parser.parseCondition(int_Superior_Equal_Bool[0]), int_Superior_Equal_Bool[1], "int_Superior_Equal_Bool")
        self.assertEqual(parser.parseCondition(int_Superior_Equal_2_Bool[0]), int_Superior_Equal_2_Bool[1], "int_Superior_Equal_2_Bool")

        # Float
        float_Superior_Equal_Str: list = ["#{f/4.5 >= 'text'; yes | no}", "yes"]
        float_Superior_Equal_2_Str: list = ["#{f/4.5 >= 'texte'; yes | no}", "no"]
        float_Superior_Equal_Int: list = ["#{f/4.5 >= i/4; yes | no}", "yes"]
        float_Superior_Equal_2_Int: list = ["#{f/4.5 >= i/5; yes | no}", "no"]
        float_Superior_Equal_Float: list = ["#{f/4.5 >= f/4.4; yes | no}", "yes"]
        float_Superior_Equal_2_Float: list = ["#{f/4.5 >= f/4.6; yes | no}", "no"]
        float_Superior_Equal_Bool: list = ["#{f/4.5 >= b/True; yes | no}", "yes"]
        float_Superior_Equal_2_Bool: list = ["#{f/4.5 >= b/False; yes | no}", "yes"]

        self.assertEqual(parser.parseCondition(float_Superior_Equal_Str[0]), float_Superior_Equal_Str[1], "float_Superior_Equal_Str")
        self.assertEqual(parser.parseCondition(float_Superior_Equal_2_Str[0]), float_Superior_Equal_2_Str[1], "float_Superior_Equal_2_Str")
        self.assertEqual(parser.parseCondition(float_Superior_Equal_Int[0]), float_Superior_Equal_Int[1], "float_Superior_Equal_Int")
        self.assertEqual(parser.parseCondition(float_Superior_Equal_2_Int[0]), float_Superior_Equal_2_Int[1], "float_Superior_Equal_2_Int")
        self.assertEqual(parser.parseCondition(float_Superior_Equal_Float[0]), float_Superior_Equal_Float[1], "float_Superior_Equal_Float")
        self.assertEqual(parser.parseCondition(float_Superior_Equal_2_Float[0]), float_Superior_Equal_2_Float[1], "float_Superior_Equal_2_Float")
        self.assertEqual(parser.parseCondition(float_Superior_Equal_Bool[0]), float_Superior_Equal_Bool[1], "float_Superior_Equal_Bool")
        self.assertEqual(parser.parseCondition(float_Superior_Equal_2_Bool[0]), float_Superior_Equal_2_Bool[1], "float_Superior_Equal_2_Bool")

        # Bool
        bool_Superior_Equal_Str: list = ["#{b/True >= 'text'; yes | no}", "no"]
        bool_Superior_Equal_2_Str: list = ["#{b/False >= 'texte'; yes | no}", "no"]
        bool_Superior_Equal_Int: list = ["#{b/True >= i/4; yes | no}", "no"]
        bool_Superior_Equal_2_Int: list = ["#{b/False >= i/5; yes | no}", "no"]
        bool_Superior_Equal_Float: list = ["#{b/True >= f/4.4; yes | no}", "no"]
        bool_Superior_Equal_2_Float: list = ["#{b/False >= f/4.6; yes | no}", "no"]
        bool_Superior_Equal_Bool: list = ["#{b/True >= b/True; yes | no}", "yes"]
        bool_Superior_Equal_2_Bool: list = ["#{b/False >= b/False; yes | no}", "yes"]

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
        str_Superior_Str: list = ["#{'text' > 'text'; yes | no}", "no"]
        str_Superior_2_Str: list = ["#{'text' > 'texte'; yes | no}", "no"]
        str_Superior_Int: list = ["#{'text' > i/4; yes | no}", "no"]
        str_Superior_2_Int: list = ["#{'text' > i/123; yes | no}", "no"]
        str_Superior_Float: list = ["#{'text' > f/4.5; yes | no}", "no"]
        str_Superior_2_Float: list = ["#{'text' > f/3.5; yes | no}", "yes"]
        str_Superior_Bool: list = ["#{'text' > b/True; yes | no}", "yes"]
        str_Superior_2_Bool: list = ["#{'text' > b/False; yes | no}", "yes"]

        self.assertEqual(parser.parseCondition(str_Superior_Str[0]), str_Superior_Str[1], "str_Superior_Str")
        self.assertEqual(parser.parseCondition(str_Superior_2_Str[0]), str_Superior_2_Str[1], "str_Superior_2_Str")
        self.assertEqual(parser.parseCondition(str_Superior_Int[0]), str_Superior_Int[1], "str_Superior_Int")
        self.assertEqual(parser.parseCondition(str_Superior_2_Int[0]), str_Superior_2_Int[1], "str_Superior_2_Int")
        self.assertEqual(parser.parseCondition(str_Superior_Float[0]), str_Superior_Float[1], "str_Superior_Float")
        self.assertEqual(parser.parseCondition(str_Superior_2_Float[0]), str_Superior_2_Float[1], "str_Superior_2_Float")
        self.assertEqual(parser.parseCondition(str_Superior_Bool[0]), str_Superior_Bool[1], "str_Superior_Bool")
        self.assertEqual(parser.parseCondition(str_Superior_2_Bool[0]), str_Superior_2_Bool[1], "str_Superior_2_Bool")

        # Int
        int_Superior_Str: list = ["#{i/4 > 'text'; yes | no}", "no"]
        int_Superior_2_Str: list = ["#{i/4 > 'texte'; yes | no}", "no"]
        int_Superior_Int: list = ["#{i/4 > i/4; yes | no}", "no"]
        int_Superior_2_Int: list = ["#{i/4 > i/5; yes | no}", "no"]
        int_Superior_Float: list = ["#{i/4 > f/3.5; yes | no}", "yes"]
        int_Superior_2_Float: list = ["#{i/4 > f/4.5; yes | no}", "no"]
        int_Superior_Bool: list = ["#{i/4 > b/True; yes | no}", "yes"]
        int_Superior_2_Bool: list = ["#{i/4 > b/False; yes | no}", "yes"]

        self.assertEqual(parser.parseCondition(int_Superior_Str[0]), int_Superior_Str[1], "int_Superior_Str")
        self.assertEqual(parser.parseCondition(int_Superior_2_Str[0]), int_Superior_2_Str[1], "int_Superior_2_Str")
        self.assertEqual(parser.parseCondition(int_Superior_Int[0]), int_Superior_Int[1], "int_Superior_Int")
        self.assertEqual(parser.parseCondition(int_Superior_2_Int[0]), int_Superior_2_Int[1], "int_Superior_2_Int")
        self.assertEqual(parser.parseCondition(int_Superior_Float[0]), int_Superior_Float[1], "int_Superior_Float")
        self.assertEqual(parser.parseCondition(int_Superior_2_Float[0]), int_Superior_2_Float[1], "int_Superior_2_Float")
        self.assertEqual(parser.parseCondition(int_Superior_Bool[0]), int_Superior_Bool[1], "int_Superior_Bool")
        self.assertEqual(parser.parseCondition(int_Superior_2_Bool[0]), int_Superior_2_Bool[1], "int_Superior_2_Bool")

        # Float
        float_Superior_Str: list = ["#{f/4.5 > 'text'; yes | no}", "yes"]
        float_Superior_2_Str: list = ["#{f/4.5 > 'texte'; yes | no}", "no"]
        float_Superior_Int: list = ["#{f/4.5 > i/4; yes | no}", "yes"]
        float_Superior_2_Int: list = ["#{f/4.5 > i/5; yes | no}", "no"]
        float_Superior_Float: list = ["#{f/4.5 > f/4.4; yes | no}", "yes"]
        float_Superior_2_Float: list = ["#{f/4.5 > f/4.6; yes | no}", "no"]
        float_Superior_Bool: list = ["#{f/4.5 > b/True; yes | no}", "yes"]
        float_Superior_2_Bool: list = ["#{f/4.5 > b/False; yes | no}", "yes"]

        self.assertEqual(parser.parseCondition(float_Superior_Str[0]), float_Superior_Str[1], "float_Superior_Str")
        self.assertEqual(parser.parseCondition(float_Superior_2_Str[0]), float_Superior_2_Str[1], "float_Superior_2_Str")
        self.assertEqual(parser.parseCondition(float_Superior_Int[0]), float_Superior_Int[1], "float_Superior_Int")
        self.assertEqual(parser.parseCondition(float_Superior_2_Int[0]), float_Superior_2_Int[1], "float_Superior_2_Int")
        self.assertEqual(parser.parseCondition(float_Superior_Float[0]), float_Superior_Float[1], "float_Superior_Float")
        self.assertEqual(parser.parseCondition(float_Superior_2_Float[0]), float_Superior_2_Float[1], "float_Superior_2_Float")
        self.assertEqual(parser.parseCondition(float_Superior_Bool[0]), float_Superior_Bool[1], "float_Superior_Bool")
        self.assertEqual(parser.parseCondition(float_Superior_2_Bool[0]), float_Superior_2_Bool[1], "float_Superior_2_Bool")

        # Bool
        bool_Superior_Str: list = ["#{b/True > 'text'; yes | no}", "no"]
        bool_Superior_2_Str: list = ["#{b/False > 'texte'; yes | no}", "no"]
        bool_Superior_Int: list = ["#{b/True > i/4; yes | no}", "no"]
        bool_Superior_2_Int: list = ["#{b/False > i/5; yes | no}", "no"]
        bool_Superior_Float: list = ["#{b/True > f/4.4; yes | no}", "no"]
        bool_Superior_2_Float: list = ["#{b/False > f/4.6; yes | no}", "no"]
        bool_Superior_Bool: list = ["#{b/True > b/True; yes | no}", "no"]
        bool_Superior_2_Bool: list = ["#{b/False > b/False; yes | no}", "no"]

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
        str_Inferior_Equal_Str: list = ["#{'text' <= 'text'; yes | no}", "yes"]
        str_Inferior_Equal_2_Str: list = ["#{'text' <= 'texte'; yes | no}", "yes"]
        str_Inferior_Equal_Int: list = ["#{'text' <= i/4; yes | no}", "yes"]
        str_Inferior_Equal_2_Int: list = ["#{'text' <= i/123; yes | no}", "yes"]
        str_Inferior_Equal_Float: list = ["#{'text' <= f/4.5; yes | no}", "yes"]
        str_Inferior_Equal_2_Float: list = ["#{'text' <= f/3.5; yes | no}", "no"]
        str_Inferior_Equal_Bool: list = ["#{'text' <= b/True; yes | no}", "no"]
        str_Inferior_Equal_2_Bool: list = ["#{'text' <= b/False; yes | no}", "no"]

        self.assertEqual(parser.parseCondition(str_Inferior_Equal_Str[0]), str_Inferior_Equal_Str[1], "str_Inferior_Equal_Str")
        self.assertEqual(parser.parseCondition(str_Inferior_Equal_2_Str[0]), str_Inferior_Equal_2_Str[1], "str_Inferior_Equal_2_Str")
        self.assertEqual(parser.parseCondition(str_Inferior_Equal_Int[0]), str_Inferior_Equal_Int[1], "str_Inferior_Equal_Int")
        self.assertEqual(parser.parseCondition(str_Inferior_Equal_2_Int[0]), str_Inferior_Equal_2_Int[1], "str_Inferior_Equal_2_Int")
        self.assertEqual(parser.parseCondition(str_Inferior_Equal_Float[0]), str_Inferior_Equal_Float[1], "str_Inferior_Equal_Float")
        self.assertEqual(parser.parseCondition(str_Inferior_Equal_2_Float[0]), str_Inferior_Equal_2_Float[1], "str_Inferior_Equal_2_Float")
        self.assertEqual(parser.parseCondition(str_Inferior_Equal_Bool[0]), str_Inferior_Equal_Bool[1], "str_Inferior_Equal_Bool")
        self.assertEqual(parser.parseCondition(str_Inferior_Equal_2_Bool[0]), str_Inferior_Equal_2_Bool[1], "str_Inferior_Equal_2_Bool")

        # Int
        int_Inferior_Equal_Str: list = ["#{i/4 <= 'text'; yes | no}", "yes"]
        int_Inferior_Equal_2_Str: list = ["#{i/4 <= 'texte'; yes | no}", "yes"]
        int_Inferior_Equal_Int: list = ["#{i/4 <= i/4; yes | no}", "yes"]
        int_Inferior_Equal_2_Int: list = ["#{i/4 <= i/5; yes | no}", "yes"]
        int_Inferior_Equal_Float: list = ["#{i/4 <= f/3.5; yes | no}", "no"]
        int_Inferior_Equal_2_Float: list = ["#{i/4 <= f/4.5; yes | no}", "yes"]
        int_Inferior_Equal_Bool: list = ["#{i/4 <= b/True; yes | no}", "no"]
        int_Inferior_Equal_2_Bool: list = ["#{i/4 <= b/False; yes | no}", "no"]

        self.assertEqual(parser.parseCondition(int_Inferior_Equal_Str[0]), int_Inferior_Equal_Str[1], "int_Inferior_Equal_Str")
        self.assertEqual(parser.parseCondition(int_Inferior_Equal_2_Str[0]), int_Inferior_Equal_2_Str[1], "int_Inferior_Equal_2_Str")
        self.assertEqual(parser.parseCondition(int_Inferior_Equal_Int[0]), int_Inferior_Equal_Int[1], "int_Inferior_Equal_Int")
        self.assertEqual(parser.parseCondition(int_Inferior_Equal_2_Int[0]), int_Inferior_Equal_2_Int[1], "int_Inferior_Equal_2_Int")
        self.assertEqual(parser.parseCondition(int_Inferior_Equal_Float[0]), int_Inferior_Equal_Float[1], "int_Inferior_Equal_Float")
        self.assertEqual(parser.parseCondition(int_Inferior_Equal_2_Float[0]), int_Inferior_Equal_2_Float[1], "int_Inferior_Equal_2_Float")
        self.assertEqual(parser.parseCondition(int_Inferior_Equal_Bool[0]), int_Inferior_Equal_Bool[1], "int_Inferior_Equal_Bool")
        self.assertEqual(parser.parseCondition(int_Inferior_Equal_2_Bool[0]), int_Inferior_Equal_2_Bool[1], "int_Inferior_Equal_2_Bool")

        # Float
        float_Inferior_Equal_Str: list = ["#{f/4.5 <= 'text'; yes | no}", "no"]
        float_Inferior_Equal_2_Str: list = ["#{f/4.5 <= 'texte'; yes | no}", "yes"]
        float_Inferior_Equal_Int: list = ["#{f/4.5 <= i/4; yes | no}", "no"]
        float_Inferior_Equal_2_Int: list = ["#{f/4.5 <= i/5; yes | no}", "yes"]
        float_Inferior_Equal_Float: list = ["#{f/4.5 <= f/4.4; yes | no}", "no"]
        float_Inferior_Equal_2_Float: list = ["#{f/4.5 <= f/4.6; yes | no}", "yes"]
        float_Inferior_Equal_Bool: list = ["#{f/4.5 <= b/True; yes | no}", "no"]
        float_Inferior_Equal_2_Bool: list = ["#{f/4.5 <= b/False; yes | no}", "no"]

        self.assertEqual(parser.parseCondition(float_Inferior_Equal_Str[0]), float_Inferior_Equal_Str[1], "float_Inferior_Equal_Str")
        self.assertEqual(parser.parseCondition(float_Inferior_Equal_2_Str[0]), float_Inferior_Equal_2_Str[1], "float_Inferior_Equal_2_Str")
        self.assertEqual(parser.parseCondition(float_Inferior_Equal_Int[0]), float_Inferior_Equal_Int[1], "float_Inferior_Equal_Int")
        self.assertEqual(parser.parseCondition(float_Inferior_Equal_2_Int[0]), float_Inferior_Equal_2_Int[1], "float_Inferior_Equal_2_Int")
        self.assertEqual(parser.parseCondition(float_Inferior_Equal_Float[0]), float_Inferior_Equal_Float[1], "float_Inferior_Equal_Float")
        self.assertEqual(parser.parseCondition(float_Inferior_Equal_2_Float[0]), float_Inferior_Equal_2_Float[1], "float_Inferior_Equal_2_Float")
        self.assertEqual(parser.parseCondition(float_Inferior_Equal_Bool[0]), float_Inferior_Equal_Bool[1], "float_Inferior_Equal_Bool")
        self.assertEqual(parser.parseCondition(float_Inferior_Equal_2_Bool[0]), float_Inferior_Equal_2_Bool[1], "float_Inferior_Equal_2_Bool")

        # Bool
        bool_Inferior_Equal_Str: list = ["#{b/True <= 'text'; yes | no}", "yes"]
        bool_Inferior_Equal_2_Str: list = ["#{b/False <= 'texte'; yes | no}", "yes"]
        bool_Inferior_Equal_Int: list = ["#{b/True <= i/4; yes | no}", "yes"]
        bool_Inferior_Equal_2_Int: list = ["#{b/False <= i/5; yes | no}", "yes"]
        bool_Inferior_Equal_Float: list = ["#{b/True <= f/4.4; yes | no}", "yes"]
        bool_Inferior_Equal_2_Float: list = ["#{b/False <= f/4.6; yes | no}", "yes"]
        bool_Inferior_Equal_Bool: list = ["#{b/True <= b/True; yes | no}", "yes"]
        bool_Inferior_Equal_2_Bool: list = ["#{b/False <= b/False; yes | no}", "yes"]

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
        str_Inferior_Str: list = ["#{'text' < 'text'; yes | no}", "no"]
        str_Inferior_2_Str: list = ["#{'text' < 'texte'; yes | no}", "yes"]
        str_Inferior_Int: list = ["#{'text' < i/4; yes | no}", "no"]
        str_Inferior_2_Int: list = ["#{'text' < i/123; yes | no}", "yes"]
        str_Inferior_Float: list = ["#{'text' < f/4.5; yes | no}", "yes"]
        str_Inferior_2_Float: list = ["#{'text' < f/3.5; yes | no}", "no"]
        str_Inferior_Bool: list = ["#{'text' < b/True; yes | no}", "no"]
        str_Inferior_2_Bool: list = ["#{'text' < b/False; yes | no}", "no"]

        self.assertEqual(parser.parseCondition(str_Inferior_Str[0]), str_Inferior_Str[1], "str_Inferior_Str")
        self.assertEqual(parser.parseCondition(str_Inferior_2_Str[0]), str_Inferior_2_Str[1], "str_Inferior_2_Str")
        self.assertEqual(parser.parseCondition(str_Inferior_Int[0]), str_Inferior_Int[1], "str_Inferior_Int")
        self.assertEqual(parser.parseCondition(str_Inferior_2_Int[0]), str_Inferior_2_Int[1], "str_Inferior_2_Int")
        self.assertEqual(parser.parseCondition(str_Inferior_Float[0]), str_Inferior_Float[1], "str_Inferior_Float")
        self.assertEqual(parser.parseCondition(str_Inferior_2_Float[0]), str_Inferior_2_Float[1], "str_Inferior_2_Float")
        self.assertEqual(parser.parseCondition(str_Inferior_Bool[0]), str_Inferior_Bool[1], "str_Inferior_Bool")
        self.assertEqual(parser.parseCondition(str_Inferior_2_Bool[0]), str_Inferior_2_Bool[1], "str_Inferior_2_Bool")

        # Int
        int_Inferior_Str: list = ["#{i/4 < 'text'; yes | no}", "no"]
        int_Inferior_2_Str: list = ["#{i/4 < 'texte'; yes | no}", "yes"]
        int_Inferior_Int: list = ["#{i/4 < i/4; yes | no}", "no"]
        int_Inferior_2_Int: list = ["#{i/4 < i/5; yes | no}", "yes"]
        int_Inferior_Float: list = ["#{i/4 < f/3.5; yes | no}", "no"]
        int_Inferior_2_Float: list = ["#{i/4 < f/4.5; yes | no}", "yes"]
        int_Inferior_Bool: list = ["#{i/4 < b/True; yes | no}", "no"]
        int_Inferior_2_Bool: list = ["#{i/4 < b/False; yes | no}", "no"]

        self.assertEqual(parser.parseCondition(int_Inferior_Str[0]), int_Inferior_Str[1], "int_Inferior_Str")
        self.assertEqual(parser.parseCondition(int_Inferior_2_Str[0]), int_Inferior_2_Str[1], "int_Inferior_2_Str")
        self.assertEqual(parser.parseCondition(int_Inferior_Int[0]), int_Inferior_Int[1], "int_Inferior_Int")
        self.assertEqual(parser.parseCondition(int_Inferior_2_Int[0]), int_Inferior_2_Int[1], "int_Inferior_2_Int")
        self.assertEqual(parser.parseCondition(int_Inferior_Float[0]), int_Inferior_Float[1], "int_Inferior_Float")
        self.assertEqual(parser.parseCondition(int_Inferior_2_Float[0]), int_Inferior_2_Float[1], "int_Inferior_2_Float")
        self.assertEqual(parser.parseCondition(int_Inferior_Bool[0]), int_Inferior_Bool[1], "int_Inferior_Bool")
        self.assertEqual(parser.parseCondition(int_Inferior_2_Bool[0]), int_Inferior_2_Bool[1], "int_Inferior_2_Bool")

        # Float
        float_Inferior_Str: list = ["#{f/4.5 < 'text'; yes | no}", "no"]
        float_Inferior_2_Str: list = ["#{f/4.5 < 'texte'; yes | no}", "yes"]
        float_Inferior_Int: list = ["#{f/4.5 < i/4; yes | no}", "no"]
        float_Inferior_2_Int: list = ["#{f/4.5 < i/5; yes | no}", "yes"]
        float_Inferior_Float: list = ["#{f/4.5 < f/4.4; yes | no}", "no"]
        float_Inferior_2_Float: list = ["#{f/4.5 < f/4.6; yes | no}", "yes"]
        float_Inferior_Bool: list = ["#{f/4.5 < b/True; yes | no}", "no"]
        float_Inferior_2_Bool: list = ["#{f/4.5 < b/False; yes | no}", "no"]

        self.assertEqual(parser.parseCondition(float_Inferior_Str[0]), float_Inferior_Str[1], "float_Inferior_Str")
        self.assertEqual(parser.parseCondition(float_Inferior_2_Str[0]), float_Inferior_2_Str[1], "float_Inferior_2_Str")
        self.assertEqual(parser.parseCondition(float_Inferior_Int[0]), float_Inferior_Int[1], "float_Inferior_Int")
        self.assertEqual(parser.parseCondition(float_Inferior_2_Int[0]), float_Inferior_2_Int[1], "float_Inferior_2_Int")
        self.assertEqual(parser.parseCondition(float_Inferior_Float[0]), float_Inferior_Float[1], "float_Inferior_Float")
        self.assertEqual(parser.parseCondition(float_Inferior_2_Float[0]), float_Inferior_2_Float[1], "float_Inferior_2_Float")
        self.assertEqual(parser.parseCondition(float_Inferior_Bool[0]), float_Inferior_Bool[1], "float_Inferior_Bool")
        self.assertEqual(parser.parseCondition(float_Inferior_2_Bool[0]), float_Inferior_2_Bool[1], "float_Inferior_2_Bool")

        # Bool
        bool_Inferior_Str: list = ["#{b/True < 'text'; yes | no}", "yes"]
        bool_Inferior_2_Str: list = ["#{b/False < 'texte'; yes | no}", "yes"]
        bool_Inferior_Int: list = ["#{b/True < i/4; yes | no}", "yes"]
        bool_Inferior_2_Int: list = ["#{b/False < i/5; yes | no}", "yes"]
        bool_Inferior_Float: list = ["#{b/True < f/4.4; yes | no}", "yes"]
        bool_Inferior_2_Float: list = ["#{b/False < f/4.6; yes | no}", "yes"]
        bool_Inferior_Bool: list = ["#{b/True < b/True; yes | no}", "no"]
        bool_Inferior_2_Bool: list = ["#{b/False < b/False; yes | no}", "no"]

        self.assertEqual(parser.parseCondition(bool_Inferior_Str[0]), bool_Inferior_Str[1], "bool_Inferior_Str")
        self.assertEqual(parser.parseCondition(bool_Inferior_2_Str[0]), bool_Inferior_2_Str[1], "bool_Inferior_2_Str")
        self.assertEqual(parser.parseCondition(bool_Inferior_Int[0]), bool_Inferior_Int[1], "bool_Inferior_Int")
        self.assertEqual(parser.parseCondition(bool_Inferior_2_Int[0]), bool_Inferior_2_Int[1], "bool_Inferior_2_Int")
        self.assertEqual(parser.parseCondition(bool_Inferior_Float[0]), bool_Inferior_Float[1], "bool_Inferior_Float")
        self.assertEqual(parser.parseCondition(bool_Inferior_2_Float[0]), bool_Inferior_2_Float[1], "bool_Inferior_2_Float")
        self.assertEqual(parser.parseCondition(bool_Inferior_Bool[0]), bool_Inferior_Bool[1], "bool_Inferior_Bool")
        self.assertEqual(parser.parseCondition(bool_Inferior_2_Bool[0]), bool_Inferior_2_Bool[1], "bool_Superior_2_Bool")

    def testSwitch(self):

        text_Switch_1: list = ["?{str; Jame::#0, Tony::#1, Marco::#2, _::#default}", "#0"]
        text_Switch_2: list = ["?{int/int; 56::#0, 36::#1, 32::#2, _::#default}", "#2"]
        text_Switch_3: list = ["?{float/float; 56.5::#0, 4.2::#1, 32.3::#2, _::#default}", "#1"]
        text_Switch_4: list = ["?{str/lower; azertY::#0, Azerty::#1, AzErTy::#2, _::#default}", "#default"]

        parser = TemplateStr(variableDict=varDict)

        self.assertEqual(parser.parseSwitch(text_Switch_1[0]), text_Switch_1[1], "text_Switch_1")
        self.assertEqual(parser.parseSwitch(text_Switch_2[0]), text_Switch_2[1], "text_Switch_2")
        self.assertEqual(parser.parseSwitch(text_Switch_3[0]), text_Switch_3[1], "text_Switch_3")
        self.assertEqual(parser.parseSwitch(text_Switch_4[0]), text_Switch_4[1], "text_Switch_4")

class TestHasMethode(unittest.TestCase):

    def testHasOne(self):

        text_Has_One_1: list = ["?{int/age; 56::#0, 36::#1, 32::#2, _::#default} and ?{int/age; 56::#0, 36::#1, 32::#2, _::#default}", True]
        text_Has_One_2: list = ["?{int/age; 56::#0, 36::#1, 32::#2, _::#default} and ${bool}", True]
        text_Has_One_3: list = ["@{uppercase ${var}} and ${name}", True]
        text_Has_One_4: list = ["text", False]
        text_Has_One_5: list = ["%{{bool}", False]

        parser = TemplateStr()

        self.assertEqual(parser.hasOne(text_Has_One_1[0]), text_Has_One_1[1], "text_Has_One_1")
        self.assertEqual(parser.hasOne(text_Has_One_2[0]), text_Has_One_2[1], "text_Has_One_2")
        self.assertEqual(parser.hasOne(text_Has_One_3[0]), text_Has_One_3[1], "text_Has_One_3")
        self.assertEqual(parser.hasOne(text_Has_One_4[0]), text_Has_One_4[1], "text_Has_One_4")
        self.assertEqual(parser.hasOne(text_Has_One_5[0]), text_Has_One_5[1], "text_Has_One_5")

    def testHasVariable(self):

        text_Has_Variable_1: list = ["${bool} and ${name}", True]
        text_Has_Variable_2: list = ["${bool} and @{uppercase lower}", True]
        text_Has_Variable_3: list = ["@{uppercaseFirst bool} and @{uppercase lower}", False]

        parser = TemplateStr()

        self.assertEqual(parser.hasVariable(text_Has_Variable_1[0]), text_Has_Variable_1[1], "text_Has_Variable_1")
        self.assertEqual(parser.hasVariable(text_Has_Variable_2[0]), text_Has_Variable_2[1], "text_Has_Variable_2")
        self.assertEqual(parser.hasVariable(text_Has_Variable_3[0]), text_Has_Variable_3[1], "text_Has_Variable_3")

    def testHasFunction(self):

        text_Has_Function_1: list = ["@{uppercase; lower} and @{uppercaseFirst; lower}", True]
        text_Has_Function_2: list = ["@{uppercase; lower} and #{'text' > 'text'; yes | no}", True]
        text_Has_Function_3: list = ["#{'text' > 'text'; yes | no} and #{'text' < 'text'; yes | no}", False]

        parser = TemplateStr()

        self.assertEqual(parser.hasFunction(text_Has_Function_1[0]), text_Has_Function_1[1], "text_Has_Function_1")
        self.assertEqual(parser.hasFunction(text_Has_Function_2[0]), text_Has_Function_2[1], "text_Has_Function_2")
        self.assertEqual(parser.hasFunction(text_Has_Function_3[0]), text_Has_Function_3[1], "text_Has_Function_3")

    def testHasCondition(self):

        text_Has_Condition_1: list = ["#{'text' > 'text'; yes | no} and #{'text' < 'text'; yes | no}", True]
        text_Has_Condition_2: list = ["#{'text' > 'text'; yes | no} and ?{int/age; 56::#0, 36::#1, 32::#2, _::#default}", True]
        text_Has_Condition_3: list = ["?{int/age; 56::#0, 36::#1, 32::#2, _::#default} and ?{int/age; 56::#0, 36::#1, 32::#2, _::#default}", False]

        parser = TemplateStr()

        self.assertEqual(parser.hasCondition(text_Has_Condition_1[0]), text_Has_Condition_1[1], "text_Has_Condition_1")
        self.assertEqual(parser.hasCondition(text_Has_Condition_2[0]), text_Has_Condition_2[1], "text_Has_Condition_2")
        self.assertEqual(parser.hasCondition(text_Has_Condition_3[0]), text_Has_Condition_3[1], "text_Has_Condition_3")

    def testHasSwitch(self):

        text_Has_Condition_1: list = ["?{int/age; 56::#0, 36::#1, 32::#2, _::#default} and ?{int/age; 56::#0, 36::#1, 32::#2, _::#default}", True]
        text_Has_Condition_2: list = ["?{int/age; 56::#0, 36::#1, 32::#2, _::#default} and ${bool}", True]
        text_Has_Condition_3: list = ["${bool} and ${name}", False]

        parser = TemplateStr()

        self.assertEqual(parser.hasSwitch(text_Has_Condition_1[0]), text_Has_Condition_1[1], "text_Has_Condition_1")
        self.assertEqual(parser.hasSwitch(text_Has_Condition_2[0]), text_Has_Condition_2[1], "text_Has_Condition_2")
        self.assertEqual(parser.hasSwitch(text_Has_Condition_3[0]), text_Has_Condition_3[1], "text_Has_Condition_3")



if __name__ == '__main__':
    print("\n----------------------------------------------------------------------\n")
    test_order = [
        "testAll",
        "testVariable", 
        "testInternFunction",
        "testCustomFunction",
        "testConditionEqual",
        "testConditionNoTEqual",
        "testConditionSuperiorEqual",
        "testConditionSuperior",
        "testConditionInferiorEqual",
        "testConditionInferior",
        "testSwitch",
        "testHasOne",
        "testHasVariable",
        "testHasFunction",
        "testHasCondition",
        "testHasSwitch",
    ]
    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = lambda x, y: test_order.index(x) - test_order.index(y)
    unittest.main(testLoader=loader, verbosity=2)
