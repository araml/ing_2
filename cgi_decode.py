import sys
import operator
from typing import Dict, Tuple
from random import seed, randint

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

distances_true: Dict[int, int] = {}
distances_false: Dict[int, int] = {}

def get_distances_true(): 
    return distances_true

def get_distances_false(): 
    return distances_false

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
    if (type(rhs) is list or type(rhs) is dict): 
        if (lhs in rhs):
            update_maps(condition_num, 0, 1)
            return True
        elif rhs == []:
            update_maps(condition_num, sys.maxsize, 0)
        else:
            distance = sys.maxsize
            for e in rhs:
                l = lhs
                r = e
                if (type(lhs) is str):
                    l = ord(lhs)
                    r = ord(e)
                distance = min(distance, max(r - l, l - r))
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
    return (distances_true, distances_false)
        
def cgi_decode_instrumented(s):
    """Decode the CGI-encoded string 's':
       * replace "+" by " "
       * replace "%xx" by the character with hex number xx.
       Return the decoded string. Raise `ValueError` for invalid inputs. """
    
    global distances_true, distances_false 
    distances_true = { 1: sys.maxsize, 2: sys.maxsize, 3: sys.maxsize, 
                       4: sys.maxsize, 5: sys.maxsize }
    distances_false = { 1: sys.maxsize, 2: sys.maxsize, 3: sys.maxsize, 
                       4: sys.maxsize, 5: sys.maxsize }

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
            t += c
        i += 1
    return t

def normalize(v: int) -> int:
    return v / (v + 1)

def get_fitness_cgi_decode(input_string: str) -> float:
    global distances_true, distances_false
    cgi_decode_instrumented(input_string)

    return (normalize(distances_true[1])  + 
            normalize(distances_false[2]) + 
            normalize(distances_true[3])  +
            normalize(distances_true[4])  +
            normalize(distances_true[5]))

def create_population(population_size: int, _seed: int) -> list:
    population = []
    seed(_seed)
    for i in range(population_size):
        population.append(randint(0, 255))

    return population


# Debo limpiar las distancias? 
def evaluate_population(population: list) -> Dict[int, int]:
    evaluated_population: Dict[int, int] = {}

    for p in population:
        v = get_fitness_cgi_decode(p)
        evaluated_population[p] = v
    
    return evaluated_population

def crossover(p1: str, p2: str) -> Tuple[str, str, int]:
    point = randint(0, len(p1))
    
    of1 = p1[0: point] + p2[point:]
    of2 = p2[0: point] + p1[point:]
        
    return (of1, of2, point)
