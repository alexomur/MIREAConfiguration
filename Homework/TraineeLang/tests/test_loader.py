import unittest
from ..loader import Loader

# Assuming the Loader class and related code are already defined as per your latest version.

class TestLoader(unittest.TestCase):
    def test_full_language_features(self):
        # Test input that uses all features of the language
        test_input = '''
        (* This is a multi-line comment *)
        INT := 25
        STR := @"Hello, World!"
        SUMONE := !(10 5 +)
        SUMTWO := !(SUMONE 10 +)
        ORD := !(@"0" ord)
        ARRAY := { 1, 2, SUMONE }
        TABLE := table([
            NAMEONE = 25,
            NAMETWO = { 2, 3, 5 },
            NAMETHREE = @"test",
        ])
        '''
        expected_output = {
            'INT': 25,
            'STR': 'Hello, World!',
            'SUMONE': 15,
            'SUMTWO': 25,
            'ORD': 48,
            'ARRAY': [1, 2, 15],
            'TABLE': {
                'NAMEONE': 25,
                'NAMETWO': [2, 3, 5],
                'NAMETHREE': 'test'
            }
        }

        # Load the configuration using the Loader class
        struct = Loader.load_trainee(test_input)

        # Check if the output matches the expected output
        self.assertEqual(struct, expected_output)

    def test_invalid_syntax(self):
        # Test input with invalid syntax
        test_input = '''
        (* Missing closing parenthesis in expression *)
        BAD_EXPR := !(10 5 +
        (* Invalid variable name *)
        123INVALID := 50
        (* Missing assignment operator *)
        MISSING_OP 25
        (* Invalid table syntax *)
        BAD_TABLE := table([
            KEY = 10
            VALUE 20
        ])
        '''

        # Expecting a ValueError due to invalid syntax
        with self.assertRaises(ValueError):
            Loader.load_trainee(test_input)

# Run the unit tests
if __name__ == '__main__':
    unittest.main()
