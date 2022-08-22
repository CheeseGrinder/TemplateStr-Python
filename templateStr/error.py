class Error(Exception):
    """Base class for other exceptions"""
    pass

class NotFoundFunctionError(Error):
    """Raised when not found function in list"""
    pass

class NotFoundVariableError(Error):
    """Raised when not found variable in dict"""
    pass

class NotAListError(Error):
    """Raised when value is not a list"""
    pass

class CustomFunctionReturnError(Error):
    """Raised when custom function dont return string"""
    pass

class BadComparatorError(Error):
    """Raised when not valide comparator is pass to parseCondition"""
    pass