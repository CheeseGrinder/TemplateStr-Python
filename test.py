import unittest
from tempStr import TemplateStr

print("\n-------------------------------- Test --------------------------------\n")

def testType(list:list) -> str:
    
    if type(list[0]) != str: raise TypeError
    if type(list[1]) != str: raise TypeError
    if type(list[2]) != str: raise TypeError
    if type(list[3]) != bool: raise TypeError
    if type(list[4]) != int: raise TypeError
    if type(list[5]) != float: raise TypeError
    if type(list[6]) != str: raise TypeError
    if type(list[7]) != str: raise TypeError

    return 'YES'

varDict: dict = {"varTest1":"hello", "varTest2":"Woww", "varTest3": 123, "varTest4": True, "varTest5": "oof"}

funcs: list = [testType]

parser = TemplateStr(functionList=funcs, variableDict=varDict)

textFull: str = "{{@testType 'E' \"E\" `E` <b:True> <n:123> <n:123.4> varTest3 varTest4}} sir, {{$varTest1}} {{#'oof' != varTest5: morning || good night }}"


class TestParseMethode(unittest.TestCase):

    def test_full(self):

        result: str = parser.parse(textFull)

        print(result)

        self.assertEqual(result, 'YES sir, hello good night')

if __name__ == '__main__':
    unittest.main(verbosity=2)
