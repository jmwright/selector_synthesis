from .vector_common import *


def synthesize(
    selector_type, **kwargs
):
    """
    Handles the high level work of calling the correct type of synthesizer.
    """

    selector_str = None

    # See whether we have a face or edge selector
    if selector_type == "Face":
        # We handle a single selected face differently than multiple selected faces
        if (
            len(kwargs["selected_origin"]) == 1
            and kwargs["selected_meta"][0]["is_planar"]
        ):
            selector_str = synthesize_min_max_face_selector(
                kwargs
            )
    elif selector_type == "Edge":
        selector_str = synthesize_edge_selector(
            kwargs
        )

    return selector_str


def find_min_max_in_axis(
    selected_origin, selected_normal, face_origins, face_normals, face_meta, axis_index
):
    """
    Determines whether a face is a maximum or minimum in a given axis, including whether it is
    an indexed max or min.
    """
    is_max = None
    is_min = None
    dist_face_map = {}

    # Save the distance for the selected face
    dist_face_map[selected_origin[axis_index]] = "selected"

    # Step through all the faces and check for a max or min condition
    for i in range(0, len(face_origins)):
        # Check to make sure this face is planar
        if not face_meta[i]["is_planar"]:
            continue

        # Check if the selected and current face normals are aligned
        # if are_vectors_parallel(selected_normal, face_normals[i]):
        # Check to see if this distance has already been added
        if face_origins[i][axis_index] not in dist_face_map:
            dist_face_map[face_origins[i][axis_index]] = len(dist_face_map)

        # Check to see if the face is the maximum along the axis
        if selected_origin[axis_index] > face_origins[i][axis_index]:
            # Keep from overriding other faces that were already more maximal
            if is_max == None:
                is_max = True
        else:
            is_max = False

        # Check to see if the face is the minimum along the axis
        if selected_origin[axis_index] < face_origins[i][axis_index]:
            # Keep from overriding other faces that were already more minimal
            if is_min == None:
                is_min = True
        else:
            is_min = False

    # If the max and/or min are still None, then the face is not the max/min
    if is_max == None:
        is_max = False
    if is_min == None:
        is_min = False

    selected_index = None
    i = 0
    # Step through and look for the selected face in the stack of filtered faces
    for dist in sorted(dist_face_map):
        # The selected face should have the only value of type string
        if type(dist_face_map[dist]).__name__ == "str":
            selected_index = i

        i += 1

    # Handle the edge case where there are only two faces
    if len(dist_face_map) == 2:
        if selected_index == 0:
            is_min = True
        elif selected_index == len(dist_face_map) - 1:
            is_max = True

    # Cover the case of the index being a true max or min, in which case you do not need an index
    if selected_index == 0 or selected_index == len(dist_face_map) - 1:
        selected_index = None
    else:
        is_min = True

    # Because of the way CadQuery selector indexing works, we have to make the index negative
    if selected_index != None:
        # selected_index += 1
        selected_index = -selected_index

    return (is_min, is_max, selected_index)


def synthesize_min_max_face_selector(
    sel_data,
):
    """
    Synthesizes an indexed min/max selector given a list of face origins and normals.
    """

    selector_str = '.faces("|{axis} and {filter}{axis}{index}")'
    axis_index = -1
    axis_str = ""
    filter_str = ""
    index_str = ""

    # Assume there is ony one selected face, for now
    selected_origin = sel_data["selected_origin"][0]
    selected_normal = sel_data["selected_normal"][0]

    # Determine if a face's normal is aligned with any axis
    if is_parallel_to_axis(selected_normal, "X"):
        axis_str = "X"
        axis_index = 0
    elif is_parallel_to_axis(selected_normal, "Y"):
        axis_str = "Y"
        axis_index = 1
    elif is_parallel_to_axis(selected_normal, "Z"):
        axis_str = "Z"
        axis_index = 2

    # Check to see if the selected face is aligned with an axis
    if axis_index > -1:
        # See if the face is either the minimum or maximum in this axis
        (is_min, is_max, index) = find_min_max_in_axis(
            selected_origin,
            selected_normal,
            sel_data["face_origins"],
            sel_data["face_normals"],
            sel_data["face_meta"],
            axis_index,
        )

        # The max/min filter string
        if is_min == True:
            filter_str = "<"
        elif is_max == True:
            filter_str = ">"

        # Use the index, if there is one
        if index != None:
            index_str = "[" + str(index) + "]"

        # Format the selector string properly
        if axis_str != "" and filter_str != "":
            selector_str = selector_str.format(
                filter=filter_str, axis=axis_str, index=index_str
            )
        else:
            selector_str = None
    else:
        selector_str = None

    return selector_str


def synthesize_edge_selector(
    sel_data,
):
    """
    Synthesizes an edge selector string based on what edges were selected.
    """

    selector_str = '.edges("{filter}{axis}")'  # {index}")'
    axis_index = -1
    axis_str = ""
    filter_str = ""
    index_str = ""

    axis_str = None
    axis_filter = None
    # axis_index = None

    # Protect against there being no edges to check against
    if len(sel_data["selected_edges"]) == 0:
        return None

    # Find the vector of the edge
    edge_start = sel_data["selected_edge_starts"][0]
    edge_end = sel_data["selected_edge_ends"][0]
    edge_vector = tuple(map(lambda i, j: i - j, edge_end, edge_start))

    # TODO: Need to check if the types of all selected edges are the same
    if sel_data["selected_edge_types"][0] == "LINE":
        # Compare the vector of the line edge to see if it is parallel to an axis
        if is_parallel_to_axis(edge_vector, "X"):
            axis_str = "X"
            axis_filter = "|"
            # axis_index = 0
        elif is_parallel_to_axis(edge_vector, "Y"):
            axis_str = "Y"
            axis_filter = "|"
            # axis_index = 1
        elif is_parallel_to_axis(edge_vector, "Z"):
            axis_str = "Z"
            axis_filter = "|"
            # axis_index = 2
    if sel_data["selected_edge_types"][0] == "CIRCLE":
        # Compare the vector of the line edge to see if it is parallel to an axis
        if is_parallel_to_axis(selected_normals[0], "X"):
            axis_str = "X"
            axis_index = 0
        elif is_parallel_to_axis(selected_normals[0], "Y"):
            axis_str = "Y"
            axis_index = 1
        elif is_parallel_to_axis(selected_normals[0], "Z"):
            axis_str = "Z"
            axis_index = 2

        # find_min_max_in_axis(selected_origin, selected_normal, face_origins, face_normals, face_meta, axis_index)
        # (is_min, is_max, index) = find_min_max_in_axis(selected_edge_starts, selected_normals, other_edge_starts, other_normals, other_edge_meta, axis_index)

        #  # The max/min filter string
        # if is_min == True:
        #     filter_str = "<"
        # elif is_max == True:
        #     filter_str = ">"

        # # Use the index, if there is one
        # if index != None:
        #     index_str = "[" + str(index) + "]"

    # Format the selector string properly
    if axis_str != None and axis_filter != None:
        selector_str = selector_str.format(
            filter=axis_filter, axis=axis_str
        )  # , index = index_str)

    return selector_str
