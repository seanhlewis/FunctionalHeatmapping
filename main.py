#Functional Heatmapping by Sean Lewis (https://github.com/seanhlewis)
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import Circle


# ---------------------------------- IMPORTANT ---------------------------------- #
# Parameters are how you may change the shape, accuracy, funciton, and grid size of the heatmap
# Shape: Shape is the type of shape you want to calculate the average exit time for. Options are 'circle', 'square', 'triangle', or 'rectangle'
# Accuracy: Accuracy is the number of directions checked for the average exit time calculation. Higher accuracy means more directions are checked
# Function: Function is the type of growth function used for the trajectory. Options are 'straight_line', 'exponential', 'logarithmic', 'inverse', or 'spiral'
# Grid Size: Grid size is the number of points in the x and y directions for the heatmap. Higher grid size for finer resolution
# ---------------------------------- IMPORTANT ---------------------------------- #

# Parameters
shape = 'circle'  # Change this to 'circle', 'square', 'triangle', or 'rectangle'
accuracy = 3  # Higher accuracy means more directions are checked
function = 'straight_line'  # Change this to 'straight_line', 'exponential', 'logarithmic', 'inverse', or 'spiral'
grid_size = 25  # Higher grid size for finer resolution


# ----------------------------- MOVEMENT FUNCTIONS ------------------------------ #
# (In future versions, some functions may be approximated to save computation time*)
# y(t) = x
def straight_line_movement(t, x0, y0, angle):
    """A straight-line trajectory starting from (x0, y0) at a given angle."""
    x = x0 + t * np.cos(angle)
    y = y0 + t * np.sin(angle)
    return x, y

# y(t) = e^x
def exponential_movement(t, x0, y0, angle, growth_rate=0.1):
    """Exponential trajectory starting from (x0, y0) at a given angle and growth rate."""
    growth = np.exp(growth_rate * t)
    x = x0 + growth * np.cos(angle)
    y = y0 + growth * np.sin(angle)
    return x, y

# y(t) = log(x)
def logarithmic_movement(t, x0, y0, angle, base=2):
    """Logarithmic trajectory starting from (x0, y0) at a given angle and base."""
    if t == 0:
        return x0, y0
    growth = np.log(t + 1) / np.log(base)
    x = x0 + growth * np.cos(angle)
    y = y0 + growth * np.sin(angle)
    return x, y

# y(t) = 1/x
def inverse_movement(t, x0, y0, angle, scale=1.0):
    """Inverse trajectory starting from (x0, y0) at a given angle and scale."""
    if t == 0:
        return x0, y0
    growth = scale / t
    x = x0 + growth * np.cos(angle)
    y = y0 + growth * np.sin(angle)
    return x, y

# r(t) = a * theta 
def spiral_movement(t, x0, y0, angle, growth_rate=0.1):
    """Logarithmic spiral trajectory starting from (x0, y0)."""
    r = np.exp(growth_rate * t)
    theta = angle + t  # Increment angle as a function of t for spiraling
    x = x0 + r * np.cos(theta)
    y = y0 + r * np.sin(theta)
    return x, y
# ----------------------------- MOVEMENT FUNCTIONS ------------------------------ #


# Determining if a point is within a shape
def is_point_in_shape(px, py, shape, shape_params):
    """Check if a point (px, py) lies within the specified shape."""
    if shape == 'circle':
        center, radius = shape_params
        return (px - center[0]) ** 2 + (py - center[1]) ** 2 <= radius ** 2
    elif shape == 'square' or shape == 'rectangle':
        xmin, ymin, xmax, ymax = shape_params
        return xmin <= px <= xmax and ymin <= py <= ymax
    elif shape == 'triangle':
        v0, v1, v2 = shape_params
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        b1 = sign((px, py), v0, v1) < 0.0
        b2 = sign((px, py), v1, v2) < 0.0
        b3 = sign((px, py), v2, v0) < 0.0
        return b1 == b2 == b3
    else:
        raise ValueError(f"Unsupported shape: {shape}")

# Exit calculation for a single direction, within a shape using straight-line growth
def calculate_exit_time_straight(x0, y0, shape, shape_params, angle):
    """Calculate the exit time using straight-line growth starting at (x0, y0) within a shape."""
    t = 0
    dt = 0.01
    while True:
        x, y = current_function(function)(t, x0, y0, angle)
        if not is_point_in_shape(x, y, shape, shape_params):
            return t
        t += dt

# Exit time calculation across all directions
def calculate_average_exit_time_all_directions_straight(x0, y0, shape, shape_params, accuracy):
    """Calculate the average exit time across all directions using straight-line growth."""
    num_directions = 2 ** accuracy
    angles = np.linspace(0, 2 * np.pi, num_directions, endpoint=False)
    times = [calculate_exit_time_straight(x0, y0, shape, shape_params, angle) for angle in angles]
    return np.mean(times), times

