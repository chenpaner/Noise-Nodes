
from .nodes.geometry.Step_node import GeometryNodeStep
from .nodes.geometry.Streaks_node import GeometryNodeStreaks
from .nodes.geometry.Regular_node import GeometryNodeRegular
from .nodes.geometry.Scratches_node import GeometryNodeScratches
from .nodes.geometry.Perlin_node import GeometryNodePerlin
from .nodes.geometry.Fractal_node import GeometryNodeFractal
from .nodes.geometry.Fluid_node import GeometryNodeFluid
from .nodes.geometry.Dots_node import GeometryNodeDots
from .nodes.geometry.Dent_node import GeometryNodeDent
from .nodes.geometry.Cranal_node import GeometryNodeCranal
from .nodes.geometry.Pixelator_node import GeometryNodePixelator
from .nodes.geometry.Crackle_node import GeometryNodeCrackle

from .nodes.shader.Voxel_node import ShaderNodeVoxel
from .nodes.shader.Cranal_node import ShaderNodeCranal
from .nodes.shader.Pixelator_node import ShaderNodePixelator
from .nodes.shader.Scratches_node import ShaderNodeScratches
from .nodes.shader.Dots_node import ShaderNodeDots
from .nodes.shader.Regular_node import ShaderNodeRegular
from .nodes.shader.Dent_node import ShaderNodeDent
from .nodes.shader.Fractal_node import ShaderNodeFractal
from .nodes.shader.Streaks_node import ShaderNodeStreaks
from .nodes.shader.Fluid_node import ShaderNodeFluid
from .nodes.shader.Crackle_node import ShaderNodeCrackle
from .nodes.shader.Perlin_node import ShaderNodePerlin
from .nodes.shader.Step_node import ShaderNodeStep
from .nodes.shader.Wavy_node import ShaderNodeWavy

import bl_ui
import bpy
import nodeitems_utils
from nodeitems_utils import NodeCategory


bl_info = {
    "name": "Noise Nodes",
    "description": "Advance Noise Nodes For blender",
    "author": "haseebahmad295",
    "version": (0, 4, 0),
    "blender": (4, 0, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Object" }
    
class Panel(bpy.types.Panel):
    bl_label = "Noise Nodes"
    bl_idname = "VIEW3D_PT_noise_nodes"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Noise Nodes"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        if context.object.active_material.node_tree.nodes.active.type == "GROUP":
            x = context.object.active_material.node_tree.nodes.active.node_tree.nodes.active.location[0]
            y = context.object.active_material.node_tree.nodes.active.node_tree.nodes.active.location[1]
            row.label(text=f"X:{x}")
            row.label(text=f"Y:{y}")
        



class ExtraNodesCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return (context.space_data.tree_type == 'ShaderNodeTree' and
                context.scene.render.engine in ['BLENDER_EEVEE', 'CYCLES'])



shader_nodes = [
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


geometry_nodes = [
    GeometryNodeDent,
    GeometryNodeCranal,
    GeometryNodePixelator,
    GeometryNodeCrackle,
    GeometryNodeDots,
    GeometryNodeFluid,
    GeometryNodeFractal,
    GeometryNodePerlin,
    GeometryNodeRegular,
    GeometryNodeScratches,
    GeometryNodeStep,
    GeometryNodeStreaks,
]


node_categories = [
    ExtraNodesCategory("SH_NoiseNodes", "NoiseNodes", items=[node.__name__ for node in shader_nodes]),
    ]
geo_node_categories = [
    ExtraNodesCategory("SH_NoiseNodes", "NoiseNodes", items=[node.__name__ for node in geometry_nodes]),
    ]

class NODE_MT_category_noise(bpy.types.Menu):
    bl_idname = "NODE_MT_category_noise"
    bl_label = "Noise Nodes"

    def draw(self, context):
        layout = self.layout
        
        if context.space_data.tree_type == 'ShaderNodeTree':
            for cls in shader_nodes:
                bl_ui.node_add_menu.add_node_type(layout, cls.__name__)
        else:
            for cls in geometry_nodes:
                bl_ui.node_add_menu.add_node_type(layout, cls.__name__)
        bl_ui.node_add_menu.draw_assets_for_catalog(layout, self.bl_label)

def menu_draw(self, context):
    layout = self.layout
    layout.menu("NODE_MT_category_noise")

def register():
    bpy.utils.register_class(Panel)
    bpy.utils.register_class(NODE_MT_category_noise)
    bpy.types.NODE_MT_shader_node_add_all.append(menu_draw)
    bpy.types.NODE_MT_geometry_node_add_all.append(menu_draw)
    nodeitems_utils.register_node_categories("NOISE_NODES", node_categories)
    
    for cls in shader_nodes:
        bpy.utils.register_class(cls)
    for cls in geometry_nodes:
        bpy.utils.register_class(cls)
    
def unregister():
    bpy.utils.unregister_class(Panel)
    bpy.utils.unregister_class(NODE_MT_category_noise)
    bpy.types.NODE_MT_shader_node_add_all.remove(menu_draw)
    bpy.types.NODE_MT_geometry_node_add_all.remove(menu_draw)
    nodeitems_utils.unregister_node_categories("NOISE_NODES")
    
    for cls in shader_nodes:
        bpy.utils.unregister_class(cls)
    for cls in geometry_nodes:
        bpy.utils.unregister_class(cls)