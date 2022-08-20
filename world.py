import config
from shape import static_shape_object
from shape import dynamic_shape_object

class world_object:
    def __init__(self) -> None:
        self.shapes = []


    def add_shape(self, position, vertices, type="static"):
        if type == "static":
            new_shape = static_shape_object(position, vertices) 
        else:
            new_shape = dynamic_shape_object(position, vertices) 
        self.shapes.append(new_shape)
        return new_shape


    def draw(self, surface):
        for shape in self.shapes:
            shape.draw(surface)

