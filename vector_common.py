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

	# Convert tuples/lists to Vectors, if needed
	v1 = to_vector(v1)
	v2 = to_vector(v2)

	# Do the cross-product
	cross_prod = v1.cross(v2)

	# If the cross product equals a zero vector, the vectors are parallel
	if cross_prod == Vector(0.0, 0.0, 0.0):
		are_parallel = True

	return are_parallel


def are_vectors_orthogonal(v1, v2):
	"""
	Determines if two vectors are orthogonal.
	"""
	are_orthogonal = False

	# Convert tuples/lists to Vectors, if needed
	v1 = to_vector(v1)
	v2 = to_vector(v2)

	# If the dot product is zero, the vectors are orthogonal
	if v1.dot(v2) == 0:
		are_orthogonal = True

	return are_orthogonal


def is_parallel_to_axis(vec, axis):
    """
    Determines whether or not a given vector is parallel to the specified
    axis. Often used to determine if a face normal is aligned with the axis.
    """
    axis_vec = Vector(0, 0, 0)

    vec = to_vector(vec)

    if axis.upper() == 'X':
        axis_vec = Vector(1, 0, 0)
    elif axis.upper() == 'Y':
        axis_vec = Vector(0, 1, 0)
    elif axis.upper() == 'Z':
        axis_vec = Vector(0, 0, 1)
    else:
        raise Exception("{} is not a valid axis. Must be 'X', 'Y', or 'Z'.".format(axis))

    return are_vectors_parallel(vec, axis_vec)


def is_orthogonal_to_axis(vec, axis):
	"""
	Determines whether or not a given vector is orthogonal to the specified
	axis.
	"""
	axis_vec = Vector(0, 0, 0)

	vec = to_vector(vec)

	if axis.upper() == 'X':
		axis_vec = Vector(1, 0, 0)
	elif axis.upper() == 'Y':
		axis_vec = Vector(0, 1, 0)
	elif axis.upper() == 'Z':
		axis_vec = Vector(0, 0, 1)
	else:
		raise Exception("{} is not a valid axis. Must be 'X', 'Y', or 'Z'.".format(axis))

	return are_vectors_orthogonal(vec, axis_vec)
