import pytest
from vector_based_synth import *

def test_are_vectors_parallel():
    # Test tuples that are parallel
    v1 = (1, 1, 0)
    v2 = (2, 2, 0)
    assert(are_vectors_parallel(v1, v2) == True)

    # Test lists that are parallel
    v1 = [1, 1, 0]
    v2 = [2, 2, 0]
    assert(are_vectors_parallel(v1, v2) == True)

    # Test Vectors that are parallel
    v1 = Vector(1, 1, 0)
    v2 = Vector(2, 2, 0)
    assert(are_vectors_parallel(v1, v2) == True)

    # Test Vectors that are not parallel
    v1 = Vector(1, 1, 0)
    v2 = Vector(2, 5, 0)
    assert(are_vectors_parallel(v1, v2) == False)
