import numpy as np
import tifffile
import matplotlib.pyplot as plt
import trimesh
from trimesh.voxel.ops import points_to_marching_cubes
import pyvista

data = tifffile.imread('Data/20190701--2/20190701--20119.tif') #path name to tiff file goes here

imarray = np.array(data)
num_layers, height, width = imarray.shape[0], imarray.shape[1], imarray.shape[2] # initialize number of layers, height and width
grayscale_threshold = 200

point_clouds = []
colors = []  # List to store RGB colors

for z in range(num_layers):
    layer = imarray[z, :, :]
    matching_pixels = np.where(layer >= grayscale_threshold)
    point_cloud = np.column_stack(matching_pixels)
    point_cloud = point_cloud.astype(float)  # Convert to float to handle non-integer coordinates
    point_cloud[:, 0] -= height / 2
    point_cloud[:, 1] -= width / 2
    point_cloud = np.hstack((point_cloud, np.full((point_cloud.shape[0], 1), z)))  # Add z-coordinate
    point_clouds.append(point_cloud)

    color_values = data[z, matching_pixels[0], matching_pixels[1]]
    colors.append(color_values)

combined_point_cloud = np.concatenate(point_clouds)
colors = np.concatenate(colors)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(combined_point_cloud[:, 0], combined_point_cloud[:, 1], combined_point_cloud[:, 2],
           s=1, c=colors / 255.0)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Set aspect ratio for each axis
ax.set_box_aspect([height, width, num_layers])

# plt.show()

pdata = pyvista.PolyData(combined_point_cloud)
pdata['orig_sphere'] = np.arange(1132)
sphere = pyvista.Sphere(radius=0.25) # if you change the radius the size of the spheres change
pc = pdata.glyph(scale=False, geom=sphere, orient=False)
pl = pyvista.Plotter()
_ = pl.add_mesh(
    pc,
    cmap='reds',
    smooth_shading=True,
    show_scalar_bar=False,
)
pl.export_gltf('balls.gltf')  
pl.show()

block = pyvista.read('balls.gltf') #these 3 lines show the underlying mesh of the gltf object (here they are the same as the original)
mesh = block[0][0][0]
mesh.plot(color='tan', show_edges=True, cpos='xy')

# points is a 3D numpy array (n_points, 3) coordinates of a sphere
cloud = pyvista.PolyData(combined_point_cloud)
cloud.plot()

volume = cloud.delaunay_3d(alpha=3)
shell = volume.extract_geometry()
shell.plot()


# # Create a trimesh object
# mesh = points_to_marching_cubes(combined_point_cloud)

# # Assign colors to mesh vertices
# mesh.visual.vertex_colors = colors / 255.0

# # Save the mesh as an OBJ file
# output_file = "point_cloud.gltf"
# mesh.export(output_file)