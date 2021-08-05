import unittest
from tempStr import TemplateStr

def testFunction(list:list) -> str:
    text = list[0]
    b = list[1]

    if b:
       text = text.replace(text, "YES")

    return text

varDict: dict = {"varTest1":"hello", "varTest2":"Wowwww", "varTest3":"UwU"}

funcs: list = [testFunction]

parser = TemplateStr(functionList=funcs, variableDict=varDict)

textFull: str = "{{@testFunction 'Euuuuu' <b:True>}} sir, {{$varTest1}} {{#ouf varTest2}} good morning {{else}} good night {{ouf#}}"


class TestParseMethode(unittest.TestCase):

    def test_full(self):

        result: str = parser.parse(textFull)

        self.assertEqual(result, 'YES sir, hello good night')

if __name__ == '__main__':
    unittest.main(verbosity=2)
