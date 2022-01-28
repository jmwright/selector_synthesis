import pytest
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


def test_is_parallel_to_axis():
    """
    Tests the wrapper method to check whether or not a given
    vector is parallel to an axis.
    """

    # Test parallel vector to X axis
    v1 = (2, 0, 0)
    res = is_parallel_to_axis(v1, 'x')
    assert(res == True)

    # Test parallel vector to Y axis
    v1 = (0, 2, 0)
    res = is_parallel_to_axis(v1, 'y')
    assert(res == True)

    # Test parallel vector to Z axis
    v1 = (0, 0, 2)
    res = is_parallel_to_axis(v1, 'z')
    assert(res == True)

    # Test not parallel to X axis
    v1 = (1, 0, 0)
    res = is_parallel_to_axis(v1, 'y')
    assert(res == False)

    # Test an axis that is not valid
    v1 = (1, 0, 0)
    with pytest.raises(Exception) as ex_info:
        res = is_parallel_to_axis(v1, 'c')
        assert(ex_info != None)