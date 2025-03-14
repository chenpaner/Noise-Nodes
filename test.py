import importlib
from pathlib import Path
import os

# Base directory for the nodes (relative to the location of this script)

BASE_DIR = Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "nodes"))


# Function to dynamically import all classes from a folder
def import_classes_from_folder(folder_path):
    classes = {}
    # Iterate over all .py files in the folder
    for file_path in folder_path.glob("*.py"):
        if file_path.stem == "__init__":  # Skip __init__.py
            continue

        # Construct the module path (e.g., ".nodes.geometry.Step_node")
        module_name = f".nodes.{folder_path.name}.{file_path.stem}"

        # Dynamically import the module
        module = importlib.import_module(module_name, package=__package__)

        # Get all classes defined in the module
        # Assumes each file has exactly one class
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type):  # Check if it's a class
                classes[attr_name] = attr
                break  # Stop after finding the first class

    return classes


# Import all geometry nodes
geometry_folder = BASE_DIR / "geometry"
geometry_classes = import_classes_from_folder(geometry_folder)

# Import all shader nodes
shader_folder = BASE_DIR / "shader"
shader_classes = import_classes_from_folder(shader_folder)

# Example usage
if __name__ == "__main__":
    # Access a specific class (e.g., GeometryNodeStep or ShaderNodeWavy)
    step_node = geometry_classes.get("GeometryNodeStep")()
    wavy_node = shader_classes.get("ShaderNodeWavy")()

    # Print to verify
    print(step_node)
    print(wavy_node)

    # Optional: Print all imported classes
    print("Geometry Classes:", list(geometry_classes.keys()))
    print("Shader Classes:", list(shader_classes.keys()))
