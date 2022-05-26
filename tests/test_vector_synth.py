import pytest
from ..vector_based_synth import *


def test_synthesize_min_non_indexed_face():
    """
    Tests a minimum face selector on a simple box, with no need for an index.
    """

    # Model code:
    # result = cq.Workplane().box(10, 10, 10)

    # Face selector
    selector = '.faces("|Z and <Z")'

    # Set up the variables based on real world model data
    selected_origin = [(-6.93889390390723e-18, 6.66133814775094e-17, -5.0)]
    selected_normal = [(-0.0, -0.0, -1.0)]
    selected_meta = [{"is_planar": True}]
    face_origins = [
        (-5.0, 2.2204460492503135e-17, -6.93889390390723e-18),
        (5.0, 2.2204460492503135e-17, -6.93889390390723e-18),
        (6.66133814775094e-17, -5.0, -6.93889390390723e-18),
        (6.66133814775094e-17, 5.0, -6.93889390390723e-18),
        (-6.93889390390723e-18, 6.66133814775094e-17, 5.0),
    ]
    face_normals = [
        (-1.0, -0.0, 0.0),
        (1.0, 0.0, -0.0),
        (-0.0, -1.0, -0.0),
        (0.0, 1.0, 0.0),
        (-0.0, -0.0, -1.0),
    ]
    face_meta = [
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
    ]

    # Synthesize the selector
    sel = synthesize(
        "Face",
        selected_origin=selected_origin,
        selected_normal=selected_normal,
        selected_meta=selected_meta,
        face_origins=face_origins,
        face_normals=face_normals,
        face_meta=face_meta,
    )
    assert sel == selector


def test_synthesize_max_non_indexed_face():
    """
    Tests a maximum face selector on a simple box, with no need for an index.
    """

    # Model code:
    # result = cq.Workplane().box(10, 10, 10)

    # Face selector:
    selector = '.faces("|Z and >Z")'

    # Set up the variables based on real world model data
    selected_origin = [(-6.93889390390723e-18, 6.66133814775094e-17, 5.0)]
    selected_normal = [(0.0, 0.0, 1.0)]
    selected_meta = [{"is_planar": True}]
    face_origins = [
        (-5.0, 2.2204460492503135e-17, -6.93889390390723e-18),
        (5.0, 2.2204460492503135e-17, -6.93889390390723e-18),
        (6.66133814775094e-17, -5.0, -6.93889390390723e-18),
        (6.66133814775094e-17, 5.0, -6.93889390390723e-18),
        (-6.93889390390723e-18, 6.66133814775094e-17, -5.0),
    ]
    face_normals = [
        (-1.0, -0.0, 0.0),
        (1.0, 0.0, -0.0),
        (-0.0, -1.0, -0.0),
        (0.0, 1.0, 0.0),
        (-0.0, -0.0, -1.0),
    ]
    face_meta = [
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
    ]

    # Synthesize the selector
    sel = synthesize(
        "Face",
        selected_origin=selected_origin,
        selected_normal=selected_normal,
        selected_meta=selected_meta,
        face_origins=face_origins,
        face_normals=face_normals,
        face_meta=face_meta,
    )
    assert sel == selector


def test_synthesize_non_planar_indexed_faces():
    """
    Tests an index minimum face selector on a shape with overhanging non-planar faces.
    """

    # Model code:
    # result = cq.Workplane().box(10, 10, 3)
    # result = result.faces("<X").workplane().circle(2).extrude(1.0)

    # Face selector
    selector = '.faces("|Z and <Z[-1]")'

    # Set up the variables based on real world model data
    selected_origin = [(4.440892098500626e-16, -5.921189464667638e-17, -1.5)]
    selected_normal = [(-0.0, -0.0, -1.0)]
    selected_meta = [{"is_planar": True}]
    face_origins = [
        (-5.0, -3.3901604935095317, 2.971049450155019e-17),
        (4.440892098500626e-16, -5.921189464667638e-17, 1.5),
        (-5.499999999999999, 1.1102230246251565e-16, -7.752045533271358e-17),
        (-1.8503717077085943e-16, -5.0, 3.903127820947816e-17),
        (-5.0, 5.448710209752528e-15, 1.7023107363884669),
        (-5.0, 3.3901604935095357, 2.9190517248992612e-18),
        (-1.8503717077085943e-16, 5.0, 3.903127820947816e-17),
        (5.0, 1.8503717077085943e-16, 3.903127820947816e-17),
        (-5.0, -4.227085391736536e-17, -1.7023107363884666),
        (-6.000000000000001, -6.66133814775094e-16, -1.3877787807814452e-17),
    ]
    face_normals = [
        (-1.0, -0.0, 0.0),
        (0.0, 0.0, 1.0),
        (0.0, 2.0, 2.4492935982947064e-16),
        (-0.0, -1.0, -0.0),
        (1.0, 0.0, 0.0),
        (-1.0, -0.0, 0.0),
        (0.0, 1.0, 0.0),
        (1.0, 0.0, -0.0),
        (1.0, 0.0, 0.0),
        (-1.0, -0.0, -0.0),
    ]
    face_meta = [
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": False},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
    ]

    sel = synthesize(
        "Face",
        selected_origin=selected_origin,
        selected_normal=selected_normal,
        selected_meta=selected_meta,
        face_origins=face_origins,
        face_normals=face_normals,
        face_meta=face_meta,
    )
    assert sel == selector


