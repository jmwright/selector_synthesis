"""
This script is not yet used (and is probably broken). In the original repo, this was used to 
track intermediary CQ objects, so as to synthesize at the relevant line number.
"""

from inspect import currentframe
from collections import OrderedDict
import decision_tree_comparator
import cadquery.cq



class TrackedObjects(object):
    """
    This is the actual object(s) tracked.
    It reflects CAD object(s) at a certain time step.
    Note: Some operations may not create actual objects, but have 'pending' wires/edges
    """

    def __init__(self, objs):
        self.object_desc = []

        if len(objs.ctx.pendingWires) == 0 and len(objs.ctx.pendingEdges) == 0:
            # No wires pending: an actual object
            self.pending = False
            print("This line has", len(objs.objects), " objects in stack.")
            # For each child object
            for child_obj in objs.objects:
                tracked_entry = TrackedObject(obj=child_obj)
                self.object_desc.append(tracked_entry)

        else:
            self.pending = True
            print("There are", len(objs.ctx.pendingWires), "pending wires")
            print("There are", len(objs.ctx.pendingEdges), "pending edges")
        print("----------")

    def merge_with(self, other):
        """
        Merges two "TrackedObjects".
        This may be useful for loops where different tracked objects come from the same line of code
        :param other: the other object
        self is merged with "other""
        """
        # TODO: The merge is not proper
        self.object_desc = self.object_desc + other.object_desc

class TrackedObject(object):
    def __init__(self, obj):
        """
        Takes a CAD obj as parameter and generates edge, face lists and aggregates
        :param obj: individual CAD object0
        :return:
        """
        self.edges = []
        self.faces = []
        self.vertices = []

        # Save a reference to the CQ object
        self.obj = cadquery.CQ(obj)
        edges_obj = obj.Edges()
        # List of edges
        for edge_obj in edges_obj:
            self.edges.append(edge_obj)
        print("Edges:", len(self.edges))
        faces_obj = obj.Faces()
        # List of faces
        for face_obj in faces_obj:
            self.faces.append(face_obj)
        print("Faces:", len(self.faces))
        vertices_obj = obj.Vertices()
        # List of faces
        for vertex_obj in vertices_obj:
            self.vertices.append(vertex_obj)
        print("Vertices:", len(self.vertices))
        # Create aggregated dictionary until this line
        # self.obj_aggregate = shape_analyzer.Aggregates(self.obj, verbose=False)


class TrackedIDs(object):
    def __init__(self, obj_id, src_ids):
        """
        Sets up the dictionary val by storing the corresponding obj and src identifiers
        :param obj_id:
        :param src_ids: list of source objs
        """
        self.obj_id = obj_id
        self.src_ids = src_ids


class Tracker(object):
    """
    This class analyzes a shape and maintains changes over time.
    The hope is to use this history later for pinpointing where
    changes happened.
    """

    def __init__(self):
        self.track = OrderedDict()
        self.track_id = OrderedDict()

    def add_change(self, line_num, obj, obj_id="_PRIM_", src_ids=["_PRIM_"]):
        """
        This function is used for adding things to the tracking list
        :param obj: the object created by cadquery
        :param line_num: unique id for entry, typically line number
        :param obj_id: identifier of object created
        :param src_ids: list of objects used to make obj
        :return:
        """
        #TODO: It is difficult to get the variable identifier in Python

        # Check if the line_num already exists in the the dict
        if line_num not in self.track:
            print("Creating tracked object entry for line", line_num)
            self.track[line_num] = TrackedObjects(obj)
        else:
            print("Merging tracked object entry for line", line_num)
            self.track[line_num].merge_with(TrackedObjects(obj))

        # Add reference ids to track single dependencies
        # There is no merge for this as there appears to be no use case for this
        # TODO: Are there cases in which a merge is meaningful for this?
        assert isinstance(src_ids, list)
        self.track_id[line_num] = TrackedIDs(obj_id, src_ids)

