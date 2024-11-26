"""
_vectors.py
14. November 2024

defines 2d and 3d vectors

Author:
Nilusink
"""
from copy import deepcopy, copy
import typing as tp
import math as m



class Vec2[T: (int, float)]:
    x: T
    y: T
    angle: T
    length: T

    def __init__(self) -> None:
        self.__x: T = 0
        self.__y: T = 0
        self.__angle: T = 0
        self.__length: T = 0

    # variable getters / setters
    @property
    def x(self) -> T:
        return self.__x

    @x.setter
    def x(self, value: T):
        self.__x = value
        self.__update("c")

    @property
    def y(self) -> T:
        return self.__y

    @y.setter
    def y(self, value: T):
        self.__y = value
        self.__update("c")

    @property
    def xy(self) -> tuple[T, T]:
        return self.__x, self.__y

    @xy.setter
    def xy(self, xy: tuple[T, T]):
        self.__x = xy[0]
        self.__y = xy[1]
        self.__update("c")

    @property
    def angle(self) -> float:
        """
        value in radian
        """
        return self.__angle

    @angle.setter
    def angle(self, value: float):
        """
        value in radian
        """
        value = self.normalize_angle(value)

        self.__angle = value
        self.__update("p")

    @property
    def length(self) -> float:
        return self.__length

    @length.setter
    def length(self, value: float):
        self.__length = value
        self.__update("p")

    @property
    def polar(self) -> tuple[float, float]:
        return self.__angle, self.__length

    @polar.setter
    def polar(self, polar: tuple[float, float]):
        self.__angle = polar[0]
        self.__length = polar[1]
        self.__update("p")

    # interaction
    def split_vector(self, direction: tp.Self) -> tuple[tp.Self, tp.Self]:
        """
        :param direction: A vector facing in the wanted direction
        :return: tuple[Vector in only that direction, everything else]
        """
        a = (direction.angle - self.angle)
        facing = Vec2.from_polar(
            angle=direction.angle,
            length=self.length * m.cos(a)
        )
        other = Vec2.from_polar(
            angle=direction.angle - m.pi / 2,
            length=self.length * m.sin(a)
        )

        return facing, other

    def copy(self) -> tp.Self:
        return Vec2().from_cartesian(x=self.x, y=self.y)

    def to_dict(self) -> dict:
        return {
            "x": self.x,
            "y": self.y,
            "angle": self.angle,
            "length": self.length,
        }

    def normalize(self) -> tp.Self:
        """
        set a vectors length to 1
        """
        self.length = 1
        return self

    def mirror(self, mirror_by: tp.Self) -> tp.Self:
        """
        mirror a vector by another vector
        """
        mirror_by = mirror_by.copy().normalize()
        ang_d = mirror_by.angle - self.angle
        self.angle = mirror_by.angle + 2 * ang_d
        return self

    # maths
    def __add__(self, other: tp.Self | T) -> tp.Self:
        if issubclass(type(other), Vec2):
            return Vec2.from_cartesian(x=self.x + other.x, y=self.y + other.y)

        return Vec2.from_cartesian(x=self.x + other, y=self.y + other)

    def __sub__(self, other: tp.Self | T) -> tp.Self:
        if issubclass(type(other), Vec2):
            return Vec2.from_cartesian(x=self.x - other.x, y=self.y - other.y)

        return Vec2.from_cartesian(x=self.x - other, y=self.y - other)

    def __mul__(self, other: tp.Self | float):
        if issubclass(type(other), Vec2):
            return Vec2.from_polar(
                angle=self.angle + other.angle,
                length=self.length * other.length
            )

        return Vec2.from_cartesian(x=self.x * other, y=self.y * other)

    def __truediv__(self, other: tp.Self):
        return Vec2.from_cartesian(x=self.x / other, y=self.y / other)

    # internal functions
    def __update(
            self,
            calc_from: tp.Literal["p", "polar", "c", "cartesian"]
    ) -> None:
        """
        :param calc_from: polar (p) | cartesian (c)
        """
        if calc_from in ("p", "polar"):
            self.__x = m.cos(self.angle) * self.length
            self.__y = m.sin(self.angle) * self.length

        elif calc_from in ("c", "cartesian"):
            self.__length = m.sqrt(self.x**2 + self.y**2)
            self.__angle = m.atan2(self.y, self.x)

        else:
            raise ValueError("Invalid value for \"calc_from\"")

    def __abs__(self) -> float:
        return m.sqrt(self.x**2 + self.y**2)

    def __repr__(self):
        return f"<\n" \
               f"\tVec2:\n" \
               f"\tx:{self.x}\ty:{self.y}\n" \
               f"\tangle:{self.angle}\tlength:{self.length}\n" \
               f">"

    # static and class methods.
    # creation of new instances
    @classmethod
    def from_cartesian(cls, x: T, y: T) -> tp.Self:
        p = cls()
        p.xy = x, y

        return p

    @classmethod
    def from_polar(cls, angle: float, length: float) -> tp.Self:
        p = cls()
        p.polar = angle, length

        return p

    @classmethod
    def from_dict(cls, dictionary: dict) -> tp.Self:
        if "x" in dictionary and "y" in dictionary:
            return cls.from_cartesian(x=dictionary["x"], y=dictionary["y"])

        elif "angle" in dictionary and "length" in dictionary:
            return cls.from_polar(
                angle=dictionary["angle"],
                length=dictionary["length"]
                )

        else:
            raise KeyError(
                "either (x & y) or (angle & length) must be in dict!"
            )

    @staticmethod
    def normalize_angle(value: float) -> float:
        while value > 2 * m.pi:
            value -= 2 * m.pi

        while value < 0:
            value += 2 * m.pi

        return value


