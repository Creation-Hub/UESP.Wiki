"""
Provides methods for formatting script data.
"""
from papyrus.code import Variable

class WikiDataScript:
    """
    Provides methods for formatting and retrieving script information.
    """

    @staticmethod
    def variable_to_string(variable:Variable) -> str:
        string_variable:str = f"{variable.type} {variable.name}"
        if variable.value:
            string_variable += f" = {variable.value}"
        return string_variable


    @staticmethod
    def variable_to_string_list(variables:list[Variable]) -> list[str]:
        string_variables:list[str] = []
        for variable in variables:
            string_variable:str = WikiDataScript.variable_to_string(variable)
            string_variables.append(string_variable)
        return string_variables
