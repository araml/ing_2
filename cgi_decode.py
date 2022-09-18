import sys
import unittest
import operator

def cgi_decode(s):
    """Decode the CGI-encoded string 's':
       * replace "+" by " "
       * replace "%xx" by the character with hex number xx.
       Return the decoded string. Raise `ValueError` for invalid inputs. """

    # Mapping of hex digits to their integer values
    hex_values = { 
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, 
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
        'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15,
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15
    }

    t = ""
    i = 0
    while (i < len(s)): # C1
        c = s[i]
        if c == '+': # C2
            t += ' ' 
        elif c == '%': # C3
            digit_high, digit_low = s[i + 1], s[i + 2]
            i += 2
            if digit_high in hex_values and digit_low in hex_values: #C4 and C5
                v = hex_values[digit_high] * 16 + hex_values[digit_low]
                t += chr(v)
            else: 
                raise ValueError("Invalid encoding")
        else:
            t += c
        i += 1
    return t

class test_cgi_decode(unittest.TestCase):
    def test_identity(self):
        s1 = "abcd"

        s2 = cgi_decode(s1)

        self.assertEqual(s1, s2)


    def test_plus(self):
        s1 = "a+b"

        s2 = cgi_decode(s1)
        
        self.assertEqual(s2, "a b")

    def test_hex(self):
        s1 = "%AE"

        s2 = cgi_decode(s1)

        self.assertEqual(s2, '®')

    def test_raise_error_empty_hex(self):
        with self.assertRaises(IndexError):
            cgi_decode("%")

    def test_raise_error_invalid_low_byte_of_hex(self):
        with self.assertRaises(ValueError):
            cgi_decode("%AT")
    
    def test_raise_error_invalid_high_byte_of_hex(self):
        with self.assertRaises(ValueError):
            cgi_decode("%TA")


from typing import Dict
distances_true: Dict[int, int] = {}
distances_false: Dict[int, int] = {}

def update_maps(condition_num, d_true, d_false):
    global distances_true, distances_false

    if condition_num in distances_true.keys():
        distances_true[condition_num] = min(distances_true[condition_num], d_true)
    else:
        distances_true[condition_num] = d_true

    if condition_num in distances_false.keys():
        distances_false[condition_num] = min(distances_false[condition_num], d_false)
    else:
        distances_false[condition_num] = d_false

# Checkear si es string y si lo es aplicar ord() para comparar enteros
def evaluate_condition(condition_num, op, lhs, rhs):
    if (type(rhs) is list): 
        if (lhs in rhs):
            update_maps(condition_num, 0, 1)
            return True
        elif rhs == []:
            update_maps(condition_num, sys.maxsize, 0)
        else:
            distance = sys.maxsize
            for e in rhs:
               distance = min(distance, max(e - lhs, lhs - e))
            update_maps(condition_num, distance, 0)
        return False
    else:
        distance = max(lhs - rhs, rhs - lhs)
        if op(lhs, rhs):
            if ((lhs <= rhs and op(lhs + distance, rhs)) or
               (rhs <= lhs and op(lhs, rhs + distance))): 
                update_maps(condition_num, 0, distance + 1)
            else:
                update_maps(condition_num, 0, distance)
            return True
        else:
            if ((lhs <= rhs and not op(lhs + distance, rhs)) or
               (rhs <= lhs and not op(lhs, rhs + distance))): 
                update_maps(condition_num, distance + 1, 0)
            else:
                update_maps(condition_num, distance, 0)
            return False

def clear_tests():
    global distances_true, distances_false
    distances_true = {}
    distances_false = {}

