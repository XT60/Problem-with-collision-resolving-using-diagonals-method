import config
import pygame
import math

class shape_object:
    def __init__(self, vertices) -> None:
        self.vertices = vertices
        self.colliding = False
        self.color = config.DEFAULT_SHAPE_COLOR


    def move(self, direcion) -> None:
        for vertex in self.vertices:
            vertex[0] += direcion[0] * config.MOVEMENT_MULTIPLIER
            vertex[1] += direcion[1] * config.MOVEMENT_MULTIPLIER


    def is_colliding(self, polygon):
        for i in range(len(polygon.vertices)):
            v0 = polygon.vertices[i]
            v1 = polygon.vertices[(i + 1) % len(polygon.vertices)]
            edge_vector = [v1[0] - v0[0], v1[1] - v0[1]]
            normal = [ - edge_vector[1], edge_vector[0]]
            self_span = span_along_line(v0, normal, self)
            polygon_span = span_along_line(v0, normal, polygon)
            if self_span[0] > polygon_span[1] or self_span[1] < polygon_span[0]:
                return False 

        for i in range(len(self.vertices)):
            v0 = self.vertices[i]
            v1 = self.vertices[(i + 1) % len(self.vertices)]
            edge_vector = [v1[0] - v0[0], v1[1] - v0[1]]
            normal = [ - edge_vector[1], edge_vector[0]]
            self_span = span_along_line(v0, normal, self)
            polygon_span = span_along_line(v0, normal, polygon)
            if self_span[0] > polygon_span[1] or self_span[1] < polygon_span[0]:
                return False 
                
        return True


    def draw(self, surface):
        pygame.draw.polygon(surface, self.color, self.vertices, config.POLYGON_BORDER_WIDTH)
        fill_polygon_with_alpha(surface, self.vertices, self.color)


def span_along_line(vertex, vector, shape):
    span = [math.inf, -math.inf]
    for v in shape.vertices:
        v_vector = [v[0] - vertex[0], v[1] - vertex[1]]
        d_p = dot_product(vector, v_vector)
        span[0] = min(span[0], d_p)
        span[1] = max(span[1], d_p)
    return span
    


def dot_product(v0, v1):
    return v0[0] * v1[0] + v0[1] * v1[1]

def fill_polygon_with_alpha(surface, polygon, color):
    # I know that this bit of code can be pretty easily optimised but used calculating power of this simulation
    # is nowhere nearof that of a big program so I thught that it would be ok to leave it here :) 
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