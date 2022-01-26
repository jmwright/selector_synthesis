from cadquery import Vector


def to_vector(vec):
	"""
	Converts tuples and lists to Vectors.
	"""

	if isinstance(vec, (tuple, list)):
		return Vector(*vec)
	elif isinstance(vec, Vector):
		return vec
	else:
		raise Exception("Cannot convert {} to a Vector".format(type(vec).__name__))

def are_vectors_parallel(v1, v2):
	"""
	Determines if two vectors are parallel.
	"""

	are_parallel = False

	# Convert tuples/lists to Vectors, if necessary
	v1 = to_vector(v1)
	v2 = to_vector(v2)

	# Do the cross-product
	cross_prod = v1.cross(v2)

	if cross_prod == Vector(0.0, 0.0, 0.0):
		are_parallel = True

	print(cross_prod)

	return are_parallel


def synthesize_max_min_face(faces):
	"""
	Synthesizes an indexed min/max selector given a list of face origins and normals.
	"""

	print("Synthesizing...")