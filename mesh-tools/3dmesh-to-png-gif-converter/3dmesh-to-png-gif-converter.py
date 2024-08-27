"""
Last update: 8/26/2024

This script takes a 3D bodymap OBJ file, renders it, rotates it along the x-axis in specific steps, and captures a PNG screenshot at each step.
The PNG screenshots are then compiled into a high-quality GIF. The script parameters such as resolution, rotation step, GIF duration, and zoom
can be adjusted to customize the output. At 4K, it takes about 5-7 minutes on a 2021 Macbook Pro M1. At 1080p, about 2 minutes runtime.

Configuration:
- obj_file_path: Path to the 3D OBJ file.
- texture_file_path: Path to the texture image associated with the OBJ file.
- output_folder: Directory where PNG screenshots will be saved.
- gif_path: Path where the final GIF will be saved.
- rotation_step: Degrees per step for rotation along the x-axis.
- window_size: Resolution of the output PNG images (width, height).
- camera_zoom: Adjusts how much of the mesh fills the frame.
- gif_duration: Duration in milliseconds for each frame in the GIF.
- smooth_shading: Whether to apply smooth shading to the mesh.
- dither_type: Dithering method to apply for the GIF creation.
- camera_position: Sets the camera position and focal point based on resolution and zoom.
"""

import pyvista as pv
import os
import numpy as np
from PIL import Image

# Configuration parameters (replace with your own file paths)
obj_file_path = "path/avatar.obj"
texture_file_path = "path/texture.png"
output_folder = "path/3d-screenshots"
gif_path = "path/avatar-360.gif"

# Adjustable parameters
rotation_step = 2  # Degrees per step in rotation
window_size = [3840, 2160]  # Resolution of the output PNGs (width, height). Choose either 4K (3840, 2160) or FHD (1920, 1080)
gif_duration = 100  # Duration in milliseconds for each frame in the GIF
smooth_shading = True  # Apply smooth shading to the mesh
dither_type = Image.FLOYDSTEINBERG  # Dithering method for GIF creation (e.g., Image.NONE, Image.FLOYDSTEINBERG)

# Camera position and focal point settings based on resolution and zoom level
if window_size == [3840, 2160]:
    # Use these camera settings for 4K resolution (3840 x 2160) and camera_zoom = 4.0 
    camera_position = [(0, 0, 10), (1, 0, 0), (0, 1, 0)]  # Camera looking down from above, centered
    camera_zoom = 4.0 # Adjusts how much of the mesh fills the screen
elif window_size == [1920, 1080]:
    # Use these camera settings for FHD resolution (1920 x 1080) and camera_zoom = 2.0 
    camera_position = [(0, 0, 5), (1, 0, 0), (0, 1, 0)]  # Camera looking down from above, centered
    camera_zoom = 2.0 # Adjusts how much of the mesh fills the screen
else:
    # Default camera position if other configurations are used
    camera_position = [(0, 0, 10), (1, 0, 0), (0, 1, 0)]  # General camera settings

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Set up the plotter with the desired resolution
plotter = pv.Plotter(off_screen=True, window_size=window_size)
texture = pv.read_texture(texture_file_path)
plotter.set_background(color=[0, 0, 0, 0])  # RGBA with alpha for transparency

# Set the camera position based on resolution and zoom
plotter.camera_position = camera_position

# Adjust zoom level to ensure the mesh fills more of the screen
plotter.camera.zoom(camera_zoom)  # You can adjust this value if needed

# Define the array of angles for rotation
angles = np.arange(0, 360, rotation_step)  # Generates angles from 0 to 358 degrees in steps of rotation_step

# Function to take screenshots
def take_screenshots(obj_file_path, plotter, output_folder, angles):
    for i, angle in enumerate(angles):
        # Reload the original mesh from file to ensure a complete reset
        mesh = pv.read(obj_file_path)

        # Apply the exact rotation for the current step
        mesh.rotate_x(angle, inplace=True)

        # Clear the plotter and add the new mesh
        plotter.clear()  # Clear the previous mesh from the plotter
        plotter.add_mesh(mesh, texture=texture, smooth_shading=smooth_shading)

        # Render and take a screenshot
        plotter.render()
        screenshot_path = os.path.join(output_folder, f"screenshot_{i:03d}.png")
        plotter.screenshot(screenshot_path, transparent_background=True)

# Rotate the mesh and take screenshots
take_screenshots(obj_file_path, plotter, output_folder, angles)

# Function to rotate images by -90 degrees if needed
def rotate_images(output_folder):
    for filename in os.listdir(output_folder):
        if filename.endswith(".png"):
            filepath = os.path.join(output_folder, filename)
            img = Image.open(filepath)
            rotated_image = img.rotate(90, expand=True)
            rotated_image.save(filepath)

# Rotate all screenshots by -90 degrees if needed
rotate_images(output_folder)

# Function to create a GIF from PNG images
def create_gif(output_folder, gif_path, duration=100):
    images = []
    file_list = sorted(os.listdir(output_folder))

    # Omit the last frame to ensure a perfect loop
    for filename in file_list[:-1]:  # Skip the last image to avoid duplication with the first
        if filename.endswith(".png"):
            filepath = os.path.join(output_folder, filename)
            img = Image.open(filepath).convert("RGBA")  # Ensure images have transparency
            images.append(img)

    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,  # Duration in milliseconds, consistent for all frames
        loop=0,  # Loop forever
        optimize=True,  # Optimize the GIF to reduce file size while maintaining quality
        disposal=2,  # Ensure each frame replaces the previous frame
        dither=dither_type,  # Apply dithering to simulate more colors
    )

# Create a GIF from all the rotated screenshots
create_gif(output_folder, gif_path, duration=gif_duration)  # Control the framerate by setting a consistent duration

print("Screenshots taken, rotated, and combined into a GIF successfully.")