class Vec3[_T: int | float]:
    """
    Simple 3D vector class
    """
    x: _T
    y: _T
    z: _T
    angle_xy: float
    angle_xz: float
    length_xy: float
    length: float

    def __init__(self):
        self.__x: _T = 0
        self.__y: _T = 0
        self.__z: _T = 0
        self.__angle_xy: float = 0
        self.__angle_xz: float = 0
        self.__length_xy: float = 0
        self.__length: float = 0

    @property
    def x(self) -> _T:
        return self.__x

    @x.setter
    def x(self, value: _T) -> None:
        self.__x = value
        self.__update("c")

    @property
    def y(self) -> _T:
        return self.__y

    @y.setter
    def y(self, value: _T) -> None:
        self.__y = value
        self.__update("c")

    @property
    def z(self) -> _T:
        return self.__z

    @z.setter
    def z(self, value: _T) -> None:
        self.__z = value
        self.__update("c")

    @property
    def xyz(self) -> tp.Tuple[_T, _T, _T]:
        """
        :return: x, y, z
        """
        return self.x, self.y, self.z

    @xyz.setter
    def xyz(self, value: tp.Tuple[_T, _T, _T]) -> None:
        """
        :param value: (x, y, z)
        """
        self.__x, self.__y, self.__z = value
        self.__update("c")

    @property
    def angle_xy(self) -> float:
        return self.__angle_xy

    @angle_xy.setter
    def angle_xy(self, value: float) -> None:
        self.__angle_xy = self.normalize_angle(value)
        self.__update("p")

    @property
    def angle_xz(self) -> float:
        return self.__angle_xz

    @angle_xz.setter
    def angle_xz(self, value: float) -> None:
        self.__angle_xz = self.normalize_angle(value)
        self.__update("p")

    @property
    def length_xy(self) -> float:
        """
        can't be set
        """
        return self.__length_xy

    @property
    def length(self) -> float:
        return self.__length

    @length.setter
    def length(self, value: float) -> None:
        self.__length = value
        self.__update("p")

    @property
    def polar(self) -> tp.Tuple[float, float, float]:
        """
        :return: angle_xy, angle_xz, length
        """
        return self.angle_xy, self.angle_xz, self.length

    @polar.setter
    def polar(self, value: tp.Tuple[float, float, float]) -> None:
        """
        :param value: (angle_xy, angle_xz, length)
        """
        self.__angle_xy = self.normalize_angle(value[0])
        self.__angle_xz = self.normalize_angle(value[1])
        self.__length = value[2]
        self.__update("p")

    @classmethod
    def from_polar(
            cls,
            angle_xy: float,
            angle_xz: float,
            length: float
    ) -> tp.Self:
        """
        create a Vector3D from polar form
        """
        v = cls()
        v.polar = angle_xy, angle_xz, length
        return v

    @classmethod
    def from_cartesian(cls, x: _T, y: _T, z: _T) -> tp.Self:
        """
        create a Vector3D from cartesian form
        """
        v = cls()
        v.xyz = x, y, z
        return v

    @staticmethod
    def calculate_with_angles(
            length: float,
            angle1: float,
            angle2: float
    ) -> tp.Tuple[float, float, float]:
        """
        calculate the x, y and z components of length facing (angle1, angle2)
        """
        tmp = m.cos(angle2) * length
        z = m.sin(angle2) * length
        x = m.cos(angle1) * tmp
        y = m.sin(angle1) * tmp

        return x, y, z

    @staticmethod
    def normalize_angle(angle: float) -> float:
        """
        removes "overflow" from an angle
        """
        while angle > 2 * m.pi:
            angle -= 2 * m.pi

        while angle < 0:
            angle += 2 * m.pi

        return angle

    # maths
    def __neg__(self) -> tp.Self:
        self.xyz = [-el for el in self.xyz]
        return self

    def __add__(self, other) -> tp.Self:
        if isinstance(other, self.__class__):
            return self.__class__.from_cartesian(
                x=self.x + other.x,
                y=self.y + other.y,
                z=self.z + other.z
            )

        return self.__class__.from_cartesian(
            x=self.x + other,
            y=self.y + other,
            z=self.z + other
        )

    def __sub__(self, other) -> tp.Self:
        if isinstance(other, self.__class__):
            return self.__class__.from_cartesian(
                x=self.x - other.x,
                y=self.y - other.y,
                z=self.z - other.z
            )

        return self.__class__.from_cartesian(
            x=self.x - other,
            y=self.y - other,
            z=self.z - other
        )

    def __mul__(self, other) -> tp.Self:
        if isinstance(other, self.__class__):
            return self.__class__.from_polar(
                angle_xy=self.angle_xy + other.angle_xy,
                angle_xz=self.angle_xz + other.angle_xz,
                length=self.length * other.length
            )

        return self.__class__.from_cartesian(
            x=self.x * other,
            y=self.y * other,
            z=self.z * other
        )

    def __truediv__(self, other) -> tp.Self:
        return self.__class__.from_cartesian(
            x=self.x / other,
            y=self.y / other,
            z=self.z / other
        )

    def copy(self, use_deepcopy: bool = False) -> tp.Self:
        new = self.__class__()
        if use_deepcopy:
            new.__dict__ = deepcopy(self.__dict__)
        else:
            new.__dict__ = copy(self.__dict__)

        return new

    def normalize(self) -> tp.Self:
        """
        cut the vectors length to 1
        """
        new = self.copy(use_deepcopy=True)
        new.length = 1
        return new

    # internal functions
    def __update(self, calc_from: str) -> None:
        match calc_from:
            case "p":
                self.__length_xy = m.cos(self.angle_xz) * self.length
                x, y, z = self.calculate_with_angles(
                    self.length,
                    self.angle_xy,
                    self.angle_xz
                )
                self.__x = x
                self.__y = y
                self.__z = z

            case "c":
                self.__length_xy = m.sqrt(self.y**2 + self.x**2)
                self.__angle_xy = m.atan2(self.y, self.x)
                self.__angle_xz = m.atan2(self.z, self.__length_xy)
                self.__length = m.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __repr__(self) -> str:
        return f"<\n" \
               f"\tVector3D:\n" \
               f"\tx:{self.x}\ty:{self.y}\tz:{self.z}\n" \
               f"\tangle_xy:{self.angle_xy}\tangle_xz:{self.__angle_xz}" \
               f"\tlength:{self.length}\n" \
               f">"


# tests
if __name__ == "__main__":
    v1 = Vec3.from_cartesian(-.2, 1, 0)
    v2 = Vec3.from_cartesian(.2, 1, 0)
    print(v1, v2, Vec3.from_cartesian(0, 1, 0))