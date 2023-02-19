"""
Broken, and not used.
"""

import itertools


class Comparator(object):
    """
    This class compares edges in the free cad world
    and the cad query world
    """

    def __init__(self, verbose=True):
        self.verbose = verbose

    @classmethod
    def compare_shape(cls, obj1, obj2):
        """
        :param obj1: object 1 to be compared
        :param obj2: object 2 to be compared
        :return: whether object 1 and 2 are the same or not

        Check is done separately for edges and faces.
        """
        if obj1.ShapeType() == "Edge":
            if obj1.startPoint() == obj2.startPoint() and obj1.endPoint() == obj2.endPoint():
                return True
            else:
                return False

        elif obj1.ShapeType() == "Face":
            if obj1.Center() == obj2.Center():
                if obj1.normalAt() == obj2.normalAt():
                    if obj1.Area() == obj2.Area():
                        return True
                    else:
                        return False
                else:
                    return False
        elif obj1.ShapeType() == "Vertex":
            if obj1.toTuple() == obj2.toTuple():
                return True
            else:
                return False
        else:
            print("Unknown shape supplied for comparison!")
            return False

    @classmethod
    def get_hash(cls, obj):
        """
        Returns the hash for the object given as argument
        :param obj: edge or face for which the hash needs to be calculated
        :return: hash
        """
        if obj.ShapeType() == "Edge":
            return hash(str(obj.startPoint()) + str(obj.endPoint()))
        elif obj.ShapeType() == "Face":
            return hash(str(obj.Center()) + str(obj.normalAt()) + str(obj.Area()))
        elif obj.ShapeType() == "Vertex":
            return hash(str(obj.toTuple()))
        else:
            print("Cannot calculate hash, unexpected shape type found")
            return None

    @classmethod
    def get_list_hash(cls, orig_list):
        """
        Uses the get_hash method to build a list of edge or face hashes
        :param orig_list: list of edges
        :return: the list of edge hashes
        """
        list_hash = []
        for elem in orig_list:
            list_hash.append(Comparator.get_hash(elem))
        return list_hash

    @classmethod
    def compare_list(cls, list1, list2):
        """
        :param list1: list 1 to be compared
        :param list2: list 2 to be compared
        :return: whether lists are the same or not

        Check is done using hash of each element in the list
        """
        list1_hash = []
        list2_hash = []

        # Create list of hashes
        for elem in list1:
            list1_hash.append(Comparator.get_hash(elem))
        for elem in list2:
            list2_hash.append(Comparator.get_hash(elem))

        # Sort the lists
        list.sort(list1_hash)
        list.sort(list2_hash)

        # Do equality check
        for entry1, entry2 in itertools.izip(list1_hash, list2_hash):
            if entry1 != entry2:
                return False
        return True

    @classmethod
    def list_sym_diff(cls, list1, list2):
        """
        Compares two lists and reports symmetric difference between the two
        Note: hashing is performed inside this function
        :param list1:
        :param list2:
        :return:
        """
        list1_hash = []
        list2_hash = []
        for elem in list1:
            list1_hash.append(Comparator.get_hash(elem))
        for elem in list2:
            list2_hash.append(Comparator.get_hash(elem))

        set1 = set(list1_hash)
        set2 = set(list2_hash)

        return list(set1.symmetric_difference(set2))

    @classmethod
    def get_shape_type(cls, shape):
        """
        Returns the type of shape
        :param shape: object whose shape needs to be known
        :return: Face or Edge or Vertex
        """
        return shape.ShapeType()

    @classmethod
    def shape_in_hash_set(cls, shape, obj_hash_set):
        """
        Check if a shape is in the supplied hash set
        :param shape:
        :param obj_hash_set:
        :return:
        """
        for obj in obj_hash_set:
            if cls.get_hash(shape) == obj:
                return True
        return False
