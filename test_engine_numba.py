from multiprocessing import shared_memory, Pool, cpu_count, Manager, Array
import numpy as np
import time
import numba

n_entities = 100_000
n_processes = cpu_count()  # Define as per the number of cores in your system

# Define components
position = np.zeros((n_entities, 2))  # position=[x, y]
size = np.ones((n_entities, 2))  # size=[width, height]
rotation = np.zeros(n_entities)  # rotation in degrees
sprite = np.zeros(n_entities, dtype=int)  # Sprite component
velocity = np.zeros((n_entities, 2))  # velocity=[vx, vy]

# Define systems
# @numba.jit(nopython=True)
def physics_system(position, size, rotation, velocity):
    position += velocity

# @numba.jit(nopython=True)
def render_system(position, size, rotation, sprite):
    start_time = time.monotonic()
    for i in range(n_entities):
        render(i, position, size, rotation, sprite)
        continue
    time_taken = time.monotonic() - start_time
    fps = 1.0 / time_taken
    print(f"FPS: {fps} ({time_taken * 1000} ms) ({n_entities} entities)")


def render(entity, position, size, rotation, sprite):
    time.sleep(0.0005)  # Simulate delay
    # print(f'Rendering entity {i} at position {position[i]} with size {size[i]} and rotation {rotation[i]}')
    pass

def system_wrapper(system_and_data):
    system, data = system_and_data
    while True:
        system(*data)


if __name__ == "__main__":
    with Manager() as manager:
        # Create shared numpy arrays
        # position_np = manager.list(position)
        # size_np = manager.list(size)
        # rotation_np = manager.list(rotation)
        # sprite_np = manager.list(sprite)
        # velocity_np = manager.list(velocity)

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


        # Prepare system data
        system_data = [
            (physics_system, [position_np, size_np, rotation_np, velocity_np]),
            (render_system, [position_np, size_np, rotation_np, sprite_np])
        ]

        # Start systems in separate processes
        with Pool(processes=n_processes) as pool:
            pool.map(system_wrapper, system_data)
