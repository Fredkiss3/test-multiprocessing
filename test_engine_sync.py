import numpy as np
from multiprocessing import Process, Manager
import time
import random
import string

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
    start_time = time.monotonic()
    for entity, components in manager_dict.items():
        if 'TransformComponent' in components and 'SpriteComponent' in components:
            transform = components['TransformComponent']
            sprite = components['SpriteComponent']
            render(entity, transform, sprite)
    time_taken = time.monotonic() - start_time
    fps = 1.0 / time_taken
    print(f"FPS: {fps} ({time_taken * 1000} ms) ({len(manager_dict)} entities)")


def physics_system(manager_dict):
        for entity, components in manager_dict.items():
            if 'TransformComponent' in components and 'VelocityComponent' in components:
                transform = components['TransformComponent']
                velocity = components['VelocityComponent']
                transform.position += velocity.velocity

# Mocked render function
def render(entity, transform, sprite):
    time.sleep(0.0005)  # Simulate delay
    # print(f"Rendering {entity} at {transform.position} with color {sprite.color_string}")
    pass

# Now let's define our entities
def create_entities(entities, n_entities=100):
    for i in range(n_entities):
        entities[i] = {
            'TransformComponent': TransformComponent([0, 0], [1, 1], 0),
            'SpriteComponent': SpriteComponent('#ffffff', '/path/to/image'),
            'VelocityComponent': VelocityComponent([1, 0])
        }

if __name__ == "__main__":
    entities = {}

    create_entities(entities, n_entities=100_000)

    try:
        while True:
            # physics_system(entities)
            render_system(entities)
            # time.sleep(0.01)  # Add delay to prevent excessive CPU usage
    except KeyboardInterrupt:
        print("Application stopped.")