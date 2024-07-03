import math
from collections import namedtuple

R = 6371300


class Coord:
    class _Coordination:
        def __init__(self, latitude, longitude):
            self.latitude = latitude
            self.longitude = longitude

    def __init__(self, latitude, longitude):
        self._deg_coord = self._Coordination(latitude, longitude)
        self._rad_coord = self._Coordination(math.radians(latitude), math.radians(longitude))

    def update(self, latitude, longitude):
        self.radians.latitude = math.radians(latitude)
        self.radians.longitude = math.radians(longitude)

        self.degrees.latitude = latitude
        self.degrees.longitude = longitude

    @property
    def radians(self):
        return self._rad_coord

    @property
    def degrees(self):
        return self._deg_coord


def _get_point(coord: Coord):
    c = coord.radians
    x = R * math.cos(c.latitude) * math.cos(c.longitude)
    y = R * math.cos(c.latitude) * math.sin(c.longitude)
    z = R * math.sin(c.latitude)
    return x, y, z


class Point:

    def __init__(self, coord: Coord):
        self.x, self.y, self.z = _get_point(coord)

    def __len__(self):
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2) + pow(self.z, 2))

    def update(self, coord: Coord):
        self.x, self.y, self.z = _get_point(coord)

    def len(self):
        return self.__len__()

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def distance(self, p2):
        return math.sqrt(pow(self.x - p2.x, 2) + pow(self.y - p2.y, 2) + pow(self.z - p2.z, 2))

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z


class Geometry:
    _CURVATURE = 1 / R
    _MAX_LENGTH = R * math.pi

    @classmethod
    def vector_length(cls, point1: Point, point2: Point):
        return point1.distance(point2)

    @classmethod
    def arc_length(cls, point1: Point, point2: Point):
        len1 = point1.len()
        len2 = point2.len()
        if len1 == 0 or len2 == 0:
            return 0
        return R * math.acos(point1 * point2 / (len1 * len2))

    @classmethod
    def get_precision_by_length(cls, length: float, coord: Coord, in_radians=False):  # length указывается в метрах
        if length <= cls._MAX_LENGTH:
            lat_precision = length * cls._CURVATURE  # отклонению 1/R радиан соответствует расстояние 1 метр
            if abs(coord.degrees.latitude) < 90:
                long_precision = lat_precision / math.cos(coord.radians.latitude)  # поправка на широту
                if in_radians:
                    return lat_precision, long_precision
                else:
                    return math.degrees(lat_precision), math.degrees(long_precision)
            return 0, 0  # на полюсах все меридианы сходятся в точку
        else:
            raise ValueError(f"Поле length должно быть не больше {cls._MAX_LENGTH}.")
