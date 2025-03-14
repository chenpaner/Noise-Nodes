import importlib
from pathlib import Path
import os


class NodeLib:
    BASE_DIR = Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "nodes"))

    @staticmethod
    def import_classes_from_folder(folder_path):
        imported_classes = {}

        for py_file in folder_path.glob("*.py"):
            if py_file.stem in {"__init__", "utils"}:
                continue

            module_name = f".nodes.{folder_path.name}.{py_file.stem}"
            try:
                module = importlib.import_module(module_name, package=__package__)
            except ImportError:
                continue

            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if isinstance(attribute, type):
                    if (
                        folder_path.name == "geometry"
                        and attribute_name.startswith("GeometryNode")
                        and attribute_name != "GeometryNode"
                    ):
                        imported_classes[attribute_name] = attribute
                        break
                    elif (
                        folder_path.name == "shader"
                        and attribute_name.startswith("ShaderNode")
                        and attribute_name != "ShaderNode"
                    ):
                        imported_classes[attribute_name] = attribute
                        break

        return imported_classes.values()

    @classmethod
    def __call__(cls):
        # Import all geometry nodes
        geometry_folder = cls.BASE_DIR / "geometry"
        geometry_classes = cls.import_classes_from_folder(geometry_folder)

        # Import all shader nodes
        shader_folder = cls.BASE_DIR / "shader"
        shader_classes = cls.import_classes_from_folder(shader_folder)

        return geometry_classes, shader_classes
