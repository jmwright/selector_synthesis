import pytest
from ..vector_based_synth import *


def test_synthesize_min_non_indexed_face():
    """
    Tests a minimum face selector on a simple box, with no need for an index.
    """

    # Model code:
    # result = cq.Workplane().box(10, 10, 10)

    # Face selector
    selector = '.faces("|Z").faces("<Z")'

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
    selector = '.faces("|Z").faces(">Z")'

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
    selector = '.faces("|Z").faces("<Z")'

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
    selector = '.faces("|Z").faces("<Z[-2]")'

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


def test_synthesize_multiple_index_face():
    """
    Tests the capability of the face selector synthesizer when multiple indexes are involved
    in the same axis.
    """

    # Model code:
    # result=cq
    # result=result.Workplane("XY").workplane(offset=0.0,invert=False,centerOption="CenterOfBoundBox").tag("result")
    # result=result.rect(11.8,12.0,centered=True,forConstruction=False)
    # result=result.extrude(5.0,combine=True,clean=True,both=False,taper=0.0)
    # result=result.faces(">X").workplane(offset=0.0,invert=False,centerOption="CenterOfBoundBox")
    # result=result.circle(3.0,forConstruction=False)
    # result=result.extrude(3.2,combine=True,clean=True,both=False,taper=0.0)
    # result=result.faces("<X[-2]").workplane(offset=0.0,invert=False,centerOption="CenterOfBoundBox")
    # result=result.rect(9.0,5.0,centered=True,forConstruction=False)
    # result=result.extrude(1.0,combine=True,clean=True,both=False,taper=0.0)
    # result=result.faces("|Z and <Z[-1]").workplane(offset=0.0,invert=False,centerOption="CenterOfBoundBox")
    # result=result.pushPoints(peg_points)
    # result=result.circle(0.6,forConstruction=False)
    # result=result.extrude(1.0,combine=True,clean=True,both=False,taper=0.0)
    # result=result.faces("|Z and <Z[-2]").workplane(offset=0.0,invert=False,centerOption="CenterOfBoundBox")
    # result=result.moveTo(2.0,0.0)
    # result=result.rect(0.6,1.5,centered=True,forConstruction=False)
    # result=result.extrude(2.5,combine=True,clean=True,both=False,taper=0.0)

    # Face selector
    selector = '.faces("|Z").faces("<Z[-3]")'

    # Set up the variables based on real world data
    selected_origin = [
        (0.14202121960285652, 4.298502521281103e-15, 3.944304526105059e-31)
    ]
    selected_normal = [(-0.0, -0.0, -1.0)]
    selected_meta = [{"is_planar": True}]
    face_origins = [
        (-5.204170427930422e-17, -6.0, 2.5),
        (-5.9, -1.5612511283791264e-16, 2.5),
        (5.9, -5.2499999999999964, 2.5),
        (0.24696338802632134, 4.2029759075481164e-15, 5.0),
        (5.204170427930422e-17, 6.0, 2.5),
        (6.4, -4.499999999999992, 2.5),
        (5.9, 5.250000000000003, 2.5),
        (6.8999999999999995, -3.5131274823434557, 2.5),
        (6.4, 4.500000000000008, 2.5),
        (7.7681278311866855, 2.220446049250313e-16, 2.5),
        (6.899999999999999, 3.5131274823434633, 2.5),
        (5.900000000000001, 5.512058256888776e-15, -0.20150112782795665),
        (2.5, -5.0, -0.5),
        (5.0, -5.0, -0.5),
        (-2.5, 1.7798985664970367e-17, -0.5),
        (2.2, 1.951563910473908e-17, -1.25),
        (2.5, -0.75, -1.25),
        (2.8, -1.951563910473908e-17, -1.25),
        (2.5, 0.75, -1.25),
        (2.5, 5.0, -0.5),
        (5.0, 5.0, -0.5),
        (5.900000000000001, 2.1030255903816775e-16, 5.2015011278279575),
        (9.100000000000001, 0.0, 2.5),
        (2.5, -5.0, -1.0),
        (5.0, -5.0, -1.0),
        (-2.5, 1.9274705288631174e-17, -1.0),
        (2.5, 5.135813185032633e-33, -2.5),
        (2.5, 5.0, -1.0),
        (5.0, 5.0, -1.0),
    ]
    face_normals = [
        (0.0, -1.0, -0.0),
        (-1.0, -0.0, -0.0),
        (1.0, -0.0, -0.0),
        (0.0, 0.0, 1.0),
        (-0.0, 1.0, -0.0),
        (-0.0, -1.0, -0.0),
        (1.0, -0.0, -0.0),
        (1.0, 0.0, 0.0),
        (-0.0, 1.0, -0.0),
        (0.0, -3.0, 3.6739403974420594e-16),
        (1.0, 0.0, 0.0),
        (-1.0, -2.7369110631344083e-47, 7.304267640935298e-32),
        (-0.6, -7.347880794884119e-17, -0.0),
        (-0.6, -7.347880794884119e-17, -0.0),
        (-0.6, -7.347880794884119e-17, -0.0),
        (-1.0, -0.0, -0.0),
        (0.0, -1.0, -0.0),
        (1.0, -0.0, -0.0),
        (-0.0, 1.0, -0.0),
        (-0.6, -7.347880794884119e-17, -0.0),
        (-0.6, -7.347880794884119e-17, -0.0),
        (-1.0, -2.7369110631344083e-47, 7.304267640935298e-32),
        (1.0, 2.7369110631344083e-47, -7.304267640935298e-32),
        (-0.0, 0.0, -1.0),
        (-0.0, 0.0, -1.0),
        (-0.0, 0.0, -1.0),
        (-0.0, 0.0, -1.0),
        (-0.0, 0.0, -1.0),
        (-0.0, 0.0, -1.0),
    ]
    face_meta = [
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": False},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": False},
        {"is_planar": False},
        {"is_planar": False},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": True},
        {"is_planar": False},
        {"is_planar": False},
        {"is_planar": True},
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


def test_synthesize_circle_edge_selector():
    """
    Tests the ability to synthesize an edge selector given information about
    the selected circular edge.
    """

    # Test a circular edge
    selected_edges = ["edge_1234"]
    selected_edge_types = ["CIRCLE"]
    selected_edge_starts = [(5, 5, 5)]
    selected_edge_ends = [(5, 5, 5)]
    selected_edge_normals = [(0, 0, 1)]
    other_edge_starts = [(0, 0, 0), (0, 0, 1)]
    other_edge_ends = [(0, 0, 0), (0, 0, 1)]
    other_edge_meta = [{}]
    other_normals = [(0, 1, 0), (0, 0, 1)]

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
    assert sel == '.edges(">Z")'


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
