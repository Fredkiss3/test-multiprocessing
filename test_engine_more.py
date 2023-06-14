import numpy as np
from multiprocessing import Process, Manager, cpu_count
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
def render_system(entities, entity_ids):
    while True:
        start_time = time.monotonic()
        for entity_id in entity_ids:
            components = entities[entity_id]
            if 'TransformComponent' in components and 'SpriteComponent' in components:
                transform = components['TransformComponent']
                sprite = components['SpriteComponent']
                render(entity_id, transform, sprite)
        time_taken = time.monotonic() - start_time
        fps = 1.0 / time_taken
        print(f"FPS: {fps} ({time_taken * 1000} ms) ({len(entity_ids)} entities)")

def physics_system(entities, entity_ids):
    while True:
        for entity_id in entity_ids:
            components = entities[entity_id]
            if 'TransformComponent' in components and 'VelocityComponent' in components:
                transform = components['TransformComponent']
                velocity = components['VelocityComponent']
                transform.position += velocity.velocity

# Mocked render function
def render(entity, transform, sprite):
    # time.sleep(0.0005)  # Simulate delay
    # print(f"Rendering {entity} at {transform.position} with color {sprite.color_string}")
    pass

# Now let's define our entities
def create_entities(manager_dict, n_entities=100):
    for i in range(n_entities):
        manager_dict[i] = {
            'TransformComponent': TransformComponent([0, 0], [1, 1], 0),
            'SpriteComponent': SpriteComponent('#ffffff', '/path/to/image'),
            'VelocityComponent': VelocityComponent([1, 0])
        }

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

if __name__ == "__main__":
    with Manager() as manager:
        entities = manager.dict()

        create_entities(entities, n_entities=1000)

        entity_ids = list(entities.keys())
        n_cores = cpu_count()
        entity_chunks = list(chunks(entity_ids, len(entity_ids) // n_cores))
        n_cores = cpu_count()

        processes = []

        for i in range(n_cores):
            chunk = entity_chunks[i]
            p = Process(target=physics_system, args=(entities, chunk))
            processes.append(p)
            p.start()

        for i in range(n_cores):
            chunk = entity_chunks[i]
            p = Process(target=render_system, args=(entities, chunk))
            processes.append(p)
            p.start()

        print(f"Running {len(processes)} processes in {n_cores} cores")


        try:
            while True:
                # time.sleep(0.0001)
                pass
        except KeyboardInterrupt:
            for process in processes:
                process.terminate()
            print("Application stopped.")
