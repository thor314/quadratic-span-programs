import unittest
from sage.all import vector, Matrix
from typing import List, Tuple

VectorPair = Tuple[vector, vector]
VectorPairList = List[VectorPair]
VectorList = List[vector]

def evaluate_span_program(target_vector: vector, vector_pairs_list: VectorPairList, assignment: list[bool]) -> bool:
    """
    Evaluate a span program.
    Returns True if: the target_vector lies in the chosen vector_list iff 
    assignment: a list of length 2^n, where n is the number of vector pairs in vector_pairs_list. 
    """
    for i, assignment_val in enumerate(assignment):
        i_bits = [x == '1' for x in str(bin(i))[2:]] 
        i_bits += [False] * (len(vector_pairs_list) - len(i_bits))

        # print(i, "esf w/: ", i_bits, assignment_val)
        if evaluate_span_frame(target_vector, vector_pairs_list, i_bits) != assignment_val:
            return False
    return True

def evaluate_span_frame(target_vector: vector, vector_pairs_list: VectorPairList, vector_pairs_choices: list[bool]) -> bool:
    """
    Evaluates a span program frame.
    Returns:
    - True if the target vector can be expressed as a linear combination of vectors corresponding to assignment. False otherwise.
    """
    assigned_vectors = [vector_pairs_list[i][choice]
                        for i, choice in enumerate(vector_pairs_choices)]
    M = Matrix(assigned_vectors).transpose()

    try:
        solution = M.solve_right(target_vector)
        # print("in span: ", target_vector, assigned_vectors)
        return True
    except ValueError:
        # If no solution exists, then the target vector doesn't lie in the span
        # print("not in span: ", target_vector, assigned_vectors)
        return False

class Test(unittest.TestCase):
    target = vector([1, 0])
    vector_tuple_1 = (vector([0, 1]), vector([1, 1]))
    vector_tuple_2 = (vector([0, 1]), vector([1, -1]))
    literal_vectors = [vector_tuple_1, vector_tuple_2]

    def test_evaluate_span_frame(self):
        self.assertTrue(evaluate_span_frame(
            self.target, self.literal_vectors, [False, True]))
        self.assertFalse(evaluate_span_frame(
            self.target, self.literal_vectors, [False, False]))
    
    def test_evaluate_span_program(self):
        self.assertTrue(evaluate_span_program(
            self.target, self.literal_vectors, [False, True, True, True]))
        self.assertFalse(evaluate_span_program(
            self.target, self.literal_vectors, [False, True, True, False]))