# TODO(agregar test con strings)
class test_evaluate_condition(unittest.TestCase):  
    def test_equal_operator_not_equal_values(self):
        clear_tests()
        lhs = 20
        rhs = 10

        v = evaluate_condition(1, operator.eq, lhs, rhs)
    
        self.assertFalse(v)
        self.assertEqual(distances_true[1], 10)
        self.assertEqual(distances_false[1], 0)

    def test_equal_operator_equal_values(self):
        clear_tests()
        lhs = 20

        v = evaluate_condition(1, operator.eq, lhs, lhs)
    
        self.assertTrue(v)
        self.assertEqual(distances_true[1], 0)
        self.assertEqual(distances_false[1], 1)

    def test_not_equal_operator_equal_values(self):
        clear_tests()
        lhs = 20

        v = evaluate_condition(1, operator.ne, lhs, lhs)
    
        self.assertFalse(v)
        self.assertEqual(distances_true[1], 1)
        self.assertEqual(distances_false[1], 0)

    def test_not_equal_operator_equal_values(self):
        clear_tests()
        lhs = 20
        rhs = 10

        v = evaluate_condition(1, operator.ne, lhs, rhs)
    
        self.assertTrue(v)
        self.assertEqual(distances_true[1], 0)
        self.assertEqual(distances_false[1], 10)

    def test_leq_equal_operator_lhs_less_than(self):
        clear_tests()
        lhs = 10
        rhs = 20

        v = evaluate_condition(1, operator.le, lhs, rhs)
    
        self.assertTrue(v)
        self.assertEqual(distances_true[1], 0)
        self.assertEqual(distances_false[1], 11)

    def test_leq_equal_operator_rhs_less_than(self):
        clear_tests()
        lhs = 20
        rhs = 10

        v = evaluate_condition(1, operator.le, lhs, rhs)
    
        self.assertFalse(v)
        self.assertEqual(distances_true[1], 10)
        self.assertEqual(distances_false[1], 0)

    def test_leq_equal_operator_lhs_equal_rhs(self):
        clear_tests()
        lhs = 20
        rhs = 20

        v = evaluate_condition(1, operator.le, lhs, rhs)
    
        self.assertTrue(v)
        self.assertEqual(distances_true[1], 0)
        self.assertEqual(distances_false[1], 1)

    def test_less_than_operator_lhs_less_than_rhs(self):
        clear_tests()
        lhs = 10
        rhs = 20

        v = evaluate_condition(1, operator.lt, lhs, rhs)
    
        self.assertTrue(v)
        self.assertEqual(distances_true[1], 0)
        self.assertEqual(distances_false[1], 10)

    def test_less_than_operator_rhs_less_than_lhs(self):
        clear_tests()
        lhs = 20
        rhs = 10

        v = evaluate_condition(1, operator.lt, lhs, rhs)
    
        self.assertFalse(v)
        self.assertEqual(distances_true[1], 11)
        self.assertEqual(distances_false[1], 0)

    def test_in_operator_lhs_in_list(self):
        clear_tests()
        lhs = 10
        rhs = [20, 30, 10]

        v = evaluate_condition(1, "in", lhs, rhs)
    
        self.assertTrue(v)
        self.assertEqual(distances_true[1], 0)
        self.assertEqual(distances_false[1], 1)

    def test_in_operator_empty_list(self):
        clear_tests()
        lhs = 10
        rhs = []

        v = evaluate_condition(1, "in", lhs, rhs)
    
        self.assertFalse(False)
        self.assertEqual(distances_true[1], sys.maxsize)
        self.assertEqual(distances_false[1], 0)

    def test_in_operator_not_in_list(self):
        clear_tests()
        lhs = 10
        rhs = [1, 2, 3]

        v = evaluate_condition(1, "in", lhs, rhs)
    
        self.assertFalse(False)
        self.assertEqual(distances_true[1], 7)
        self.assertEqual(distances_false[1], 0)

    def test_in_operator_not_in_list(self):
        clear_tests()
        lhs = 10
        rhs = [1, 2, 3, 9]

        v = evaluate_condition(1, "in", lhs, rhs)
    
        self.assertFalse(False)
        self.assertEqual(distances_true[1], 1)
        self.assertEqual(distances_false[1], 0)
        
def cgi_decode_instrumented(s):
    """Decode the CGI-encoded string 's':
       * replace "+" by " "
       * replace "%xx" by the character with hex number xx.
       Return the decoded string. Raise `ValueError` for invalid inputs. """

    # Mapping of hex digits to their integer values
    hex_values = { 
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, 
        '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
        'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15,
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15
    }

    t = ""
    i = 0
    while (evaluate_condition(1, operator.lt, i, len(s))): # C1
        c = s[i]
        if evaluate_condition(2, operator.eq, ord(c), ord('+')): # C2
            t += ' ' 
        elif evaluate_condition(3, operator.eq, ord(c), ord('%')): # C3
            digit_high, digit_low = s[i + 1], s[i + 2]
            i += 2
            if (evaluate_condition(4, "in", digit_high, hex_values) and
                evaluate_condition(5, "in", digit_low, hex_values)): #C4 and C5
                v = hex_values[digit_high] * 16 + hex_values[digit_low]
                t += chr(v)
            else: 
                raise ValueError("Invalid encoding")
        else:
            t += c
        i += 1
    return t

class test_cgi_decode_instrumente(unittest.TestCase):  
    def test_decode_hello_reader(self):
        clear_tests()
        s = "Hello+Reader"

        s2 = cgi_decode_instrumented(s)
    
        self.assertEqual(s2, "Hello Reader")
        self.assertEqual(distances_true[1], 0)
        self.assertEqual(distances_true[2], 0)
        self.assertEqual(distances_true[3], 35)
        self.assertEqual(distances_false[2], 0)
        self.assertEqual(distances_false[3], 0)
        self.assertEqual(distances_false[3], 0)


if __name__ == '__main__':
    unittest.main()
