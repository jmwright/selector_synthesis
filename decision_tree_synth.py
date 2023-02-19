"""
This script is under construction. The synthesis logic should appear here.
"""
import decision_tree_comparator
import cadquery.cq as cq
# For using Vectors in bounding box
from cadquery import Vector, BoxSelector
# For deepcopy of dict, set, list
from copy import deepcopy
import decision_tree_shape_analyzer
from math import log
# For timing synthesis procs
import time


class Selector(object):
    """"
    Edge selection, comparison and synthesis based methods
    """

    @classmethod
    def compare_vectors(cls, edge_list, obj):
        """
        Compares start and end point vectors of edges in the inputed edge list to get an appropriate selector
        :param edge_list: list of edges to be analyzed
        :return:
        """
        startpt_x_equal = True
        startpt_y_equal = True
        startpt_z_equal = True

        endpt_x_equal = True
        endpt_y_equal = True
        endpt_z_equal = True

        start_x_prev = edge_list[0].startPoint().x
        start_y_prev = edge_list[0].startPoint().y
        start_z_prev = edge_list[0].startPoint().z

        end_x_prev = edge_list[0].endPoint().x
        end_y_prev = edge_list[0].endPoint().y
        end_z_prev = edge_list[0].endPoint().z

        for index in range(1, len(edge_list)):
            start_x_curr = edge_list[index].startPoint().x
            start_y_curr = edge_list[index].startPoint().y
            start_z_curr = edge_list[index].startPoint().z

            end_x_curr = edge_list[index].endPoint().x
            end_y_curr = edge_list[index].endPoint().y
            end_z_curr = edge_list[index].endPoint().z

            if start_x_curr != start_x_prev:
                startpt_x_equal = False
            if start_y_curr != start_y_prev:
                startpt_y_equal = False
            if start_z_curr != start_z_prev:
                startpt_z_equal = False

            if end_x_curr != end_x_prev:
                endpt_x_equal = False
            if end_y_curr != end_y_prev:
                endpt_y_equal = False
            if end_z_curr != end_z_prev:
                endpt_z_equal = False

            start_x_prev = start_x_curr
            start_y_prev = start_y_curr
            start_z_prev = start_z_curr

            end_x_prev = end_x_curr
            end_y_prev = end_y_curr
            end_z_prev = end_z_curr

            # Break loop if everything already failed
            if (not startpt_x_equal) and (not startpt_y_equal) and (not startpt_z_equal) and (not endpt_x_equal) and \
                    (not endpt_y_equal) and (not endpt_z_equal):
                break

        # Print results
        if startpt_x_equal:
            print("Start points x are equal ", edge_list[0].startPoint().x)

        if startpt_y_equal:
            print("Start points y are equal ", edge_list[0].startPoint().y)

        if startpt_z_equal:
            print("Start points z are equal ", edge_list[0].startPoint().z)

        if endpt_x_equal:
            print("End points x are equal ", edge_list[0].endPoint().x)

        if endpt_y_equal:
            print("End points y are equal ", edge_list[0].endPoint().y)

        if endpt_z_equal:
            print("End points z are equal ", edge_list[0].endPoint().z)

    @classmethod
    def compare_agg(cls, edge_list, agg):
        """
        Compares a given input edge list to certain aggregated lists
        :param edge_list: list of edges to be compared
        :param agg: decision_tree_shape_analyzer.Aggregates object
        :return: string representation of match
        """
        if decision_tree_comparator.decision_tree_comparator.compare_list(edge_list, agg.edges["maxZ"]):
            print("Max Z matched")
            return ">Z"
        elif decision_tree_comparator.decision_tree_comparator.compare_list(edge_list, agg.edges["minZ"]):
            print("Min Z matched")
            return "<Z"
        elif decision_tree_comparator.decision_tree_comparator.compare_list(edge_list, agg.edges["maxY"]):
            print("Max Y matched")
            return ">Y"
        elif decision_tree_comparator.decision_tree_comparator.compare_list(edge_list, agg.edges["minY"]):
            print("Min Y matched")
            return "<Y"
        elif decision_tree_comparator.decision_tree_comparator.compare_list(edge_list, agg.edges["maxX"]):
            print("Max X matched")
            return ">X"
        elif decision_tree_comparator.decision_tree_comparator.compare_list(edge_list, agg.edges["minX"]):
            print("Min X matched")
            return "<X"
        else:
            print("Does not match with any aggregated edge list")
            return None

    @classmethod
    def synthesize_from_agg(cls, edge_list, agg, max_it=10, wt_common=1, wt_new=1):
        """
        Synthesizes a selector by using operations on aggregated lists
        :param edge_list: target list of edges
        :param agg: decision_tree_shape_analyzer.Aggregates object
        :param max_it: the maximum number of iterations this algorithm runs for
        :param wt_common: weight for common elements in aggregated list and target list
        :param wt_new: weight against addition of new elements by the aggregated list
        :return: TODO
        """

        # Calculate hashes for edge_list
        edge_list = decision_tree_comparator.decision_tree_comparator.get_list_hash(orig_list=edge_list)
        # Initially, the target set is the edge_list
        target_set = set(edge_list)
        curr_set = set()
        # Make a list of the current target set
        curr_target = list(target_set)
        # Number of iterations
        it = 0
        while target_set != curr_set and it < max_it:
            max_reward = 0
            max_key = None

            # Find max reward
            for key, value in agg.edges_hash.iteritems():
                reward = (wt_common * len(Selector.calc_intersection(curr_target, value))) \
                         - (wt_new * len(Selector.calc_diff(value, curr_target)))
                if reward > max_reward:
                    max_reward = reward
                    max_key = key

            if not (max_key is None):
                # Apply max reward
                print("Applying union with ", max_key)
                curr_set = Selector.calc_union(list(curr_set), agg.edges_hash[max_key])
                print("Target set=", target_set, "Current set=", curr_set,
                      "Symmetric difference=", target_set.symmetric_difference(curr_set))
                curr_target = list(target_set - curr_set)
                it = it + 1
            else:
                print("No appropriate aggregate set found, breaking...")
                break

    @classmethod
    def synthesize_from_agg_dtree(cls, target_list, cad_obj, bounding_box=False, mode=0, verbose=False):
        """
        Synthesizes a selector using decision tree
        :param target_list:
        :param cad_obj: the full cad object
        :param mode = 0, 1, or 2- chaining off, on or adaptive
        :param verbose = print statements or not
        :return: TODO
        """
        if verbose:
            print("Started synthesis using decision tree")

        # Make the decision tree
        dtree = DecisionTree(cq_obj=cad_obj, target_list=target_list, bounding_box=bounding_box, mode=mode,
                             verbose=verbose)
        return dtree.formula

    @classmethod
    def synthesize_bounding_box(cls, cad_obj, target_list, cushion=0.00000001, verbose=True):
        """
        Synthesizes a bounding box for the edge_list provided.
        For an edge list, being inside a particular bounding box means that for each edge in the edge list,
        the edge's bounding box lies inside this particular bounding box.
        :param target_list: List of edges for which a bounding box is to be found
        :param cad_obj: the overall cad object we're working on
        :param cushion: A small value by which the bounding box is extended in each direction
        :param mode: "Edge", "Vertex" or "Face"
        :return: BB and side effect list
        """
        # Get the kind of shape we are working with
        mode = decision_tree_comparator.decision_tree_comparator.get_shape_type(target_list[0])

        # Bounding box
        vector1 = None
        vector2 = None

        # Get min/max points for the bounding box
        for elem in target_list:
            temp_bb = elem.BoundingBox()
            if vector2 is None or vector1 is None:
                vector2 = Vector(temp_bb.xmax + cushion, temp_bb.ymax + cushion, temp_bb.zmax + cushion)
                vector1 = Vector(temp_bb.xmin - cushion, temp_bb.ymin - cushion, temp_bb.zmin - cushion)
            else:
                if temp_bb.xmin < vector1.x:
                    vector1.x = temp_bb.xmin - cushion
                if temp_bb.xmax > vector2.x:
                    vector2.x = temp_bb.xmax + cushion

                if temp_bb.ymin < vector1.y:
                    vector1.y = temp_bb.ymin - cushion
                if temp_bb.ymax > vector2.y:
                    vector2.y = temp_bb.ymax + cushion

                if temp_bb.zmin < vector1.z:
                    vector1.z = temp_bb.zmin - cushion
                if temp_bb.zmax > vector2.z:
                    vector2.z = temp_bb.zmax + cushion

        if verbose:
            print("The naive bounding box is=", [[vector1.x, vector1.y, vector1.z], [vector2.x, vector2.y, vector2.z]])
            # Check side effects
            print("Checking for side effects now...")

        # First we get all edges in the object
        all_objs = []
        temp = cad_obj.objects
        for tempObj in temp:
            temp_list = None
            if mode == "Edge":
                temp_list = tempObj.Edges()
            elif mode == "Face":
                temp_list = tempObj.Faces()
            elif mode == "Vertex":
                temp_list = tempObj.Vertices()
            else:
                print("Boundidng Box Synthesis: Unknown shape type encountered!")
            for obj in temp_list:
                all_objs.append(obj)

        # Now we check how many lie inside and how many outside

        # print("Edge list=", decision_tree_comparator.decision_tree_comparator.get_list_hash(target_list))

        # The box selector accepts list of edges and returns edges that satisfy the condition
        bs = BoxSelector(point0=[vector1.x, vector1.y, vector1.z], point1=[vector2.x, vector2.y, vector2.z])
        filtered_edges = bs.filter(all_objs)
        # print("Filtered edges=", decision_tree_comparator.decision_tree_comparator.get_list_hash(filtered_edges))
        side_effect = decision_tree_comparator.decision_tree_comparator.list_sym_diff(filtered_edges, target_list)
        if verbose:
            print("Side effect of applying this bounding box=", side_effect)

        return [[vector1.x, vector1.y, vector1.z], [vector2.x, vector2.y, vector2.z]], side_effect

    @classmethod
    def synthesize_bounding_box_var(cls, target_list, cad_obj, var_dict, cushion=0.2):
        """
        Synthesis of selector based on bounding box with variables in script
        :return:
        """
        # What kind of shape are we working with?
        mode = decision_tree_comparator.decision_tree_comparator.get_shape_type(target_list[0])

        # Maximum score so far
        max_score = 0
        target_set = set(target_list)
        # print (var_dict)
        # Get the closest points to the bounding box solution prior

        bb, side_effect = Selector.synthesize_bounding_box(target_list=target_list, cad_obj=cad_obj, verbose=False)
        bb_key = [[], []]
        bb_val = [[], []]

        for index in range(len(bb[0])):
            key, val = Selector.get_nearest_in_dict(var_dict, bb[0][index], flag=False)
            bb_key[0].append(key)
            bb_val[0].append(val)

        for index in range(len(bb[1])):
            key, val = Selector.get_nearest_in_dict(var_dict, bb[1][index], flag=True)
            bb_key[1].append(key)
            bb_val[1].append(val)

        # How good is this selector?
        score = Selector.get_bb_score(cad_obj, bb_val, target_list, mode=mode)
        print("Synthesized var bounding box is", bb_key, " score (0 is best, lower is better)=", score)

    @classmethod
    def get_nearest_in_dict(cls, var_dict, target, flag=True):
        """
        :param var_dict:
        :param target: the target value
        :param flag: if flag is true, then we find the smallest num larger than val, else, largest num smaller than val
        :return: key, value pair from var_dict
        """
        k = None
        v = None
        if flag:
            for key, val in var_dict.iteritems():
                if var_dict[key] > target:
                    k = key
                    v = val
                    break
        else:
            for key, val in var_dict.iteritems():
                if var_dict[key] > target:
                    break
                k = key
                v = val
        return k, v

    @classmethod
    def get_bb_score(cls, cad_obj, bb, target_set, mode="Edge"):
        """
        Returns the score, i.e., num(sel symmetric_diff. target)
        :param cad_obj: the cad object with all edges
        :param target_set:
        :param bb:
        :return:
        """
        # First we get all edges in the object
        all_objs = []
        temp = cad_obj.objects
        for tempObj in temp:
            obj_list = None
            if mode == "Edge":
                obj_list = tempObj.Edges()
            elif mode == "Face":
                obj_list = tempObj.Faces()
            elif mode == "Vertex":
                obj_list = tempObj.Vertices()
            for edge in obj_list:
                all_objs.append(edge)

        bs = BoxSelector(point0=[bb[0][0], bb[0][1], bb[0][2]], point1=[bb[1][0], bb[1][1], bb[1][2]])
        filtered_edges = bs.filter(all_objs)
        edge_set = set(filtered_edges)

        cost = len(edge_set.symmetric_difference(target_set))
        return cost

    @classmethod
    def calc_union(cls, list1, list2):
        """
        Takes two lists and returns the union
        :param list1: some list of edge hashes
        :param list2: some list of edge hashes
        :return: set intersection of list1 and list2
        """
        # Get sets with hashes
        set1 = set(list1)

        set2 = set(list2)

        # Now get intersection
        union = set1.union(set2)
        return union

    @classmethod
    def calc_intersection(cls, list1, list2):
        """
        Takes two lists and returns the number of common elements between them
        :param list1: some list of edge hashes
        :param list2: some list of edge hashes
        :return: set intersection of list1 and list2
        """
        # Get sets with hashes
        set1 = set(list1)

        set2 = set(list2)

        # Now get intersection
        common = set1.intersection(set2)
        return common

    @classmethod
    def calc_intersection(cls, list1, list2):
        """
        Takes two lists and returns the number of common elements between them
        :param list1: some list of edge hashes
        :param list2: some list of edge hashes
        :return: set intersection of list1 and list2
        """
        # Get sets with hashes
        set1 = set(list1)

        set2 = set(list2)

        # Now get intersection
        common = set1.intersection(set2)
        return common

    @classmethod
    def calc_diff(cls, list1, list2):
        """
        Calculates difference between two lists list1-list2
        :param list1: some list of edge hashes
        :param list2: some list of edge hashes
        :return: list of the difference
        """
        # Get sets with hashes
        set1 = set(list1)

        set2 = set(list2)

        # Now get intersection
        diff = set1 - set2
        return diff

    @classmethod
    def _checkUnique(cls, axis, val):
        print("Not yet implemented. "
              "This method will check uniqueness of a selector if this is not algorithmically guaranteed.")


