REG_STR = r"\"(?P<str_double>[^\"]+)\"|\'(?P<str_single>[^\']+)\'|`(?P<str_back>[^`]+)`"
REG_BOOL = r"b/(?P<bool>[Tt]rue|[Ff]alse)"
REG_INT = r"i/(?P<int>[0-9_]+)"
REG_FLOAT = r"f/(?P<float>[0-9_.]+)"
REG_VAR = r'(?P<varName>[\w._-]+)(?:\[(?P<index>[\d]+)])?'
REG_LIST = r"\((?P<list>[^\(\)]+)\)"

REG_VARIABLE = r'(?P<match>\${'+REG_VAR+r'})'
REG_FUNCTION = r'(?P<match>@{(?P<functionName>[^{}\s]+)(?:; (?P<parameters>[^{}]+))?})'
REG_CONDITION = r'(?P<match>#{(?P<conditionValue1>[^{}]+) (?P<conditionSymbol>==|!=|<=|<|>=|>) (?P<conditionValue2>[^{}]+); (?P<trueValue>[^{}]+) \| (?P<falseValue>[^{}]+)})'
REG_SWITCH = r'(?P<match>\?{(?:(?P<type>str|int|float)/)?'+REG_VAR+r'; (?P<values>(?:[^{}]+::[^{}]+){2,}), _::(?P<defaultValue>[^{}]+)})'