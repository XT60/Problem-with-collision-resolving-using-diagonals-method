import config
import pygame
import math

class static_shape_object:
    def __init__(self, position, vertices) -> None:
        ''' vertices are relative to given position'''
        self.vertices = vertices
        self.position = position
        self.colliding = False
        self.color = config.DEFAULT_SHAPE_COLOR
        self.world_vertices = list(map(lambda x: (x[0] + self.position[0], x[1] + self.position[1]), self.vertices))
        self.centralize_polygon_position()


    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.world_vertices, config.POLYGON_BORDER_WIDTH)
        pygame.draw.circle(surface, (255,0,0), self.position, 2)
        fill_polygon_with_alpha(surface, self.world_vertices, self.color)


    def centralize_polygon_position(self):
        self.position = get_centroid(self.world_vertices)
        self.vertices = []
        for vertex in self.world_vertices:
            self.vertices.append(calc_vector(self.position, vertex))


class dynamic_shape_object(static_shape_object):
    def __init__(self, position, vertices) -> None:
        super().__init__(position, vertices)
        self.facing = [0, 1]
        self.moved = False
    

    def udpdate_world_verices(self):
        self.world_vertices = list(map(lambda x: (x[0] + self.position[0], x[1] + self.position[1]), self.vertices))


    def rotate(self, angle):
        ''' rotates vertices cunter-clockwise by given angle in radians'''
        cos = math.cos(angle)
        sin = math.sin(angle)
        for vertex in self.vertices:
            x, y = vertex
            vertex[0] = x * cos - y * sin
            vertex[1] = x * sin + y * cos

        x, y = self.facing
        self.facing[0] = x * cos - y * sin
        self.facing[1] = x * sin + y * cos
        self.moved = True


    def move_forwards(self):
        self.position[0] += self.facing[0] * config.MOVEMENT_MULTIPLIER
        self.position[1] += self.facing[1] * config.MOVEMENT_MULTIPLIER
        self.moved = True


    def move_backwards(self):
        self.position[0] -= self.facing[0] * config.MOVEMENT_MULTIPLIER
        self.position[1] -= self.facing[1] * config.MOVEMENT_MULTIPLIER
        self.moved = True


    def update_variables(self, world_shapes):
        if self.moved:
            self.handle_collisions(world_shapes)
            self.udpdate_world_verices()
            self.moved = False


    def handle_collisions(self, world_shapes):
        self_edges = generate_edge_data(self)
        moved = False
        for shape in world_shapes:
            if shape is not self: 
                shape_edges = generate_edge_data(shape)
                for diag in self.vertices:
                    for point, dir in shape_edges:
                        vector = line_intersection(self.position, diag, point, dir)
                        if vector != None:
                            self.position[0] -= (diag[0] - vector[0])
                            self.position[1] -= (diag[1] - vector[1])
                            moved = True

                if moved:
                    self_edges = generate_edge_data(self)

                for diag in shape.vertices:
                    for point, dir in self_edges:
                        vector = line_intersection(shape.position, diag, point, dir)
                        if vector != None:
                            self.position[0] += (diag[0] - vector[0])
                            self.position[1] += (diag[1] - vector[1])
                            self_edges = generate_edge_data(self)
                            moved = True
        if moved:
            self.udpdate_world_verices()



def get_centroid(vertices):
    x = y = 0
    area = 0
    n = len(vertices)
    for i in range(n):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]
        tmp = p1[0] * p2[1] - p2[0] * p1[1]
        area += tmp
        x += (p1[0] + p2[0]) * tmp
        y += (p1[1] + p2[1]) * tmp
    
    return [x / (3*area), y / (3*area)] 
        

def generate_edge_data(shape):
    edge_data = []
    vertices = shape.vertices
    n = len(vertices)
    for i in range(n):
        vector = calc_vector(vertices[i], vertices[(i + 1) % n])
        position = (vertices[i][0] + shape.position[0], vertices[i][1] + shape.position[1])
        edge_data.append((position, vector))
    return edge_data


def line_intersection(p, r, q, s):
    ''' <p,q> - points,  <r,s> - vectors, if lines do intersect with each other return vetor from p to intersection point'''
    a = cross_product_2d(r, s)
    vec = calc_vector(p, q)
    b = cross_product_2d(vec, s)
    if a == 0:
        if b == 0:
            v1 = calc_vector(p, q)
            v2 = calc_vector(p, add_vectors(q, s))
            r_length = get_vector_length(r)
            if r_length != 0:
                r_versor = calc_versor(r, r_length)
                d_p = min(dot_product(r_versor, v1), dot_product(r_versor, v2))
                if 0 < d_p < r_length:
                    return multiply_vector_by_scalar(d_p, r)
    else:
        t = b / a
        s = cross_product_2d(vec, r) / a
        if 0 < t < 1 and 0 < s < 1:
            return multiply_vector_by_scalar(t, r)
    return None


def fill_polygon_with_alpha(surface, polygon, color):
    x_range = [math.inf, -math.inf]
    y_range = [math.inf, -math.inf]
    for vertex in polygon:
        x_range[0] = min(x_range[0], vertex[0])
        x_range[1] = max(x_range[1], vertex[0])
        y_range[0] = min(y_range[0], vertex[1])
        y_range[1] = max(y_range[1], vertex[1])

    surface_rect = (x_range[0], y_range[0], x_range[1] - x_range[0], y_range[1] - y_range[0])
    relative_vertices = list(map(lambda x: (x[0] - surface_rect[0], x[1] - surface_rect[1]), polygon))
    polygon_surface = pygame.Surface(surface_rect[2:])
    polygon_surface.set_colorkey((0, 0, 0))
    polygon_surface.set_alpha(config.POLYGON_FILL_ALPHA)
    pygame.draw.polygon(polygon_surface, color, relative_vertices)
    surface.blit(polygon_surface, surface_rect[:2])


def calc_vector(p1, p2):
    return [p2[0] - p1[0], p2[1] - p1[1]]

def get_vector_length(v):
    return math.sqrt(v[0]**2 + v[1]**2)

def calc_versor(v, length):
    length = math.sqrt(v[0]**2 + v[1]**2)
    return (v[0] / length , v[1] / length)

def add_vectors(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

def subtract_vectors(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def multiply_vector_by_scalar(s, v):
    return (s * v[0], s * v[1])

def cross_product_2d(v1, v2):
    return v1[0]* v2[1] - v1[1]* v2[0] 

def dot_product(v0, v1):
    return v0[0] * v1[0] + v0[1] * v1[1]