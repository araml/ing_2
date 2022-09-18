# -*- coding: utf-8 -*-
import unittest

import cgi_decode
from cgi_decode import *

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


class test_evaluate_condition(unittest.TestCase):  
  
    def test_equal_operator_not_equal_values(self):
        distances_true, distances_false = clear_tests()
        lhs = 20
        rhs = 10

        v = evaluate_condition(1, operator.eq, lhs, rhs)
    
        self.assertFalse(v)
        self.assertEqual(distances_true[1], 10)
        self.assertEqual(distances_false[1], 0)

    def test_equal_operator_equal_values(self):
        distances_true, distances_false = clear_tests()
        lhs = 20

        v = evaluate_condition(1, operator.eq, lhs, lhs)
    
        self.assertTrue(v)
        self.assertEqual(distances_true[1], 0)
        self.assertEqual(distances_false[1], 1)

    def test_not_equal_operator_equal_values(self):
        distances_true, distances_false = clear_tests()
        lhs = 20

        v = evaluate_condition(1, operator.ne, lhs, lhs)
    
        self.assertFalse(v)
        self.assertEqual(distances_true[1], 1)
        self.assertEqual(distances_false[1], 0)

    def test_not_equal_operator_equal_values(self):
        distances_true, distances_false = clear_tests()
        lhs = 20
        rhs = 10

        v = evaluate_condition(1, operator.ne, lhs, rhs)
    
        self.assertTrue(v)
        self.assertEqual(distances_true[1], 0)
        self.assertEqual(distances_false[1], 10)

    def test_leq_equal_operator_lhs_less_than(self):
        distances_true, distances_false = clear_tests()
        lhs = 10
        rhs = 20

        v = evaluate_condition(1, operator.le, lhs, rhs)
    
        self.assertTrue(v)
        self.assertEqual(distances_true[1], 0)
        self.assertEqual(distances_false[1], 11)

    def test_leq_equal_operator_rhs_less_than(self):
        distances_true, distances_false = clear_tests()
        lhs = 20
        rhs = 10

        v = evaluate_condition(1, operator.le, lhs, rhs)
    
        self.assertFalse(v)
        self.assertEqual(distances_true[1], 10)
        self.assertEqual(distances_false[1], 0)

    def test_leq_equal_operator_lhs_equal_rhs(self):
        distances_true, distances_false = clear_tests()
        lhs = 20
        rhs = 20

        v = evaluate_condition(1, operator.le, lhs, rhs)
    
        self.assertTrue(v)
        self.assertEqual(distances_true[1], 0)
        self.assertEqual(distances_false[1], 1)

    def test_less_than_operator_lhs_less_than_rhs(self):
        distances_true, distances_false = clear_tests()
        lhs = 10
        rhs = 20

        v = evaluate_condition(1, operator.lt, lhs, rhs)
    
        self.assertTrue(v)
        self.assertEqual(distances_true[1], 0)
        self.assertEqual(distances_false[1], 10)

    def test_less_than_operator_rhs_less_than_lhs(self):
        distances_true, distances_false = clear_tests()
        lhs = 20
        rhs = 10

        v = evaluate_condition(1, operator.lt, lhs, rhs)
    
        self.assertFalse(v)
        self.assertEqual(distances_true[1], 11)
        self.assertEqual(distances_false[1], 0)

    def test_in_operator_lhs_in_list(self):
        distances_true, distances_false = clear_tests()
        lhs = 10
        rhs = [20, 30, 10]

        v = evaluate_condition(1, "in", lhs, rhs)
    
        self.assertTrue(v)
        self.assertEqual(distances_true[1], 0)
        self.assertEqual(distances_false[1], 1)

    def test_in_operator_empty_list(self):
        distances_true, distances_false = clear_tests()
        lhs = 10
        rhs = []

        v = evaluate_condition(1, "in", lhs, rhs)
    
        self.assertFalse(v)
        self.assertEqual(distances_true[1], sys.maxsize)
        self.assertEqual(distances_false[1], 0)

    def test_in_operator_not_in_list(self):
        distances_true, distances_false = clear_tests()
        lhs = 10
        rhs = [1, 2, 3]

        v = evaluate_condition(1, "in", lhs, rhs)
    
        self.assertFalse(v)
        self.assertEqual(distances_true[1], 7)
        self.assertEqual(distances_false[1], 0)

    def test_in_operator_not_in_list(self):
        distances_true, distances_false = clear_tests()
        lhs = 10
        rhs = [1, 2, 3, 9]

        v = evaluate_condition(1, "in", lhs, rhs)
    
        self.assertFalse(v)
        self.assertEqual(distances_true[1], 1)
        self.assertEqual(distances_false[1], 0)

    def test_in_operator_for_strings(self):
        distances_true, distances_false = clear_tests()
        lhs = 'a'
        rhs = ['b', 'c', 'd']

        v = evaluate_condition(4, "in", lhs, rhs)

        self.assertFalse(v)

class test_cgi_decode_instrumente(unittest.TestCase):  
    def test_decode_hello_reader(self):
        clear_tests()
        s = "Hello+Reader"

        s2 = cgi_decode_instrumented(s)
        distances_true = get_distances_true()
        distances_false = get_distances_false()
        self.assertEqual(s2, "Hello Reader")
        self.assertEqual(distances_true[1], 0)
        self.assertEqual(distances_true[2], 0)
        self.assertEqual(distances_true[3], 35)
        self.assertEqual(distances_false[2], 0)
        self.assertEqual(distances_false[3], 0)
        self.assertEqual(distances_false[3], 0)

class test_get_fitness_cgi_decode(unittest.TestCase):  
    def test_get_fitness_cgi_decode(self):
        clear_tests()
        
        v = get_fitness_cgi_decode("%AA")

        self.assertEqual(v, 0)

    def test_get_fitness_cgi_decode3(self):
        clear_tests()
        
        print("\n", get_fitness_cgi_decode("%AA"))
        print(get_distances_true(), "\n", 
              get_distances_false())
        

    def test_get_fitness_cgi_decode2(self):
        clear_tests()
        
        v = get_fitness_cgi_decode("Hello+Reader")

        self.assertEqual(v, 2.9722222222222223)

    def test_get_fitness_cgi_decode4(self):
        clear_tests()
        
        v = get_fitness_cgi_decode("")

        self.assertEqual(v, 4.5)

class test_create_population(unittest.TestCase):
    def test_population_length(self):
        pop = create_population(10, 1)
        
        self.assertEqual(len(pop), 10)

    def test_population_range(self):
        pop = create_population(10, 1)

        for i in pop:
            self.assertTrue(i <= 255)
            self.assertTrue(i >= 0)


class test_evaluate_population(unittest.TestCase):
    def test_population_value(self):
        population = ['']
        
        evaluated_population = evaluate_population(population)

        self.assertEqual(evaluated_population[''], 4.5)

class test_crossover(unittest.TestCase):
    def test_population_value(self):
        p1 = 'Hola'
        p2 = 'Mund'

        of1, of2, p = crossover(p1, p2)
        
        print(p, of1, of2)

        self.assertEqual(len(of1), len(p1))
        self.assertEqual(len(of2), len(p2))
        self.assertEqual(of1[0:p], p1[0:p])
        self.assertEqual(of1[p: ], p2[p: ])


if __name__ == '__main__':
    unittest.main()
