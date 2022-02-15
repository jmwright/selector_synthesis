import pytest
from ..vector_based_synth import *

def test_synthesize():
    """
    Tests the top level synthesize function.
    """

    # Set the test data up for the Z axis
    selected_origins = [[0, 0, 10]]
    selected_normals = [[0, 0, 1]]
    face_origins = [[0, 0, 9], [0, 0, 8], [0, 0, 0], [0, 0, -7], [0, 0, -8], [0, 0, -9], [0, 10, 0]]
    face_normals = [[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 1, 0]]
    selected_meta = [{'is_planar': False}]
    face_meta = [{'is_planar': True}, {'is_planar': True}, {'is_planar': True}, {'is_planar': True}, {'is_planar': True}, {'is_planar': True}, {'is_planar': True}]


    # Test that a non-planar selected face is rejected
    selector_str = synthesize(selected_origins, selected_normals, face_origins, face_normals, selected_meta, face_meta)
    assert(selector_str == None)

def test_find_min_max_in_axis():
    """
    Tests the more raw form of min-max checking for an axis.
    """

    # Set the test data up for the Z axis
    min_selected_origin = [0, 0, -10]
    max_selected_origin = [0, 0, 10]
    indexed_min_selected_origin = [0, 0, -5]
    indexed_max_selected_origin = [0, 0, 5]
    selected_normal = [0, 0, 1]
    face_origins = [[0, 0, 9], [0, 0, 8], [0, 0, 0], [0, 0, -7], [0, 0, -8], [0, 0, -9], [0, 10, 0]]
    face_normals = [[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 1, 0]]
    face_meta = [{'is_planar': True}, {'is_planar': True}, {'is_planar': True}, {'is_planar': True}, {'is_planar': True}, {'is_planar': True}, {'is_planar': True}]
    axis_index = 2

    # Test a min, non-indexed selector
    (is_min, is_max, index) = find_min_max_in_axis(min_selected_origin, selected_normal, face_origins, face_normals, face_meta, axis_index)
    assert(is_min == True and is_max == False and index == -1)

    # Test a max, non-indexed selector
    (is_min, is_max, index) = find_min_max_in_axis(max_selected_origin, selected_normal, face_origins, face_normals, face_meta, axis_index)
    assert(is_min == False and is_max == True and index == -1)

    # Test an indexed min selector
    (is_min, is_max, index) = find_min_max_in_axis(indexed_min_selected_origin, selected_normal, face_origins, face_normals, face_meta, axis_index)
    assert(is_min == True and is_max == False and index == 3)

    # Test an indexed min selector on the other side of the origin
    (is_min, is_max, index) = find_min_max_in_axis(indexed_max_selected_origin, selected_normal, face_origins, face_normals, face_meta, axis_index)
    assert(is_min == True and is_max == False and index == 4)

    # Test a max selector in the Y axis
    (is_min, is_max, index) = find_min_max_in_axis([0, 11, 0], [0, 1, 0], face_origins, face_normals, face_meta, 1)
    assert(is_min == False and is_max == True and index == -1)

    # Test with multiple non-planar faces
    face_meta = [{'is_planar': False}, {'is_planar': True}, {'is_planar': True}, {'is_planar': False}, {'is_planar': True}, {'is_planar': True}, {'is_planar': True}]
    (is_min, is_max, index) = find_min_max_in_axis(indexed_min_selected_origin, selected_normal, face_origins, face_normals, face_meta, axis_index)
    assert(is_min == True and is_max == False and index == 2)


def test_synthesize_min_max_face():
    """
    Test the string synthesis of the min-max selector.
    """

    # Set the test data up for the Z axis
    min_selected_origin = [0, 0, -10]
    max_selected_origin = [0, 0, 10]
    indexed_min_selected_origin = [0, 0, -5]
    indexed_max_selected_origin = [0, 0, 5]
    selected_normal = [0, 0, 1]
    face_origins = [[0, 0, 9], [0, 0, 8], [0, 0, 0], [0, 0, -7], [0, 0, -8], [0, 0, -9], [0, 10, 0]]
    face_normals = [[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 1, 0]]
    face_meta = [{'is_planar': True}, {'is_planar': True}, {'is_planar': True}, {'is_planar': True}, {'is_planar': True}, {'is_planar': True}, {'is_planar': True}]

    # Test a min, non-indexed selector
    sel = synthesize_min_max_face_selector([min_selected_origin], [selected_normal], face_origins, face_normals, face_meta)
    assert(sel == '.faces("<Z")')

    # Test a max, non-indexed selector
    sel = synthesize_min_max_face_selector([max_selected_origin], [selected_normal], face_origins, face_normals, face_meta)
    assert(sel == '.faces(">Z")')

    # Test an indexed min selector
    sel = synthesize_min_max_face_selector([indexed_min_selected_origin], [selected_normal], face_origins, face_normals, face_meta)
    assert(sel == '.faces("<Z[3]")')

    # Test an indexed min selector on the other side of the origin
    sel = synthesize_min_max_face_selector([indexed_max_selected_origin], [selected_normal], face_origins, face_normals, face_meta)
    assert(sel == '.faces("<Z[4]")')

    # Test a max selector in a different axis
    sel = synthesize_min_max_face_selector([[0, 11, 0]], [[0, 1, 0]], face_origins, face_normals, face_meta)
    assert(sel == '.faces(">Y")')

    # Test an indexed face with non-planar other faces
    face_meta = [{'is_planar': False}, {'is_planar': True}, {'is_planar': True}, {'is_planar': False}, {'is_planar': True}, {'is_planar': True}, {'is_planar': True}]
    sel = synthesize_min_max_face_selector([indexed_min_selected_origin], [selected_normal], face_origins, face_normals, face_meta)
    assert(sel == '.faces("<Z[2]")')
