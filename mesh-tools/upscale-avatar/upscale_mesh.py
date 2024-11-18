import bpy
import sys
import os

# Input and output paths from CLI arguments
input_obj = sys.argv[sys.argv.index("--") + 1]
texture_path = sys.argv[sys.argv.index("--") + 2]
output_obj = sys.argv[sys.argv.index("--") + 3]
target_vertex_count = int(sys.argv[sys.argv.index("--") + 4])  # New parameter for target vertex count

def load_obj_file(filepath):
    """
    Parses an OBJ file to extract vertices, faces, and optional UVs.
    """
    vertices = []
    faces = []

    with open(filepath, 'r') as obj_file:
        for line in obj_file:
            if line.startswith('v '):  # Vertex
                parts = line.strip().split()
                vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
            elif line.startswith('f '):  # Faces
                face = []
                for vertex in line.strip().split()[1:]:
                    face_data = vertex.split('/')
                    vertex_index = int(face_data[0]) - 1  # Convert to zero-based index
                    face.append(vertex_index)
                faces.append(face)

    return vertices, faces

def create_mesh(vertices, faces, name="ImportedMesh"):
    """
    Creates a Blender mesh object from vertices and faces.
    """
    # Create mesh and object
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)

    # Link object to the scene
    bpy.context.collection.objects.link(obj)

    # Set mesh data
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    return obj

def apply_texture(obj, texture_path):
    """
    Applies a texture to the given object.
    """
    # Create material
    material = bpy.data.materials.new(name="MeshMaterial")
    material.use_nodes = True
    obj.data.materials.append(material)

    # Get nodes
    bsdf = material.node_tree.nodes.get("Principled BSDF")
    tex_image = material.node_tree.nodes.new('ShaderNodeTexImage')
    tex_image.image = bpy.data.images.load(texture_path)

    # Link texture to the material
    material.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])

def export_obj(filepath, vertices, faces):
    """
    Exports a mesh to an OBJ file manually.
    """
    with open(filepath, 'w') as obj_file:
        # Write vertices
        for v in vertices:
            obj_file.write(f"v {v[0]} {v[1]} {v[2]}\n")

        # Write faces
        for f in faces:
            f_line = " ".join([str(idx + 1) for idx in f])  # Convert to 1-based indexing
            obj_file.write(f"f {f_line}\n")

def add_decimation_modifier(obj, target_vertex_count):
    """
    Adds a Decimate Modifier to reduce the vertex count to the target.
    """
    current_vertex_count = len(obj.data.vertices)
    if current_vertex_count <= target_vertex_count:
        print(f"No decimation needed. Current vertices: {current_vertex_count}")
        return

    # Calculate ratio for decimation
    ratio = target_vertex_count / current_vertex_count

    # Add and apply the decimate modifier
    decimate = obj.modifiers.new(name="Decimate", type='DECIMATE')
    decimate.ratio = ratio  # Set decimation ratio
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=decimate.name)

    final_vertex_count = len(obj.data.vertices)
    print(f"Decimation applied. Final vertices: {final_vertex_count}")

def calculate_subdivision_levels(current_vertex_count, target_vertex_count):
    """
    Calculate the number of subdivision levels required to reach the target vertex count.
    Ensures at least one subdivision is applied if the target is not reached.
    """
    levels = 0
    while current_vertex_count < target_vertex_count:
        current_vertex_count *= 4  # Subdivision roughly quadruples the vertex count
        levels += 1
    return max(1, levels - 1)  # Ensure at least one level of subdivision

# Clear all objects from the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Load OBJ data
vertices, faces = load_obj_file(input_obj)

# Create the mesh in Blender
mesh_obj = create_mesh(vertices, faces)

# Apply the texture
apply_texture(mesh_obj, texture_path)

# Calculate optimal subdivision level
current_vertex_count = len(mesh_obj.data.vertices)
subdivision_levels = calculate_subdivision_levels(current_vertex_count, target_vertex_count)

print(f"Current vertices: {current_vertex_count}, Target: {target_vertex_count}, Levels: {subdivision_levels}")

# Add subdivision modifier to upscale the mesh
subdiv = mesh_obj.modifiers.new(name="Subdivision", type='SUBSURF')
subdiv.levels = subdivision_levels  # Dynamically set subdivision level
subdiv.render_levels = subdivision_levels  # Ensure render levels match
bpy.context.view_layer.objects.active = mesh_obj

# Ensure the modifier is enabled before applying
if subdivision_levels > 0:
    bpy.ops.object.modifier_apply(modifier=subdiv.name)
else:
    print("No subdivision applied as levels are 0.")

# Update current vertex count after subdivision
current_vertex_count = len(mesh_obj.data.vertices)
print(f"Vertices after subdivision: {current_vertex_count}")

# Fine-tune vertex count with decimation
add_decimation_modifier(mesh_obj, target_vertex_count)

# Export the upscaled mesh manually
export_obj(
    output_obj,
    [v.co for v in mesh_obj.data.vertices],  # Get updated vertices after subdivision and decimation
    [p.vertices for p in mesh_obj.data.polygons]  # Get updated faces
)
print(f"Upscaled OBJ exported to: {output_obj}")