def test_synthesize_cbore_hole_face():
    """
    Tests an indexed face selector to select the bottom of the counter-bore in a counter-bore hole.
    """

    # Model code:
    # result = cq.Workplane().box(10, 10, 10)
    # result = result.faces(">Z").workplane().cboreHole(diameter=2.4, cboreDiameter=4.4, cboreDepth=4.0)

    # Face selector
    selector = '.faces("|Z and <Z[-2]")'

    # Set up the variables based on real world model data
    selected_origin = [(-2.220446049250313e-16, -3.82705867764668e-16, 1.0)]
    selected_normal = [(-0.0, -0.0, 1.0)]
    selected_meta = [{"is_planar": True}]
    face_origins = [
        (-5.0, 2.2204460492503135e-17, -6.93889390390723e-18),
        (6.66133814775094e-17, -5.0, -6.93889390390723e-18),
        (3.3306690738754696e-16, -1.7578335871931255e-16, 5.0),
        (6.66133814775094e-17, 5.0, -6.93889390390723e-18),
        (3.0531133177191805e-16, 4.337603480800566e-17, -5.0),
        (5.0, 2.2204460492503135e-17, -6.93889390390723e-18),
        (0.0, -8.01285088296047e-17, 3.0),
        (0.0, -3.433916166612692e-17, -2.0),
    ]
    face_normals = [
        (-1.0, -0.0, 0.0),
        (-0.0, -1.0, -0.0),
        (0.0, 0.0, 1.0),
        (0.0, 1.0, 0.0),
        (-0.0, -0.0, -1.0),
        (1.0, 0.0, -0.0),
        (-2.2, -2.6942229581241775e-16, -0.0),
        (-1.2, -1.4695761589768238e-16, -0.0),
    ]
    face_meta = [
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": False},
        {"is_planar": False},
    ]

    sel = synthesize(
        "Face",
        selected_origin=selected_origin,
        selected_normal=selected_normal,
        selected_meta=selected_meta,
        face_origins=face_origins,
        face_normals=face_normals,
        face_meta=face_meta,
    )
    assert sel == selector


def test_synthesize_edge_selector():
    """
    Tests the ability to synthesize an edge selector given information about
    selected edge(s).
    """
    selected_edges = ["edge_1234"]
    selected_edge_types = ["LINE"]
    selected_edge_starts = [(5, -5, 5)]
    selected_edge_ends = [(5, 5, 5)]
    selected_edge_normals = [(0, 0, 1)]
    other_edge_starts = [()]
    other_edge_ends = [()]
    other_edge_meta = [{}]
    other_normals = [()]

    sel = synthesize(
        "Edge",
        selected_edges=selected_edges,
        selected_edge_types=selected_edge_types,
        selected_edge_starts=selected_edge_starts,
        selected_edge_ends=selected_edge_ends,
        selected_edge_normals=selected_edge_normals,
        other_edge_starts=other_edge_starts,
        other_edge_ends=other_edge_ends,
        other_edge_meta=other_edge_meta,
        other_normals=other_normals,
    )
    assert sel == '.edges("|Y")'

    # Test a circular edge
    # selected_edge_types = ["CIRCLE"]
    # selected_edge_starts = [(5, 5, 5)]
    # selected_edge_ends = [(5, 5, 5)]
    # selected_edge_normals = [(0, 0, 1)]

    # sel = synthesize_edge_selector(selected_edges, selected_edge_types, selected_edge_starts, selected_edge_ends, selected_edge_normals, other_edge_starts, other_edge_ends, other_edge_meta, other_normals)
    # assert(sel == '.edges(">Z")')


# Other potential face selector test cases

# Test an indexed min selector
# sel = synthesize_min_max_face_selector([indexed_min_selected_origin], [selected_normal], face_origins, face_normals, face_meta)
# assert(sel == '.faces("|Z and <Z[-4]")')

# Test an indexed min selector on the other side of the origin
# sel = synthesize_min_max_face_selector([indexed_max_selected_origin], [selected_normal], face_origins, face_normals, face_meta)
# assert(sel == '.faces("|Z and <Z[-5]")')

# Test a max selector in a different axis
# sel = synthesize_min_max_face_selector([[0, 11, 0]], [[0, 1, 0]], face_origins, face_normals, face_meta)
# assert(sel == '.faces("|Y and >Y")')

# Test an indexed face with non-planar other faces
# face_meta = [{'is_planar': False}, {'is_planar': True}, {'is_planar': True}, {'is_planar': False}, {'is_planar': True}, {'is_planar': True}, {'is_planar': True}]
# sel = synthesize_min_max_face_selector([indexed_min_selected_origin], [selected_normal], face_origins, face_normals, face_meta)
# assert(sel == '.faces("|Z and <Z[-3]")')
