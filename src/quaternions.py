from math import sqrt, pi, sin, cos

class Quaternion:
    def __init__(self, w, x, y, z):
        self.__w, self.__x, self.__y, self.__z = w, x, y, z
        self.__components = (w, x, y, z)

    def __add__(self, other):
        return Quaternion(*[self.__components[i] + other.__components[i] for i in range(4)])
    
    def __sub__(self, other):
        return Quaternion(*[self.__components[i] - other.__components[i] for i in range(4)])
    
    def __mul__(self, other):
        if isinstance(other, int | float):
            return Quaternion(*[component * other for component in self.__components])
        elif isinstance(other, Quaternion):
            w = self.__w * other.__w - self.__x * other.__x - self.__y * other.__y - self.__z * other.__z
            x = self.__w * other.__x + other.__w * self.__x + self.__y * other.__z - other.__y * self.__z
            y = self.__w * other.__y + other.__w * self.__y + self.__z * other.__x - other.__z * self.__x
            z = self.__w * other.__z + other.__w * self.__z + self.__x * other.__y - other.__x * self.__y
            return Quaternion(w, x, y, z)

    def __str__(self):
        return f'Quaternion(w: {self.__w:.3f}, x: {self.__x:.3f}, y: {self.__y:.3f}, z: {self.__z:.3f})'
    
    def norm(self):
        return sqrt(self.__w ** 2 + self.__x ** 2 + self.__y ** 2 + self.__z ** 2)
    
    def conjugate(self):
        return Quaternion(self.__w, *[-self.__components[i] for i in range(1, 4)])
    
    def normalize(self):
        return self * (1 / self.norm())
    
    def inverse(self):
        return self.conjugate() * (1 / self.norm() ** 2)

    def to_vector(self):
        return (self.__x, self.__y, self.__z)
    
    @staticmethod
    def rotation_quaternion(axis, angle):
        radians = angle * 2 * pi / 360
        quat = Quaternion(0, *axis).normalize() * sin(radians / 2)
        quat.__w = cos(radians / 2)
        return quat