def get_line_num():
    """
    Helper function to get line number in the main script
    :return: line number from where the function was called
    """
    cf = currentframe()
    return cf.f_back.f_lineno


def get_objects_at_line(track, line_num):
    """
    Returns a list of objects
    :param track: A TrackedObjects object
    :param line_num: line number
    :return: List of CQ objects at that line number
    """
    cq_objects = []
    for obj in track[line_num].object_desc:
        cq_objects.append(obj.obj)
    return cq_objects


def get_index_edge_in_objects(tracked_objects, edge):
    """

    :param tracked_objects: object of type TrackedObjects
    :param edge: the edge reference to be found
    :return: the index of list_cq_objects where edge exists, if not found, return -1
    """
    for i in range(len(tracked_objects.object_desc)):
        # For each individual object at that line number
        for obj_ind_edge in tracked_objects.object_desc[i].edges:
            # For each edge in the object, make comparisons until found
            if decision_tree_comparator.decision_tree_comparator.compare_shape(edge, obj_ind_edge):
                return i
    return -1


def CreateCQWith(cq_obj, obj_hashes_set, shape_type):
    """
    Create a new CQ object on which cq selectors can be applied which only includes shapes specified in obj_hashes
    :param cq_obj:
    :param obj_hashes_set:
    :param shape_type: The shape to expect in the obj_hashes
    :return: the cadquery object
    """

    list_new = []
    new_obj = cadquery.CQ(cq_obj)
    temp = cq_obj.objects

    if shape_type == "Edge":
        for tempObj in temp:
            for edge in tempObj.Edges():
                if decision_tree_comparator.decision_tree_comparator.shape_in_hash_set(shape=edge, obj_hash_set=obj_hashes_set):
                    list_new.append(edge)

    elif shape_type == "Face":
        for tempObj in temp:
            for face in tempObj.Faces():
                if decision_tree_comparator.decision_tree_comparator.shape_in_hash_set(shape=face, obj_hash_set=obj_hashes_set):
                    list_new.append(face)

    elif shape_type == "Vertex":
        for tempObj in temp:
            for vertex in tempObj.Vertices():
                if decision_tree_comparator.decision_tree_comparator.shape_in_hash_set(shape=vertex, obj_hash_set=obj_hashes_set):
                    list_new.append(vertex)

    else:
        print("CreateCQWith(): Unrecognized shape")

    return new_obj.newObject(objlist=list_new)


def get_shape_list_from_hash(cq_objs, hash_list, shape_type):
    """
    :param cq_objs: the cadquery object to be checked
    :param hash_list: the hashed shapes
    :param shape_type:
    :return: List of shapes in the hash list
    """
    shapes_obj = None
    targets_shapes = []
    for cq_obj in cq_objs.objects:
        if shape_type == "Face":
            shapes_obj = cq_obj.Faces()
        elif shape_type == "Edge":
            shapes_obj = cq_obj.Edges()
        elif shape_type == "Vertex":
            shapes_obj = cq_obj.Vertices()
        else:
            print("get_shape_list_from_hash(): Unknown shape type")
            continue
        for shape in shapes_obj:
            if decision_tree_comparator.decision_tree_comparator.shape_in_hash_set(shape, set(hash_list)):
                targets_shapes.append(shape)

    return targets_shapes


