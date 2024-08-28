# 3D Mesh to PNG to GIF Converter

This tool is part of the **Prism Mesh Tools** suite within the Prism Tools repository. It is designed to convert 3D mesh OBJ files into a sequence of PNG images, which can then be compiled into a high-quality GIF. This tool is ideal for creating visual assets from 3D models, whether for use in marketing materials or within your applications.
![Alt Text](https://github.com/prismlabs-tech/prism-tools/blob/main/mesh-tools/asset-samples/prism-sample-avatar-360-2-degree-step.gif)

## Features

- Converts 3D OBJ models to a series of PNG screenshots.
- Generates a rotating GIF from the PNG sequence.
- Customizable parameters for resolution, rotation step, camera zoom, shading, and more.
- Supports high-resolution outputs, including 4K.


## Input & Output

### Input
- Mesh/scan file (`avatar.obj` or `avatar_appose.obj`)
- Texture mesh file (`texture.png`)
- Configurations (described below)

### Output
- Up to 360 PNG snapshots of the avatar at different rotation angles.
- GIF generated from the PNG files.

## Dependencies

This tool is designed to run with Python 3.x. You will need the following Python packages installed:

- `pyvista`
- `numpy`
- `Pillow`

### Installing dependencies

1. **Clone the repository:**
   ```bash
   git clone https://github.com/prismlabs-tech/prism-tools.git
   cd prism-tools/mesh-tools/3dmesh-to-png-gif-converter
   ```

2. **Install the required Python packages:**
   ```bash
   pip install pyvista numpy pillow
   ```

## Configuration & usage

1. Make sure to update file paths on the script:

Navigate to the `3dmesh-to-png-gif-converter` directory and make sure to update the file paths for the scan data you want to process (including mesh obj and texture png files) and for the outputs of the script:

```python
# Configuration parameters (replace with your own file paths)
obj_file_path = "path/avatar.obj"
texture_file_path = "path/texture.png"
output_folder = "path/3d-screenshots"
gif_path = "path/avatar-360.gif"
```

2. Configure the parameters of the script:

This script is configurable, allowing you to adjust various parameters to suit your output needs. You can modify the settings directly at the top of the script (`3dmesh-to-png-gif-converter.py`):

```python
# Adjustable parameters
rotation_step = 2  # Degrees per step in rotation
window_size = [3840, 2160]  # Resolution of the output PNGs (width, height). Choose either 4K (3840, 2160) or FHD (1920, 1080)
gif_duration = 100  # Duration in milliseconds for each frame in the GIF
smooth_shading = True  # Apply smooth shading to the mesh
dither_type = Image.FLOYDSTEINBERG  # Dithering method for GIF creation (e.g., Image.NONE, Image.FLOYDSTEINBERG)
```

3. Generate PNG Screenshots and GIF:

Once file paths and configurations are set, run the script:
```bash
python3 3dmesh-to-png-gif-converter.py
```
