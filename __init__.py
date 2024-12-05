
from .Voxel_node import ShaderNodeVoxel
from .Cranal_node import ShaderNodeCranal
from .Pixelator_node import ShaderNodePixelator
from .Scratches_node import ShaderNodeScratches
from .Dots_node import ShaderNodeDots
from .Regular_node import ShaderNodeRegular
from .Dent_node import ShaderNodeDent
from .Fractal_node import ShaderNodeFractal
from .Streaks_node import ShaderNodeStreaks
from .Fluid_node import ShaderNodeFluid
from .Crackle_node import ShaderNodeCrackle
from .Perlin_node import ShaderNodePerlin
from .Step_node import ShaderNodeStep
from .Wavy_node import ShaderNodeWavy
import bl_ui
import bpy
import os
from .translations import langs
from bpy.app.translations import pgettext_iface as iface_

import bpy,nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem
from bpy.types import Menu
from bl_ui import node_add_menu


bl_info = {
    "name": "Noise nodes",
    "description": "Description of this addon",
    "author": "Authors name",
    "version": (0, 0, 1),
    "blender": (2, 9, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Node"}
    

icons = None
def register_icons():
    plugin_folder = os.path.dirname(__file__)
    path = os.path.join(plugin_folder, "icons")
    icons = bpy.utils.previews.new()
    for i in sorted(os.listdir(path)):
        if i.endswith(".png"):
            iconname = i[:-4]
            filepath = os.path.join(path, i)
            icons.load(iconname, filepath, 'IMAGE')
    return icons

def unregister_icons(icons):
    try:
        bpy.utils.previews.remove(icons)
    except:
        pass


def get_icon(name):
    if icons and name in icons:
        return icons[name].icon_id
    else:
        return 3


class ExtraNodesCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'ShaderNodeTree' and
                context.scene.render.engine in ['BLENDER_EEVEE', 'CYCLES'])



nodes = [
    ShaderNodeVoxel,
    ShaderNodeCranal,
    ShaderNodePixelator,
    ShaderNodeScratches,
    ShaderNodeDots,
    ShaderNodeRegular,
    ShaderNodeStreaks,
    ShaderNodeFractal,
    ShaderNodeDent,
    ShaderNodeFluid,
    ShaderNodeCrackle,
    ShaderNodePerlin,
    ShaderNodeStep,
    ShaderNodeWavy
]

node_categories = [
    ExtraNodesCategory("SH_NoiseNodes", "NoiseNodes", items=[node.__name__ for node in nodes]),
    ]

class NODE_MT_category_shader_noise(bpy.types.Menu):
    bl_idname = "NODE_MT_category_shader_noise"
    bl_label = "Noise Nodes"

    def draw(self, context):
        layout = self.layout
        # for cls in nodes:
        #     bl_ui.node_add_menu.add_node_type(layout, cls.__name__)
        # bl_ui.node_add_menu.draw_assets_for_catalog(layout, self.bl_label)

        for node in nodes:
            # print(node.bl_label)
            op = layout.operator("node.add_node",text=iface_(node.bl_label), icon_value=get_icon(node.bl_label))
            op.type = node.bl_idname
            op.use_transform = True
        bl_ui.node_add_menu.draw_assets_for_catalog(layout, self.bl_label)

def menu_draw(self, context):
    layout = self.layout
    layout.menu("NODE_MT_category_shader_noise")

def register():
    global icons
    if icons is None:
        icons = register_icons()
   

    bpy.utils.register_class(NODE_MT_category_shader_noise)
    bpy.types.NODE_MT_shader_node_add_all.append(menu_draw)
    nodeitems_utils.register_node_categories("NOISE_NODES", node_categories)
    
    for cls in nodes:
        bpy.utils.register_class(cls)

    bpy.app.translations.register(__name__, langs)

def unregister():
    global icons
    unregister_icons(icons)

    bpy.utils.unregister_class(NODE_MT_category_shader_noise)
    bpy.types.NODE_MT_shader_node_add_all.remove(menu_draw)
    nodeitems_utils.unregister_node_categories("NOISE_NODES")
    
    for cls in nodes:
        bpy.utils.unregister_class(cls)

    bpy.app.translations.unregister(__name__)