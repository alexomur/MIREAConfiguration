import os
from typing import Any
from pyparsing import (
    Word, alphas, nums, alphanums, Suppress, Literal, QuotedString,
    Forward, Group, ZeroOrMore, delimitedList, Optional, OneOrMore, restOfLine, Regex, ParserElement
)
import yaml
import operator

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

# static
class Loader:
    def __init__(self):
        raise Exception(f"Class {Loader.__name__} is a static class and cannot be instantiated")

    @staticmethod
    def load_trainee(trainee_text: str) -> Struct:
        """
        Translates text in trn (trainee) language into structure.
        :param trainee_text: Text in trn (trainee).
        :return: Structure filled with data from the read text.
        """
        # Enable packrat parsing for performance
        ParserElement.enablePackrat()

        # Comments
        multiline_comment = Suppress('(*') + ZeroOrMore(~Literal('*)') + Regex('.')) + Suppress('*)')
        comment = multiline_comment

        # Identifiers (Names): [A-Z]+
        identifier = Regex(r'[A-Z]+')

        # Numbers
        number = Regex(r'\d+').setParseAction(lambda t: int(t[0]))

        # Strings
        string = QuotedString('@\"', endQuoteChar='\"', escChar='\\').setParseAction(lambda t: t[0])

        # Forward declarations
        value = Forward()
        expression = Forward()

        # Arrays: { value, value, ... }
        array = Suppress('{') + Optional(delimitedList(value)) + Suppress('}')
        array.setParseAction(lambda t: list(t))

        # Dictionaries (Tables): table([ name = value, ... ])
        key_value = Group(identifier + Suppress('=') + value)
        table = Suppress('table([') + Optional(delimitedList(key_value)) + Suppress('])')
        table.setParseAction(lambda t: dict(t))

        # Constants dictionary for storing constant values
        constants = {}

        # Helper function to get value
        def get_constant_value(token):
            if token in constants:
                return constants[token]
            else:
                raise ValueError(f"Unknown constant '{token}'")

        # Expressions (Postfix notation)
        def parse_expression(tokens):
            return Loader.evaluate_expression(tokens, constants)

        const_expr = Suppress('!(') + OneOrMore(Regex(r'[^\s)]+')) + Suppress(')')
        const_expr.setParseAction(parse_expression)

        # Values can be number, string, array, table, const_expr, or identifier (constant)
        value <<= number | string | array | table | const_expr | identifier.setParseAction(lambda t: get_constant_value(t[0]))

        # Constant declaration: NAME := value
        def parse_const_decl(t):
            name = t[0]
            val = t[1]
            constants[name] = val

        const_decl = Group(identifier + Suppress(':=') + value)
        const_decl.setParseAction(parse_const_decl)

        # Statements
        statement = const_decl

        # The overall grammar
        grammar = ZeroOrMore(comment | statement)

        # Parse the input
        grammar.parseString(trainee_text, parseAll=True)

        # Build the structure
        return Struct(**constants)

    @staticmethod
    def evaluate_expression(tokens, constants):
        """
        Evaluate constant expression in postfix notation.
        Supports addition and ord() function.
        """
        stack = []

        # Operators and functions
        operators = {
            '+': operator.add,
        }

        functions = {
            'ord()': lambda x: ord(x) if isinstance(x, str) and len(x) == 1 else ValueError("ord() expects a single character"),
        }

        for token in tokens:
            if token in operators:
                b = stack.pop()
                a = stack.pop()
                result = operators[token](a, b)
                stack.append(result)
            elif token in functions:
                a = stack.pop()
                result = functions[token](a)
                stack.append(result)
            else:
                if token.isdigit():
                    stack.append(int(token))
                elif token.startswith('@\"') and token.endswith('\"'):
                    stack.append(token[2:-1])  # Remove @" and "
                elif token in constants:
                    stack.append(constants[token])
                else:
                    raise ValueError(f"Unknown token '{token}' in expression")

        if len(stack) != 1:
            raise ValueError("Invalid expression")
        return stack[0]

    @staticmethod
    def get_yaml(struct: Any) -> str:
        """
        Translates any type of object with any fields to yaml
        :param struct: Object to save
        :return: Configuration in yaml
        """
        return yaml.dump(struct.__dict__, allow_unicode=True)

if __name__ == "__main__":
    # Path to the test.trn file in the tests folder
    test_file_path = os.path.join('tests', 'test.trn')

    try:
        # Read the content of the test.trn file
        with open(test_file_path, 'r', encoding='utf-8') as file:
            trainee_text = file.read()

        # Load the configuration using the Loader class
        struct = Loader.load_trainee(trainee_text)

        # Convert the structure to YAML format
        yaml_output = Loader.get_yaml(struct)

        # Print the YAML output to the console
        print(yaml_output)
    except FileNotFoundError:
        print(f"File '{test_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