class DecisionTree(object):
    """
    The class works with sets instead of lists unless specified otherwise in the variable identifier.
    """

    def __init__(self, cq_obj, target_list, bounding_box=False, mode=0, verbose=False):
        """
        Initializes a decision tree to get appropriate formula to get target_edges from all_edges.
        :param cq_obj: the top level cq object (cq selectors can be run on this object)
        :param target_list: the target list of shapes to be reached
        :param bounding_box: Are bounding boxes included during the decision process?
        :param mode: the mode of formula generation, 0- chaining off, 1- chaining on, 2- adaptive
        """

        # Set reference to top-level object
        self.obj = cq_obj

        # List of all edges/faces in object
        list_all = []
        temp = cq_obj.objects

        # First we find out if we are synthesizing for edges or faces
        shape_type = decision_tree_comparator.decision_tree_comparator.get_shape_type(target_list[0])

        # get list of hashes and save into target_list
        target_list = decision_tree_comparator.decision_tree_comparator.get_list_hash(orig_list=target_list)

        # start_time = time.time()
        if shape_type == "Edge":
            for tempObj in temp:
                for edge in tempObj.Edges():
                    list_all.append(edge)
            # Create a dictionary of hashes
            agg_dict = decision_tree_shape_analyzer.Aggregates(cq_obj, verbose=False, shape_type=shape_type).edges_hash
        elif shape_type == "Face":
            for tempObj in temp:
                for face in tempObj.Faces():
                    list_all.append(face)
            # Create a dictionary of hashes
            agg_dict = decision_tree_shape_analyzer.Aggregates(cq_obj, verbose=False, shape_type=shape_type).faces_hash
        elif shape_type == "Vertex":
            for tempObj in temp:
                for vertex in tempObj.Vertices():
                    list_all.append(vertex)
            # Create a dictionary of hashes
            agg_dict = decision_tree_shape_analyzer.Aggregates(cq_obj, verbose=False, shape_type=shape_type).vertices_hash
        # print("Time to calculate aggregates", time.time()-start_time)

        # get list of hashes
        list_all_hash = decision_tree_comparator.decision_tree_comparator.get_list_hash(orig_list=list_all)

        self.root = DecisionTree.Node(shape_set=set(list_all_hash), available_agg=agg_dict, )

        self.all_hash_set = set(list_all_hash)
        self.target_set = set(target_list)

        self.formula = None  # Will be set by build_tree proc
        # Time the decision tree building procedure
        start_time = time.time()

        # Older build tree function
        if self.build_tree(shape_type=shape_type, bounding_box=bounding_box, mode=mode, verbose=verbose):
            print("Tree built and it took", time.time() - start_time, "seconds")
        else:
            print("Tree could not be built...")

    def build_tree(self, shape_type, bounding_box, mode, verbose=False):
        """
        Start the process of building the tree.
        :param chaining: Do we build chained formulae or conjunction based formulae on the same aggregate
        :param bounding_box: Are bounding boxes included during the decision process?
        :param shape_type: "Edge", "Face" or "Vertex"
        :param mode: the mode of formula generation, 0- chaining off, 1- chaining on, 2- adaptive
        :param verbose: Are there a lot of descriptive print statements?
        :return:
        """
        # TODO: Fix issue with chaining where there no more shapes left anymore for a given aggregation scheme
        formula = ""
        # List which holds nodes that need to be expanded
        expansion_list = [self.root]
        # Dynamic target set
        curr_target = deepcopy(self.target_set)

        while len(expansion_list) > 0:
            # Recurse the following
            node = expansion_list[0]
            if verbose:
                print("Calculating base case on edge set, target set:", node.shape_set, self.target_set)
            # Calculate base case on this node
            base_case = DecisionTree.check_base_case(shape_set=node.shape_set, target_set=self.target_set)
            if base_case == 0:
                # We need to branch using a selector...
                # One additional branch
                neg_str = " not "
                if mode == 0:
                    # Chaining is off, we use statically calculated selectors, and 'and' to go down a tree level
                    # If our selector set (dictionary) is empty
                    if not node.available_agg:
                        print("Ran out of selectors!")
                        return False

                    max_inf_gain = -1
                    max_inf_key = None
                    # Go over all selector sets and calculate information gain
                    for key in node.available_agg:
                        sel_set = set(node.available_agg[key])
                        temp_inf_gain = DecisionTree.get_info_gain(edge_set=node.shape_set, selector_set=sel_set,
                                                                   target_set=curr_target)
                        if verbose: print("For selector", key, "the information gain is", temp_inf_gain)
                        if temp_inf_gain > max_inf_gain:
                            max_inf_gain = temp_inf_gain
                            max_inf_key = key
                    # Are we including the bounding box selector?
                    if bounding_box:
                        # If not chaining, we use the full original object to make the bounding box
                        # Target shape
                        target_shape_list = decision_tree_shape_analyzer.get_shape_list_from_hash(cq_objs=self.obj,
                                                                                    hash_list=list(curr_target),
                                                                                    shape_type=shape_type)
                        bb, side_effect = Selector.synthesize_bounding_box(cad_obj=self.obj,
                                                                           target_list=target_shape_list, verbose=False)
                        sel_set = curr_target.union(set(side_effect))
                        inf_gain = DecisionTree.get_info_gain(edge_set=node.shape_set, selector_set=sel_set,
                                                              target_set=curr_target)
                        key = str(bb)
                        if verbose: print("For selector", key, "the information gain is", inf_gain)
                        if inf_gain > max_inf_gain:
                            max_inf_key = key

                    if max_inf_key is None:
                        # No information gain more than 0 (or initial max value)
                        print("Failing, no appropriate information gain.")
                        return False

                    # Perform selection on max information gain
                    if verbose: print("Performing selection on ", max_inf_key)
                    sel_set = set(node.available_agg[max_inf_key])
                    set_pve, set_nve = DecisionTree.apply_selector(edge_set=node.shape_set, selector_set=sel_set)

                    # # Remove selector from agg dictionary
                    node.available_agg.pop(max_inf_key)

                    # Make children with additional level of branching
                    child_pve = DecisionTree.Node(shape_set=set_pve, available_agg=node.available_agg,
                                                  parent=node, sel_max_inf=max_inf_key, branching=node.branching + 1,
                                                  sel_conj=" and ")
                    child_nve = DecisionTree.Node(shape_set=set_nve, available_agg=node.available_agg,
                                                  parent=node,
                                                  sel_max_inf=neg_str + max_inf_key, branching=node.branching + 1,
                                                  sel_conj=" and ")

                if mode == 1:
                    # Chaining is on, we always calculate selectors dynamically
                    print("Failing, chained selection query generation no longer supported.")
                    return False
                    """
                    # Further splitting needed
                    max_inf_gain = -1
                    max_inf_key = None

                    # Create a new object and calculate aggregates again
                    # Create a CQ object and add all shapes to it
                    # List of objects to add to the cq object
                    cq_obj = decision_tree_shape_analyzer.CreateCQWith(cq_obj=self.obj, obj_hashes_set=node.shape_set,
                                                         shape_type=shape_type)
                    # Re-calculate aggregates
                    if shape_type == "Edge":
                        node.available_agg = decision_tree_shape_analyzer.Aggregates(cq_obj, shape_type=shape_type).edges_hash
                    elif shape_type == "Face":
                        node.available_agg = decision_tree_shape_analyzer.Aggregates(cq_obj, shape_type=shape_type).faces_hash
                    elif shape_type == "Vertex":
                        node.available_agg = decision_tree_shape_analyzer.Aggregates(cq_obj, shape_type=shape_type).vertices_hash
                    # Go over all selector sets and calculate information gain
                    for key in node.available_agg:
                        sel_set = set(node.available_agg[key])
                        temp_inf_gain = DecisionTree.get_info_gain(edge_set=node.shape_set, selector_set=sel_set,
                                                                   target_set=curr_target)
                        if verbose: print("For selector", key, "the information gain is", temp_inf_gain)
                        if temp_inf_gain > max_inf_gain:
                            max_inf_gain = temp_inf_gain
                            max_inf_key = key
                    # Are we including the bounding box selector?
                    if bounding_box:
                        # The shape on which BB is calculated
                        cq_obj_temp = decision_tree_shape_analyzer.CreateCQWith(cq_obj=self.obj, obj_hashes_set=node.shape_set,
                                                                  shape_type=shape_type)
                        # Target shape
                        target_shape_list = decision_tree_shape_analyzer.get_shape_list_from_hash(cq_objs=cq_obj_temp,
                                                                                    hash_list=list(curr_target),
                                                                                    shape_type=shape_type)

                        bb, side_effect = Selector.synthesize_bounding_box(cad_obj=cq_obj_temp,
                                                                           target_list=target_shape_list, verbose=False)
                        sel_set = curr_target.union(set(side_effect))
                        inf_gain = DecisionTree.get_info_gain(edge_set=node.shape_set, selector_set=sel_set,
                                                              target_set=curr_target)
                        key = str(bb)

                        if verbose: print("For selector", key, "the information gain is", inf_gain)
                        if inf_gain > max_inf_gain:
                            max_inf_key = key

                    if max_inf_key is None:
                        # No information gain more than 0 (or initial max value)
                        print("Failing, no appropriate information gain.")
                        return False

                    # Perform selection on max information gain
                    if verbose: print("Performing selection on ", max_inf_key)
                    sel_set = set(node.available_agg[max_inf_key])
                    set_pve, set_nve = DecisionTree.apply_selector(edge_set=node.shape_set, selector_set=sel_set)

                    child_pve = DecisionTree.Node(shape_set=set_pve, available_agg=None,
                                                  branching=node.branching + 1, parent=node, sel_max_inf=max_inf_key,
                                                  sel_conj=" . (")
                    child_nve = DecisionTree.Node(shape_set=set_pve, available_agg=None,
                                                  branching=node.branching + 1, parent=node,
                                                  sel_max_inf=neg_str + max_inf_key,
                                                  sel_conj=" . (")
                    """
                elif mode == 2:
                    # Chaining is adaptive
                    # This means that we use both, the dot operator and boolean operators
                    # Further splitting needed
                    max_inf_gain = -1
                    max_inf_key = None
                    chaining = False

                    # Go over all selector sets and calculate information gain
                    for key in node.available_agg:
                        sel_set = set(node.available_agg[key])
                        temp_inf_gain = DecisionTree.get_info_gain(edge_set=node.shape_set, selector_set=sel_set,
                                                                   target_set=curr_target)
                        if verbose: print("For selector", key, "the information gain is", temp_inf_gain)
                        if temp_inf_gain > max_inf_gain:
                            max_inf_gain = temp_inf_gain
                            max_inf_key = key
                    # Are we including the bounding box selector?
                    if bounding_box:
                        # If not chaining, we use the full original object to make the boundidng box
                        # Target shape
                        target_shape_list = decision_tree_shape_analyzer.get_shape_list_from_hash(cq_objs=self.obj,
                                                                                    hash_list=list(curr_target),
                                                                                    shape_type=shape_type)
                        bb, side_effect = Selector.synthesize_bounding_box(cad_obj=self.obj,
                                                                           target_list=target_shape_list, verbose=False)
                        sel_set = curr_target.union(set(side_effect))
                        inf_gain = DecisionTree.get_info_gain(edge_set=node.shape_set, selector_set=sel_set,
                                                              target_set=curr_target)
                        key = str(bb)
                        if verbose: print("For selector", key, "the information gain is", inf_gain)
                        if inf_gain > max_inf_gain:
                            max_inf_key = key

                    # Now we do search for the chained version
                    # We need to do recalculations for aggregates
                    # Create the CQ object
                    cq_obj_temp = decision_tree_shape_analyzer.CreateCQWith(cq_obj=self.obj, obj_hashes_set=node.shape_set,
                                                              shape_type=shape_type)
                    # Re-calculate aggregates
                    if shape_type == "Edge":
                        agg_ch = decision_tree_shape_analyzer.Aggregates(cq_obj_temp, shape_type=shape_type).edges_hash
                    elif shape_type == "Face":
                        agg_ch = decision_tree_shape_analyzer.Aggregates(cq_obj_temp, shape_type=shape_type).faces_hash
                    elif shape_type == "Vertex":
                        agg_ch = decision_tree_shape_analyzer.Aggregates(cq_obj_temp, shape_type=shape_type).vertices_hash

                    # Go over all selector sets and calculate information gain
                    for key in agg_ch:
                        sel_set = set(agg_ch[key])
                        temp_inf_gain = DecisionTree.get_info_gain(edge_set=node.shape_set, selector_set=sel_set,
                                                                   target_set=curr_target)
                        if verbose: print("For chained selector", key, "the information gain is", temp_inf_gain)
                        if temp_inf_gain > max_inf_gain:
                            max_inf_gain = temp_inf_gain
                            max_inf_key = key
                            chaining = True

                    if bounding_box:
                        # The shape on which BB is calculated is cq_obj_temp
                        # Target shape
                        target_shape_list = decision_tree_shape_analyzer.get_shape_list_from_hash(cq_objs=cq_obj_temp,
                                                                                    hash_list=list(curr_target),
                                                                                    shape_type=shape_type)

                        bb, side_effect = Selector.synthesize_bounding_box(cad_obj=cq_obj_temp,
                                                                           target_list=target_shape_list,
                                                                           verbose=False)
                        sel_set = curr_target.union(set(side_effect))
                        inf_gain = DecisionTree.get_info_gain(edge_set=node.shape_set, selector_set=sel_set,
                                                              target_set=curr_target)
                        key = str(bb)

                        if verbose: print("For chained selector", key, "the information gain is", inf_gain)
                        if inf_gain > max_inf_gain:
                            max_inf_key = key
                            chaining = True

                    # Perform selection on max information gain

                    # Our selector set depends on the value of flag_chaining
                    if chaining:
                        # Chaining wins
                        if verbose: print("Performing selection on chained", max_inf_key)
                        sel_set = set(agg_ch[max_inf_key])
                        set_pve, set_nve = DecisionTree.apply_selector(edge_set=node.shape_set, selector_set=sel_set)
                        # Remove selector from dictionary
                        agg_ch.pop(max_inf_key)

                        child_pve = DecisionTree.Node(shape_set=set_pve,
                                                      parent=node, available_agg=agg_ch,
                                                      sel_max_inf=max_inf_key, branching=node.branching + 1,
                                                      sel_conj=" . ")

                        child_nve = DecisionTree.Node(shape_set=set_nve,
                                                      parent=node, available_agg=agg_ch,
                                                      sel_max_inf=neg_str + max_inf_key, branching=node.branching + 1,
                                                      sel_conj=" . ")

                    else:
                        # Unchained wins
                        if verbose: print("Performing selection on unchained", max_inf_key)
                        sel_set = set(node.available_agg[max_inf_key])
                        set_pve, set_nve = DecisionTree.apply_selector(edge_set=node.shape_set, selector_set=sel_set)
                        # Remove selector from agg dictionary
                        node.available_agg.pop(max_inf_key)

                        child_pve = DecisionTree.Node(shape_set=set_pve, available_agg=node.available_agg,
                                                      parent=node, branching=node.branching + 1,
                                                      sel_max_inf=max_inf_key,
                                                      sel_conj=" and ")
                        child_nve = DecisionTree.Node(shape_set=set_nve, available_agg=node.available_agg,
                                                      parent=node, branching=node.branching + 1,
                                                      sel_max_inf=neg_str + max_inf_key,
                                                      sel_conj=" and ")
                # Set references to children
                node.pve_child = child_pve
                node.nve_child = child_nve

                # Add children to expansion list
                expansion_list = [child_pve, child_nve] + expansion_list

            elif base_case == 1:
                if verbose: print("Reached positive base case on", node.selector_max_inf)
                close_bracket = DecisionTree.string_closebracket(node.branching)
                # Build a proper string to hold the formula
                if formula == "":
                    formula = node.selector() + close_bracket
                else:
                    formula = formula + " or ( " + node.selector() + close_bracket  # Use appropriate print
            elif base_case == -1:
                if verbose: print("Reached negative base case", node.selector_max_inf)
            # Remove node from expansion list
            expansion_list.remove(node)
        formula = formula + ")"
        # Print the final formula
        print("Formula generated is", formula)
        self.formula = formula
        return True

    # TODO: Redo the decision tree building
    def build_tree_2(self, C, T, S_curr, S, t=0):
        """
        A wrapper for the new decision tree synthesizer
        :param C: Current set of elements (initially all elements)
        :param T: Target set, i.e., the selected elements
        :param S_curr: Pre-computed set of predicates
        :param S: All available selection predicates
        :param t: threshold for re-computation of predicates
        :return:
        """
        self.synth_query(C, T, S_curr, S, t)
        return True

    def synth_query(self, C, T, S_curr, S, t=0):
        """
        Method from the paper for decision tree synthesis.
        :param C: Current set of elements (initally all elements)
        :param T: Target set, i.e., the selected elements
        :param S_curr: Pre-computed set of predicates
        :param S: All available selection predicates
        :param t: threshold for re-computation of predicates
        :return:
        """
        return ""

    @staticmethod
    def string_closebracket(num):
        str_closebracket = ""
        for i in range(num):
            str_closebracket = str_closebracket + ")"
        return str_closebracket

    class Node:
        def __init__(self, shape_set, available_agg, sel_max_inf="Error", sel_conj="", parent=None,
                     chain_same=True, branching=-1):
            """
            Create a new node
            :param shape_set: set of edges at this node
            :param available_agg: the currently available aggregated dictionary
            :param parent: ref to parent
            :param chain_same: This is a marking to
            :param branching: What level of branching is this node at?
            """
            self.shape_set = shape_set
            self.available_agg = available_agg
            self.parent = parent
            self.pve_child = None
            self.nve_child = None
            self.marking = ""
            self.selector_max_inf = sel_max_inf
            self.conj = sel_conj
            self.chain_same = chain_same
            self.inactive = False
            self.branching = branching

        def selector(self):
            if self.parent is None:
                self.inactive = True
                return ""
            elif self.parent.inactive is True:
                self.inactive = True
                return self.selector_max_inf
            else:
                # Returns the selector (Uses the status of the selector in the parent as well)
                self.inactive = True
                return self.parent.selector() + self.parent.conj + " ( " + self.selector_max_inf

    @classmethod
    def check_base_case(cls, shape_set, target_set):
        """
        Checks for the base case, i.e., all elements of shape_set belong to target_set
        Note: This method assumes shape_set and target set are sets with hashes
        :param shape_set: current list in decision tree procedure
        :param target_set: the list of target edges
        :return: 1, 0, -1 or -100
        """
        if len(shape_set) == 0:
            # Check if the set still has elements
            return -100
        if shape_set.issubset(target_set):
            # All values of edge set are in target set
            return 1
        elif len(shape_set.intersection(target_set)) == 0:
            # All values of edge set are not in target set
            return -1
        else:
            # Some values of edge set are in target set (further selection needed)
            return 0

    @classmethod
    def get_info_gain(cls, edge_set, selector_set, target_set):
        """
        Returns information gain if the shape_set
        is selected on selector_set.

        Information gain is entropy_curr - entropy_fut

        :param edge_set: current set in decision tree procedure
        :param selector_set: currently chosen selector set
        :param target_set: the set we want to reach
        :return: normalized information gain
        """

        # https://en.wikipedia.org/wiki/ID3_algorithm
        # Entropy of the current set
        curr_num_pve = len(edge_set & target_set)
        px_curr_pve = (curr_num_pve * 1.0) / len(edge_set)
        # Ensure log can be calculated
        # if px_curr_pve == 0:
        #     px_curr_pve = 0.0001
        curr_num_nve = len(edge_set - target_set)
        px_curr_nve = (curr_num_nve * 1.0) / len(edge_set)
        # Ensure log can be calculated
        # if px_curr_nve == 0:
        #     px_curr_nve = 0.0001
        entropy_curr = (-px_curr_pve * (log(px_curr_pve, 2))) + (-px_curr_nve * (log(px_curr_nve, 2)))

        # For future set, we calculate entropy of left and right child separately
        # Left child
        fut_set_1 = edge_set & selector_set
        len_fut_set_1 = len(fut_set_1)
        # Avoid possible division by 0
        if len_fut_set_1 == 0:
            # This is not a good selector
            return - 1
        fut_num_pve_1 = len(fut_set_1 & target_set)
        px_fut_pve_1 = (fut_num_pve_1 * 1.0) / len_fut_set_1
        # Ensure log can be calculated
        if px_fut_pve_1 == 0:
            px_fut_pve_1 = 0.00001
        fut_num_nve_1 = len(fut_set_1 - target_set)
        px_fut_nve_1 = (fut_num_nve_1 * 1.0) / len_fut_set_1
        # Ensure log can be calculated
        if px_fut_nve_1 == 0:
            px_fut_nve_1 = 0.00001
        entropy_fut_1 = (-px_fut_pve_1 * (log(px_fut_pve_1, 2))) + (-px_fut_nve_1 * (log(px_fut_nve_1, 2)))

        # Right child
        fut_set_2 = edge_set - selector_set
        len_fut_set_2 = len(fut_set_2)
        if len_fut_set_2 == 0:
            # This is not a good selector
            return - 1
        fut_num_pve_2 = len(fut_set_2 & target_set)
        px_fut_pve_2 = (fut_num_pve_2 * 1.0) / len_fut_set_2
        # Ensure log can be calculated
        if px_fut_pve_2 == 0:
            px_fut_pve_2 = 0.00001
        fut_num_nve_2 = len(fut_set_2 - target_set)
        px_fut_nve_2 = (fut_num_nve_2 * 1.0) / len_fut_set_2
        # Ensure log can be calculated
        if px_fut_nve_2 == 0:
            px_fut_nve_2 = 0.00001
        entropy_fut_2 = (-px_fut_pve_2 * (log(px_fut_pve_2, 2))) + (-px_fut_nve_2 * (log(px_fut_nve_2, 2)))

        entropy_new = ((len_fut_set_1 * 1.0 / len(edge_set)) * entropy_fut_1) + (
                (len_fut_set_2 * 1.0 / len(edge_set)) * entropy_fut_2)

        return entropy_curr - entropy_new

    @classmethod
    def apply_selector(cls, edge_set, selector_set):
        """
        Apply the selector set to the shape_set. This returns to children for + and - selector.
        :param edge_set:
        :param selector_set: the set of selector edges
        :return:
        """
        return (edge_set & selector_set), (edge_set - selector_set)