class Aggregates(object):
    """
    This class holds lists of special aggregated edges and faces in the structure
    """
    def __init__(self, obj, verbose=False, selectors=[">Z", ">Y", ">X", "<Z", "<Y", "<X", "|Z", "|Y", "|X", "#Z", "#Y",
                                                      "#X", "+Z", "+Y", "+X", "-Z", "-Y", "-X"], shape_type=None):
        """
        Initializes the special lists in self.edges dictionary.
        The corresponding edge hashes go to self.edges_hash dictionary.
        :param obj: the object created by cadquery
        :param shape_type: "Edge", "Face" or Vertex; aggregates are accordingly calculated
        """
        # Init empty dictionaries
        self.edges = dict()
        self.edges_hash = dict()
        self.faces = dict()
        self.faces_hash = dict()
        self.vertices = dict()
        self.vertices_hash = dict()

        # Shape based selectors are hereby included
        edge_shapes = ["%LINE", "%CIRCLE", "%ARC"]
        face_shapes = ["%PLANE", "%CYLINDER", "%SPHERE"]

        if shape_type is None:
            # Iterate over all selectors
            for sel in selectors:
                try:
                    # Edges
                    temp = obj.edges(sel).objects
                    edge_list = []
                    for tempObj in temp:
                        for edge in tempObj.Edges():
                            edge_list.append(edge)
                    if verbose:
                        print("-----------")
                        print("Printing", sel, "edges...", edge_list)
                    self.edges[sel] = edge_list
                    self.edges_hash[sel] = decision_tree_comparator.decision_tree_comparator.get_list_hash(orig_list=edge_list)
                except IndexError:
                    print("No edges in selector", sel)

                try:
                    # Faces
                    temp = obj.faces(sel).objects
                    face_list = []
                    for tempObj in temp:
                        for face in tempObj.Faces():
                            face_list.append(face)
                    if verbose:
                        print("-----------")
                        print("Printing", sel, "faces...", face_list)
                    self.faces[sel] = face_list
                    self.faces_hash[sel] = decision_tree_comparator.decision_tree_comparator.get_list_hash(orig_list=face_list)
                except IndexError:
                    print("No faces in selector", sel)

                try:
                    # Vertices
                    temp = obj.vertices(sel).objects
                    vertex_list = []
                    for tempObj in temp:
                        for vertex in tempObj.Vertices():
                            vertex_list.append(vertex)
                    if verbose:
                        print("-----------")
                        print("Printing", sel, "vertices...", vertex_list)
                    self.vertices[sel] = vertex_list
                    self.vertices_hash[sel] = decision_tree_comparator.decision_tree_comparator.get_list_hash(orig_list=vertex_list)
                except IndexError:
                    print("No vertices in selector", sel)

        elif shape_type == "Edge":
            selectors = selectors + edge_shapes
            for sel in selectors:
                try:
                    # Edges
                    temp = obj.edges(sel).objects
                    edge_list = []
                    for tempObj in temp:
                        for edge in tempObj.Edges():
                            edge_list.append(edge)
                    if verbose:
                        print("-----------")
                        print("Printing", sel, "edges...", edge_list)
                    self.edges[sel] = edge_list
                    self.edges_hash[sel] = decision_tree_comparator.decision_tree_comparator.get_list_hash(orig_list=edge_list)
                except IndexError:
                    print("No edges in selector", sel)

        elif shape_type == "Face":
            selectors = selectors + face_shapes
            for sel in selectors:
                try:
                    temp = obj.faces(sel).objects
                    face_list = []
                    for tempObj in temp:
                        for face in tempObj.Faces():
                            face_list.append(face)
                    if verbose:
                        print("-----------")
                        print("Printing", sel, "faces...", face_list)
                    self.faces[sel] = face_list
                    self.faces_hash[sel] = decision_tree_comparator.decision_tree_comparator.get_list_hash(orig_list=face_list)
                except IndexError:
                    print("No faces in selector", sel)

        elif shape_type == "Vertex":
            for sel in selectors:
                # Vertices
                try:
                    temp = obj.vertices(sel).objects
                    vertex_list = []
                    for tempObj in temp:
                        for vertex in tempObj.Vertices():
                            vertex_list.append(vertex)
                    if verbose:
                        print("-----------")
                        print("Printing", sel, "vertices...", vertex_list)
                    self.vertices[sel] = vertex_list
                    self.vertices_hash[sel] = decision_tree_comparator.decision_tree_comparator.get_list_hash(orig_list=vertex_list)
                except IndexError:
                    print("No vertices in selector", sel)
