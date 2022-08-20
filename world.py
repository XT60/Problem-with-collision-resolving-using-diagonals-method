import config
from shape import shape_object

class world_object:
    def __init__(self) -> None:
        self.shapes = []


    def add_shape(self, vertices):
        new_shape = shape_object(vertices) 
        self.shapes.append(new_shape)
        return new_shape


    def update_variables(self):
        colliding_shapes = [False for _ in range(len(self.shapes))]
        for i, shape1 in enumerate(self.shapes):
            for j in range(i+1, len(self.shapes)):
                shape2 = self.shapes[j]
                if not shape1 is shape2 and shape1.is_colliding(shape2):
                    colliding_shapes[i] = colliding_shapes[j] = True
        
        for i, collided in enumerate(colliding_shapes):
            if collided:
                self.shapes[i].color = config.COLLIDING_SHAPE_COLOR
            else:
                self.shapes[i].color = config.DEFAULT_SHAPE_COLOR


    def draw(self, surface):
        for shape in self.shapes:
            shape.draw(surface)

