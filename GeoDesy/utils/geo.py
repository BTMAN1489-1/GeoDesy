import math
from config import COORD_ROUND_SCALE
__all__ = (
    "R", "Coord", "Point", "Geometry"
)

R = 6371300  # радиус Земли в метрах


class Coord:
    class _Coordination:
        def __init__(self, latitude, longitude):
            self.latitude = latitude
            self.longitude = longitude

        @property
        def latitude(self):
            return self._latitude

        @latitude.setter
        def latitude(self, value: float):
            self._latitude = round(value, COORD_ROUND_SCALE)

        @property
        def longitude(self):
            return self._longitude

        @longitude.setter
        def longitude(self, value: float):
            self._longitude = round(value, COORD_ROUND_SCALE)

        def as_tuple(self):
            return self.latitude, self.longitude

    @staticmethod
    def assert_coord(latitude, longitude):
        assert abs(latitude) <= 90
        assert abs(longitude) <= 180

    def __init__(self, latitude, longitude):
        self.assert_coord(latitude, longitude)

        self._deg_coord = self._Coordination(latitude, longitude)
        self._rad_coord = self._Coordination(math.radians(latitude), math.radians(longitude))

    def update(self, latitude, longitude):
        self.assert_coord(latitude, longitude)

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

    def update(self, coord: Coord):
        self.x, self.y, self.z = _get_point(coord)

    def norm(self):
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2) + pow(self.z, 2))

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
        len1 = point1.norm()
        len2 = point2.norm()
        assert len1 != 0 and len2 != 0, "Для вычисления длины дуги векторы должны иметь невырожденную норму"
        return R * math.acos(point1 * point2 / (len1 * len2))

    @classmethod
    def get_precision_by_length(cls, length: float, in_radians: bool = False) -> float:
        # length указывается в метрах
        assert length >= 0, "Длина должна быть неотрицательна"
        assert length <= cls._MAX_LENGTH, f"Поле length должно быть не больше {cls._MAX_LENGTH}."

        precision = length * cls._CURVATURE  # отклонению 1/R радиан соответствует расстояние 1 метр
        if in_radians:
            return precision
        else:
            return math.degrees(precision)

    @classmethod
    def correct_precision_by_latitude(cls, coord: Coord, precision: float, in_radians: bool = False) -> float:
        assert precision >= 0

        if coord.degrees.latitude < 90:
            corrected_precision = precision / math.cos(coord.radians.latitude)
            if in_radians:
                return corrected_precision
            else:
                return math.degrees(corrected_precision)

        else:
            return 0
