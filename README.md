# prism-tools
**Prism Labs Tools** is a suite of utilities designed to allow Prism Labs' Partners to easily create and manipulate scan assets for various purposes.
## Available Tools

### 1. [3D Mesh to PNG to GIF Converter](./mesh-tools/3dmesh-to-png-gif-converter/readme.md)

This tool allows you to convert 3D mesh OBJ files into a series of PNG images, which can then be compiled into a high-quality rotating GIF. It's ideal for generating visual assets from 3D models, whether for use in marketing materials or within your applications.

- **Features:**
  - Converts 3D OBJ models to a sequence of PNG images.
  - Generates a high-quality rotating GIF from the PNG sequence.
  - Customizable parameters for resolution, rotation step, camera zoom, shading, and more.
  - Supports high-resolution outputs, including 4K.

### 2. [Upscale Avatar Mesh](./mesh-tools/upscale-avatar/README.md)

This tool allows you to convert 3D mesh OBJ files into a series of PNG images, which can then be compiled into a high-quality rotating GIF. It's ideal for generating visual assets from 3D models, whether for use in marketing materials or within your applications.

This script processes a given 3D model (OBJ file), upscales its vertex count using subdivision, optionally reduces it using decimation, and exports the result as a new OBJ file.

- **Features:**
  - Upscales Mesh by dynamically calculating the required subdivision levels to reach a target vertex count.
  - Allows setting a target vertex count
  - Applies a `Decimate` modifier to adjust the vertex count to a target level.
  - Exports the processed mesh manually to an OBJ file.

## Getting Started

To get started with Prism Mesh Tools, navigate to the specific tool you wish to use. Each tool has its own directory containing the necessary scripts and a detailed README with usage instructions.

There's an assets folder with sample obj files to help you get started.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](./LICENSE) file for details.
