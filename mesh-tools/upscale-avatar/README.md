# OBJ Upscaling (Blender-based)

This script processes a given 3D model (OBJ file), upscales its vertex count using subdivision, optionally reduces it using decimation, and exports the result as a new OBJ file.

## Features

- **Upscale Mesh**:
  - Dynamically calculates the required subdivision levels to reach a target vertex count.
  - Subdivides the mesh using Blender's `Subdivision Surface` modifier.
- **Vertex Target Count**
    - Set the desired vertex target count for the upscaled mesh.
- **Fine-tune Vertex Count**:
  - Applies a `Decimate` modifier to adjust the vertex count to a target level.
- **Manual Export**:
  - Exports the processed mesh manually to an OBJ file.

## Dependencies

This script requires the following software:
- **Blender**: Version 2.8+ (tested on Blender 4.2.3 LTS).
- **Python**: Version 3.12+

## How to Install Dependencies

1. **Install Blender**:
   - Download and install Blender from the [official website](https://www.blender.org/).

2. **Command-line Execution**:
   - Ensure Blender's executable path is accessible from your terminal or command prompt.
   - On macOS, Blender is typically located at:
     ```
     /Applications/Blender.app/Contents/MacOS/Blender
     ```

## Usage

### Running the Script

1. Save the script as `upscale_mesh.py`.

2. Use the following command format to run the script:

   ```bash
   /path/to/blender --background --python upscale_mesh.py -- avatar.obj texture.png upscaled_avatar.obj target_vertex_count



