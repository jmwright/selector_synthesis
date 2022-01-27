import pytest
from ..vector_based_synth import *
from ..vector_common import *

def test_to_vector():
    """
    Tests the capability of converting tuples and lists
    to CadQuery Vectors.
    """

     # Test a tuple
    v1 = (1, 1, 0)
    v2 = to_vector(v1)
    assert(v2 == Vector(1, 1, 0))

    # Test a list
    v1 = [1, 1, 0]
    v2 = to_vector(v1)
    assert(v2 == Vector(1, 1, 0))

    # Test Vector
    v1 = Vector(1, 1, 0)
    v2 = to_vector(v1)
    assert(v2 == v1)


def test_are_vectors_parallel():
    """
    Tests the method that determines if two CadQuery Vectors
    are parallel.
    """

    # Test vectors that are parallel
    v1 = (1, 1, 0)
    v2 = (2, 2, 0)
    assert(are_vectors_parallel(v1, v2) == True)

    # Test vectors that are not parallel
    v1 = (1, 1, 0)
    v2 = (2, 5, 0)
    assert(are_vectors_parallel(v1, v2) == False)


def test_are_vectors_orthogonal():
    """
    Tests the method that determines if two CadQuery Vectors
    are orthogonal.
    """

    # Test vectors that are orthogonal
    v1 = (5, 5, 0)
    v2 = (-5, 5, 0)
    assert(are_vectors_orthogonal(v1, v2) == True)

    # Test vectors that are parallel instead of orthogonal
    v1 = (1, 1, 0)
    v2 = (2, 2, 0)
    assert(are_vectors_orthogonal(v1, v2) == False)

    # Test vectors that are neither orthogonal or parallel
    v1 = (1, 1, 0)
    v2 = (2, 5, 0)
    assert(are_vectors_orthogonal(v1, v2) == False)
