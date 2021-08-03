bl_info = {
    "name": "ACON3D Panel",
    "description": "",
    "author": "sdk@acon3d.com",
    "version": (0, 0, 1),
    "blender": (2, 93, 0),
    "location": "",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "ACON3D"
}
import bpy


class Acon3dImageAdjustmentPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_idname = "ACON3D_PT_image_adjustment"
    bl_label = "Image Adjustment"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="IMAGE_DATA")

    def draw(self, context):
        return


class Acon3dBrightnessContrastPanel(bpy.types.Panel):
    bl_label = "Brightness / Contrast"
    bl_idname = "ACON3D_PT_image_sub_bright"
    bl_parent_id = "ACON3D_PT_image_adjustment"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
        if not node_group: return

        node = node_group.nodes.get('ACON_node_brightContrast')
        if not node: return

        inputs = node.inputs

        prop = context.scene.ACON_prop
        
        layout.prop(prop, "image_adjust_brightness", text="Brightness", slider=True)
        layout.prop(prop, "image_adjust_contrast", text="Contrast", slider=True)


class Acon3dColorBalancePanel(bpy.types.Panel):
    bl_label = "Color Balance"
    bl_idname = "ACON3D_PT_image_sub_color"
    bl_parent_id = "ACON3D_PT_image_adjustment"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        prop = context.scene.ACON_prop

        layout.prop(prop, "image_adjust_color_r", text="Red", slider=True)
        layout.prop(prop, "image_adjust_color_g", text="Green", slider=True)
        layout.prop(prop, "image_adjust_color_b", text="Blue", slider=True)


class Acon3dHueSaturationPanel(bpy.types.Panel):
    bl_label = "Hue / Saturation"
    bl_idname = "ACON3D_PT_image_sub_hue"
    bl_parent_id = "ACON3D_PT_image_adjustment"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
        if not node_group: return

        node = node_group.nodes.get('ACON_node_hueSaturation')
        if not node: return

        inputs = node.inputs

        layout.prop(inputs[0], "default_value", text="Hue", slider=True)
        layout.prop(inputs[1], "default_value", text="Saturation", slider=True)


classes = (
    Acon3dImageAdjustmentPanel,
    Acon3dBrightnessContrastPanel,
    Acon3dColorBalancePanel,
    Acon3dHueSaturationPanel,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)