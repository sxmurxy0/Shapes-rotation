class ShapesProvider:
    def __init__(self):
        self.__shapes = {
            'Тетраэдр': ShapeData(vertices = [(0, 0, 0.40825), (0.57735, 0, -0.40825), (-0.288675, 0.5, -0.40825), (-0.288675, -0.5, -0.40825)], 
                faces = [(0, 1, 2), (0, 2, 3), (0, 3, 1), (1, 2, 3)]),
            'Пирамида': ShapeData(vertices = [(0, 0, 0.3535), (-0.4, -0.4, -0.3535), (-0.4, 0.4, -0.3535), (0.4, 0.4, -0.3535), (0.4, -0.4, -0.3535)],
                faces = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (1, 2, 3, 4)]),
            'Куб': ShapeData(vertices = [(-0.4, -0.4, -0.4), (-0.4, 0.4, -0.4), (0.4, 0.4, -0.4), (0.4, -0.4, -0.4), (0.4, -0.4, 0.4), (-0.4, -0.4, 0.4), (-0.4, 0.4, 0.4), (0.4, 0.4, 0.4)], 
                faces = [(0, 1, 2, 3), (0, 3, 4, 5), (4, 5, 6, 7), (1, 2, 7, 6), (2, 3, 4, 7), (0, 1, 6, 5)]),
            'Октаэдр': ShapeData(vertices = [(0, 0, 0.6271), (-0.4, -0.4, 0), (-0.4, 0.4, 0), (0.4, 0.4, 0), (0.4, -0.4, 0), (0, 0, -0.6271)], 
                faces = [(0, 1, 2), (0, 2, 3), (0, 3, 4), ( 0, 4, 1), (5, 1, 2), (5, 2, 3), (5, 3, 4), (5, 4, 1)])
        }

    def shapes_names(self):
        return list(self.__shapes.keys())

    def build_shape(self, name, initial_pos, size):
        data = self.__shapes[name]
        vertices = [tuple((initial_pos[i] + vertex[i] * size) for i in range(3)) for vertex in data.vertices()]
        return ShapeData(vertices = vertices, faces = data.faces())

class ShapeData:
    def __init__(self, vertices, faces):
        self.__vertices = vertices
        self.__faces = faces
    
    def vertices(self):
        return self.__vertices
    
    def set_vertices(self, vertices):
        self.__vertices = vertices
    
    def faces(self):
        return self.__faces