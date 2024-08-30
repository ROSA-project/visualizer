import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation
from scipy.spatial.transform import Rotation as R

# Load the JSON data from files
with open('objects.json', 'r') as f:
    objects_data = json.load(f)

with open('simulation.json', 'r') as f:
    simulation_data = json.load(f)

# Function to generate vertices of a cube
def generate_cube_vertices(center, length, height, width):
    l, h, w = length / 2, height / 2, width / 2
    vertices = np.array([[l, h, w], [l, h, -w], [l, -h, -w], [l, -h, w],
                         [-l, h, w], [-l, h, -w], [-l, -h, -w], [-l, -h, w]])
    vertices += np.array(center)
    return vertices

# Function to plot a cube
def plot_cube(ax, vertices, color='b'):
    faces = [[vertices[j] for j in [0, 1, 2, 3]], [vertices[j] for j in [4, 5, 6, 7]],
             [vertices[j] for j in [0, 3, 7, 4]], [vertices[j] for j in [1, 2, 6, 5]],
             [vertices[j] for j in [0, 1, 5, 4]], [vertices[j] for j in [2, 3, 7, 6]]]
    ax.add_collection3d(Poly3DCollection(faces, color=color, linewidths=1, edgecolors='r', alpha=.25))

# Function to plot a sphere
def plot_sphere(ax, center, radius, color='g'):
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = center[0] + radius * np.cos(u) * np.sin(v)
    y = center[1] + radius * np.sin(u) * np.sin(v)
    z = center[2] + radius * np.cos(v)
    ax.plot_surface(x, y, z, color=color, alpha=0.6)

# Function to apply quaternion rotation to the vertices of a cube
def apply_rotation(vertices, orientation):
    r = R.from_quat(orientation)
    rotated_vertices = r.apply(vertices)
    return rotated_vertices

# Initialize the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([0, 30])
ax.set_ylim([0, 30])
ax.set_zlim([0, 30])

# Extract object shapes and parameters from objects.json
object_shapes = {}
for obj_id, obj_data in objects_data.items():
    shape_type = obj_data['shape']['type']
    params = obj_data['shape']['params']
    object_shapes[obj_id] = (shape_type, params)

# Function to update the plot for each frame of the animation
def update(frame):
    ax.cla()
    ax.set_xlim([0, 30])
    ax.set_ylim([0, 30])
    ax.set_zlim([0, 30])
    
    timestep = list(simulation_data.keys())[frame]
    timestep_data = simulation_data[timestep]
    
    for obj_id, obj_data in timestep_data.items():
        position = obj_data['position']
        orientation = obj_data['orientation']
        
        shape_type, params = object_shapes[obj_id]
        
        if shape_type == 'Cube':
            length = params['length']
            height = params['height']
            width = params['width']
            vertices = generate_cube_vertices(position, length, height, width)
            rotated_vertices = apply_rotation(vertices - position, orientation) + position
            plot_cube(ax, rotated_vertices)
        
        elif shape_type == 'Sphere':
            radius = params['radius']
            plot_sphere(ax, position, radius)

# Number of frames is equal to the number of timesteps in simulation_data
num_frames = len(simulation_data)

# Create the animation
ani = FuncAnimation(fig, update, frames=num_frames, interval=1000, repeat=False)


plt.show()
