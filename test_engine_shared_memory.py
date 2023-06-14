from multiprocessing import Process, shared_memory
import numpy as np
import time
import string
import random

# Define components
n_entities = 1_000_000
# Transform component
position = np.zeros((n_entities, 2))  # position=[x, y]
size = np.ones((n_entities, 2))  # size=[width, height]
rotation = np.zeros(n_entities)  # rotation in degrees

# Sprite component
# To simplify, let's represent the sprite as an integer instead of a string or image
sprite = np.zeros(n_entities, dtype=int) 

# Velocity component
velocity = np.zeros((n_entities, 2))  # velocity=[vx, vy]

# Define systems
def physics_system(position, size, rotation, velocity):
    while True:
        position += velocity

def render_system(position, size, rotation, sprite):
    while True:
        start_time = time.monotonic()
        for i in range(n_entities):
            render(i, position, size, rotation, sprite)
            pass
        time_taken = time.monotonic() - start_time
        fps = 1.0 / time_taken
        print(f"FPS: {fps} ({time_taken * 1000} ms) ({n_entities} entities)")

def render(entity, position, size, rotation, sprite):
    # time.sleep(0.0005)  # Simulate delay
    # print(f'Rendering entity {i} at position {position[i]} with size {size[i]} and rotation {rotation[i]}')
    pass


if __name__ == "__main__":
    # Create shared memory blocks for the component arrays
    position_shared = shared_memory.SharedMemory(create=True, size=position.nbytes)
    size_shared = shared_memory.SharedMemory(create=True, size=size.nbytes)
    rotation_shared = shared_memory.SharedMemory(create=True, size=rotation.nbytes)
    sprite_shared = shared_memory.SharedMemory(create=True, size=sprite.nbytes)
    velocity_shared = shared_memory.SharedMemory(create=True, size=velocity.nbytes)

    # Create numpy arrays backed by shared memory
    position_np = np.ndarray(position.shape, dtype=position.dtype, buffer=position_shared.buf)
    size_np = np.ndarray(size.shape, dtype=size.dtype, buffer=size_shared.buf)
    rotation_np = np.ndarray(rotation.shape, dtype=rotation.dtype, buffer=rotation_shared.buf)
    sprite_np = np.ndarray(sprite.shape, dtype=sprite.dtype, buffer=sprite_shared.buf)
    velocity_np = np.ndarray(velocity.shape, dtype=velocity.dtype, buffer=velocity_shared.buf)

    # Copy data into shared memory arrays
    np.copyto(position_np, position)
    np.copyto(size_np, size)
    np.copyto(rotation_np, rotation)
    np.copyto(sprite_np, sprite)
    np.copyto(velocity_np, velocity)

    # Start systems in separate processes
    physics_process = Process(target=physics_system, args=(position_np, size_np, rotation_np, velocity_np))
    render_process = Process(target=render_system, args=(position_np, size_np, rotation_np, sprite_np))
    physics_process.start()
    render_process.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        physics_process.terminate()
        render_process.terminate()

        # Cleanup shared memory
        position_shared.close()
        size_shared.close()
        rotation_shared.close()
        sprite_shared.close()
        velocity_shared.close()
