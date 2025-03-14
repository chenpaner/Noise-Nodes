import bpy
import bl_ui
import bpy.utils.previews
from bpy.app.translations import pgettext_iface as iface_

from .translations import langs
from .node_imp import NodeLib
from .icons import Icon

bl_info = {
    "name": "Noise Nodes",
    "description": "Advance Noise Nodes For blender",
    "author": "haseebahmad295",
    "version": (0, 4, 0),
    "blender": (4, 0, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Object",
}

geometry_nodes, shader_nodes = NodeLib()()


class NODE_MT_category_noise(bpy.types.Menu):
    bl_idname = "NODE_MT_category_noise"
    bl_label = "Noise Nodes"

    def draw(self, context):
        layout = self.layout

        if context.space_data.tree_type == "ShaderNodeTree":
            node_classes = shader_nodes
        else:
            node_classes = geometry_nodes

        for node_class in sorted(node_classes, key=lambda x: x.bl_name):
            operator = layout.operator(
                "node.add_node",
                text=iface_(node_class.bl_label),
                icon_value=Icon.get_icon(node_class.bl_label),
            )
            operator.type = node_class.__name__
            operator.use_transform = True

        bl_ui.node_add_menu.draw_assets_for_catalog(layout, self.bl_label)


def menu_draw(self, context):
    layout = self.layout
    layout.menu("NODE_MT_category_noise")


def register():
    Icon.register_icons()
    bpy.utils.register_class(NODE_MT_category_noise)
    bpy.types.NODE_MT_shader_node_add_all.append(menu_draw)
    bpy.types.NODE_MT_geometry_node_add_all.append(menu_draw)

    for cls in shader_nodes:
        bpy.utils.register_class(cls)
    for cls in geometry_nodes:
        bpy.utils.register_class(cls)

    bpy.app.translations.register(__name__, langs)


def unregister():
    Icon.unregister_icons()
    bpy.utils.unregister_class(NODE_MT_category_noise)
    bpy.types.NODE_MT_shader_node_add_all.remove(menu_draw)
    bpy.types.NODE_MT_geometry_node_add_all.remove(menu_draw)

    for cls in shader_nodes:
        bpy.utils.unregister_class(cls)
    for cls in geometry_nodes:
        bpy.utils.unregister_class(cls)

    bpy.app.translations.unregister(__name__)
