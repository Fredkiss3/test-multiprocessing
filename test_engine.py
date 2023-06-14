import numpy as np
from multiprocessing import Process, Manager

# Let's define our components
class TransformComponent:
    def __init__(self, position, size, rotation):
        self.position = np.array(position, dtype=float)
        self.size = np.array(size, dtype=float)
        self.rotation = rotation

class SpriteComponent:
    def __init__(self, color_string, image_path):
        self.color_string = color_string
        self.image_path = image_path

class VelocityComponent:
    def __init__(self, velocity):
        self.velocity = np.array(velocity, dtype=float)

# Our systems are functions that operate on entities with specific components
def render_system(manager_dict):
    for entity, components in manager_dict.items():
        if 'TransformComponent' in components and 'SpriteComponent' in components:
            transform = components['TransformComponent']
            sprite = components['SpriteComponent']
            render(entity, transform, sprite)

def physics_system(manager_dict):
    for entity, components in manager_dict.items():
        if 'TransformComponent' in components and 'VelocityComponent' in components:
            transform = components['TransformComponent']
            velocity = components['VelocityComponent']
            transform.position += velocity.velocity

# Mocked render function
def render(entity, transform, sprite):
    print(f"Rendering {entity} at {transform.position} with color {sprite.color_string}")

# Now let's define our entities
def create_entities(manager_dict):
    entity_1 = 'entity1'
    entity_2 = 'entity2'

    manager_dict[entity_1] = {
        'TransformComponent': TransformComponent([0, 0], [1, 1], 0),
        'SpriteComponent': SpriteComponent('#ffffff', '/path/to/image'),
        'VelocityComponent': VelocityComponent([1, 0])
    }

    manager_dict[entity_2] = {
        'TransformComponent': TransformComponent([5, 5], [2, 2], 0),
        'SpriteComponent': SpriteComponent('#000000', '/path/to/image'),
        'VelocityComponent': VelocityComponent([-1, 0])
    }

if __name__ == "__main__":
    with Manager() as manager:
        entities = manager.dict()

        create_entities(entities)

        physics_process = Process(target=physics_system, args=(entities,))
        render_process = Process(target=render_system, args=(entities,))

        physics_process.start()
        render_process.start()

        physics_process.join()
        render_process.join()
