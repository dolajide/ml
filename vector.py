from decimal import Decimal, getcontext
from math import acos, cos, pi, sqrt

getcontext().prec = 15

class Vector(object):
    """This is my custom vector class"""
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"
    ONLY_DEFINED_IN_TWO_THREE_DIMENS_MSG = "Can only cross vectors defined in two or three dimensions"
    def __init__(self, coordinates):
        """ Init Method"""
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x)*Decimal(1.0) for x in coordinates])
            self.dimension = len(self.coordinates)

        except ValueError:
            raise ValueError('The coordinates must be non-empty')

        except TypeError:
            raise TypeError('The coordinates must be iterable')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus(self, vector):
        """This method adds two vectors together"""
        return [Decimal(x)+Decimal(y) for x, y in zip(self.coordinates, vector.coordinates)]

    def minus(self, vector):
        """This method subtracts two vectors from each other"""
        return [x-y for x, y in zip(self.coordinates, vector.coordinates)]

    def times_scalar(self, scalar):
        """This method returns the scaled value of a scalar multiplication"""
        coordinates_scaled = [Decimal(x)*Decimal(scalar) for x in self.coordinates]
        return Vector(coordinates_scaled)

    def magnitude(self):
        """This method returns the maginitude of a vector"""
        coordinates_squared = [Decimal(x)**2 for x in self.coordinates]
        return Decimal(sqrt(Decimal(sum(coordinates_squared))))

    def normalized(self):
        """This method returns the unit vector of the current vector"""
        try:
            magnitude = Decimal(self.magnitude())
            return self.times_scalar(Decimal(1) / magnitude)
        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

    def angle_with(self, vector, in_degrees=False):
        """returns the angle between two vectors in either radians or degrees"""
        try:
            normalized1 = self.normalized()
            normalized2 = vector.normalized()
            print(normalized1.dot(normalized2))
            angle_in_radians = acos(normalized1.dot(normalized2))
            if in_degrees:
                return angle_in_radians * (180/pi)
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute angle with zero vector')
            else:
                raise e

    def dot(self, vector):
        """This method returns the dot operation on two vectors"""
        return sum([Decimal(x) * Decimal(y) for x, y in zip(self.coordinates, vector.coordinates)])

    def is_parallel_to(self, vector):
        """This method checks where two vectors are parallel"""
        return (self.is_zero() or vector.is_zero() or self.angle_with(vector) == 0
                or self.angle_with(vector) == pi)
        # u1 = self.angle_with(v, True)
        # if u1 == 0 or u1 == 180:
        #     return True
        # else:
        #     return False

    def is_orthorgonal_to(self, vector, tolerance=1e-10):
        """This method checks where two vectors are orthogonal"""
        return abs(self.dot(vector)) < tolerance
        # angle = self.dot(v)
        # if angle == 0:
        #     return True
        # else:
        #     return False

    def is_zero(self, tolerance=1e-10):
        """This method checks where a vector is the zero vector"""
        return self.magnitude() < tolerance

    def get_projection(self, basis):
        """Returns the projection of vectior on base which is the current object"""
        unit_base = basis.normalized()
        weight = Decimal(self.dot(unit_base))
        return unit_base.times_scalar(weight)

    def get_orthogonal(self, basis):
        """Returns the """
        proj = self.get_projection(basis)
        return self.minus(proj)
    
    def component_parallel_to(self, basis):
        try:
            u = basis.normalized()
            weight = self.dot(u)
            return u.times_scalar(weight)
        except Exception as e:
            raise e

    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)
        except Exception as e:
            raise e

    def cross(self, vector):
        """Returs cross product of this vector and an argument"""
        try:
            i = Decimal(self.coordinates[1]*vector.coordinates[2] - vector.coordinates[1]*self.coordinates[2])
            j = Decimal(-(self.coordinates[0]*vector.coordinates[2] - vector.coordinates[0]*self.coordinates[2]))
            k = Decimal(self.coordinates[0]*vector.coordinates[1] - vector.coordinates[0] * self.coordinates[1])
            v = Vector([i, j, k])
            print(self.dot(v))
            print(vector.dot(v))
            return v
        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                v1=Vector(self.coordinates+('0,'))
                w1=Vector(vector.coordinates+('0,'))
                return v1.cross(w1)
            elif (msg == 'too many values to unpack' or
                    msg == 'need more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMENS_MSG)
            else:
                raise e
    def get_area_of_parallelogram(self, vector):
        """"""
        return self.cross(vector).magnitude()

    def get_area_of_triangle(self, vector):
        """"""
        return self.get_area_of_parallelogram(vector) / Decimal(2)

v=Vector([8.462, 7.893, -8.187])
w=Vector([6.984, -5.975, 4.778])

v1=Vector([-8.987, -9.838, 5.031])
w1=Vector([-4.268, -1.861, -8.866])

v2=Vector([1.5, 9.547, 3.691])
w2=Vector([-6.007, 0.124, 5.772])

v4 = Vector([1,2])
w4 = Vector([3,1])
print(v4.angle_with(w4, True))

# print(v.cross(w))
# # print(v1.get_area_of_parallelogram(w1))
# print(v2.get_area_of_triangle(w2))