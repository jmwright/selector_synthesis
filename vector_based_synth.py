from .vector_common import *


def synthesize(selected_origins, selected_normals, face_origins, face_normals, selected_meta, face_meta):
	"""
	Handles the high level work of calling the correct type of synthesizer.
	"""

	selector_str = None

	# We handle a single selected face differently than multiple selected faces
	if len(selected_origins) == 1 and selected_meta[0]['is_planar']:
		selector_str = synthesize_min_max_face_selector(selected_origins, selected_normals, face_origins, face_normals, face_meta)

	return selector_str


def find_min_max_in_axis(selected_origin, selected_normal, face_origins, face_normals, face_meta, axis_index):
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
		if not face_meta[i]['is_planar']:
			continue

		# Check if the selected and current face normals are aligned
		if are_vectors_parallel(selected_normal, face_normals[i]):
			# Check to see if this distance has already been added
			if face_origins[i][axis_index] not in dist_face_map:
				dist_face_map[face_origins[i][axis_index]] = i

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
		selected_index += 1
		selected_index = -selected_index

	return (is_min, is_max, selected_index)


def synthesize_min_max_face_selector(selected_origins, selected_normals, face_origins, face_normals, face_meta):
	"""
	Synthesizes an indexed min/max selector given a list of face origins and normals.
	"""

	selector_str = '.faces("{filter}{axis}{index}")'
	axis_index = -1
	axis_str = ""
	filter_str = ""
	index_str = ""

	# Assume there is ony one selected face, for now
	selected_origin = selected_origins[0]
	selected_normal = selected_normals[0]

	# Determine if a face's normal is aligned with any axis
	if is_parallel_to_axis(selected_normal, 'X'):
		axis_str = 'X'
		axis_index = 0
	elif is_parallel_to_axis(selected_normal, 'Y'):
		axis_str = 'Y'
		axis_index = 1
	elif is_parallel_to_axis(selected_normal, 'Z'):
		axis_str = 'Z'
		axis_index = 2

	# Check to see if the selected face is aligned with an axis
	if axis_index > -1:
		# See if the face is either the minimum or maximum in this axis
		(is_min, is_max, index) = find_min_max_in_axis(selected_origin, selected_normal, face_origins, face_normals, face_meta, axis_index)

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
			selector_str = selector_str.format(filter = filter_str, axis = axis_str, index = index_str)
		else:
			selector_str = None
	else:
		selector_str = None

	return selector_str