# Choosing the function
def current_function(f):
    if f == 'straight_line':
        return straight_line_movement
    elif f == 'exponential':
        return exponential_movement
    elif f == 'logarithmic':
        return logarithmic_movement
    elif f == 'inverse':
        return inverse_movement
    elif f == 'spiral':
        return spiral_movement
    else:
        raise ValueError(f"Unsupported function: {f}")

# Defining shape parameters
if shape == 'circle':
    center = (0, 0)
    radius = 5
    shape_params = (center, radius)
elif shape == 'square':
    side_length = 10
    shape_params = (-side_length/2, -side_length/2, side_length/2, side_length/2)
elif shape == 'triangle':
    triangle_height = 10
    triangle_base = triangle_height / np.sqrt(3) * 2
    v0 = (0, triangle_height/2)
    v1 = (-triangle_base/2, -triangle_height/2)
    v2 = (triangle_base/2, -triangle_height/2)
    shape_params = (v0, v1, v2)
elif shape == 'rectangle':
    width = 12
    height = 8
    shape_params = (-width/2, -height/2, width/2, height/2)
else:
    raise ValueError(f"Unsupported shape: {shape}")
if shape == 'circle':
    center, radius = shape_params
    x_vals = np.linspace(center[0] - radius, center[0] + radius, grid_size)
    y_vals = np.linspace(center[1] - radius, center[1] + radius, grid_size)
else:
    x_vals = np.linspace(shape_params[0], shape_params[2], grid_size)
    y_vals = np.linspace(shape_params[1], shape_params[3], grid_size)

x_grid, y_grid = np.meshgrid(x_vals, y_vals)

# Calculating the average exit times for the grid points within the shape
exit_times = np.zeros_like(x_grid, dtype=float)

# Calculating the exit times for all grid points
for i in range(grid_size):
    for j in range(grid_size):
        x0, y0 = x_grid[i, j], y_grid[i, j]
        if is_point_in_shape(x0, y0, shape, shape_params):
            avg_time, _ = calculate_average_exit_time_all_directions_straight(x0, y0, shape, shape_params, accuracy)
            exit_times[i, j] = avg_time
        else:
            exit_times[i, j] = np.nan  # Setting points outside the shape to NaN for masking

# Creating a path for masking
if shape == 'circle':
    path = Circle(shape_params[0], shape_params[1])
elif shape == 'square' or shape == 'rectangle':
    path = Path([(shape_params[0], shape_params[1]),
                 (shape_params[2], shape_params[1]),
                 (shape_params[2], shape_params[3]),
                 (shape_params[0], shape_params[3]),
                 (shape_params[0], shape_params[1])])
elif shape == 'triangle':
    path = Path([shape_params[0], shape_params[1], shape_params[2], shape_params[0]])

# Plotting the heatmap
fig, ax = plt.subplots(figsize=(8, 8))
heatmap = ax.pcolormesh(x_grid, y_grid, exit_times, cmap='RdYlGn_r', shading='auto')
plt.colorbar(heatmap, label='Average Exit Time')

# Creating a Circle object for masking (only for 'circle' shape)
if shape == 'circle':
    center, radius = shape_params
    circle = Circle(center, radius, facecolor='none', edgecolor='none')
    ax.add_patch(circle)

# Setting the plot limits to the shape bounds
if shape == 'circle':
    ax.set_xlim(center[0] - radius, center[0] + radius)
    ax.set_ylim(center[1] - radius, center[1] + radius)
else:
    ax.set_xlim(shape_params[0], shape_params[2])
    ax.set_ylim(shape_params[1], shape_params[3])

# Setting the aspect ratio to equal to preserve the shape
ax.set_aspect('equal')

# Drawing the shape boundary
if shape == 'circle':
    ax.add_patch(plt.Circle(center, radius, fill=False, linewidth=2, color='black'))
elif shape == 'square' or shape == 'rectangle':
    ax.plot([shape_params[0], shape_params[2], shape_params[2], shape_params[0], shape_params[0]],
            [shape_params[1], shape_params[1], shape_params[3], shape_params[3], shape_params[1]],
            color='black', linewidth=2)
elif shape == 'triangle':
    ax.plot([shape_params[0][0], shape_params[1][0], shape_params[2][0], shape_params[0][0]],
            [shape_params[0][1], shape_params[1][1], shape_params[2][1], shape_params[0][1]],
            color='black', linewidth=2)

# Setting the plot title and labels
ax.set_title(f'Heatmap of Average Exit Times\nFunction: {function}\nShape: {shape.capitalize()}, Accuracy: ({2**accuracy} directions, {grid_size**2} points)')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')

# Displaying the heatmap
plt.show()