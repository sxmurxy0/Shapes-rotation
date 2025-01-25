from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Renderer:
    def __init__(self, axes):
        self.__axes = axes
    
    def render_shape(self, shape_data, edgecolors = 'black', facecolor = '#a2d2ff', linewidth = 1.7, alpha = 0.5):
        vertices = shape_data.vertices()
        faces = [[vertices[index] for index in face] for face in shape_data.faces()]
        return self.__axes.add_collection3d(Poly3DCollection(faces, edgecolors = edgecolors, facecolor = facecolor, linewidth = linewidth, alpha = alpha))

    def render_polyline(self, vertices, linestyle = 'solid', color = 'black', linewidth = 1.7, alpha = 1):
        x, y, z = zip(*vertices)
        return self.__axes.plot(x, y, z, linestyle = linestyle, color = color, linewidth = linewidth, alpha = alpha)

    def render_points(self, vertices, marker = 'o', s = 30, color = 'black', linewidth = 1.7, edgecolors = 'face', alpha = 1):
        x, y, z = zip(*vertices)
        return self.__axes.scatter(x, y, z, marker = marker, s = s, color = color, linewidth = linewidth, edgecolors = edgecolors, alpha = alpha)