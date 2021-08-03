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


class Acon3dShadowPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_idname = "ACON3D_PT_shadow"
    bl_label = "Shadow / Light Control"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}    
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="LIGHT")

    def draw(self, context):
        return


class Acon3dShadowControlPanel(bpy.types.Panel):
    bl_label = "Shadow"
    bl_idname = "ACON3D_PT_shadow_sub"
    bl_parent_id = "ACON3D_PT_shadow"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        is_ACON_sun = False
        if "ACON_sun" in bpy.data.objects.keys() and bpy.data.objects["ACON_sun"].type == "LIGHT":
            is_ACON_sun = True
        layout = self.layout
        layout.active = is_ACON_sun
        if layout.active:
            sun_data = bpy.data.objects["ACON_sun"].data
            layout.prop(sun_data, "use_shadow", text="")
    
    def draw(self, context):
        is_ACON_sun = False
        if "ACON_sun" in bpy.data.objects.keys() and bpy.data.objects["ACON_sun"].type == "LIGHT":
            is_ACON_sun = True
            sun_data = bpy.data.objects["ACON_sun"].data.use_shadow
            is_ACON_sun = is_ACON_sun and sun_data

        layout = self.layout
        layout.use_property_decorate = False  # No animation.
        layout.active = is_ACON_sun
        if layout.active:
            layout.use_property_split = True
            ob = bpy.data.objects["ACON_sun"]
            if ob.rotation_mode == "XYZ":
                row = layout.row(align=True)
                row.prop(context.scene.ACON_prop, "sun_rotation_x", text="Altitude")
                row = layout.row(align=True)
                row.prop(context.scene.ACON_prop, "sun_rotation_z", text="Azimuth")


classes = (
    Acon3dShadowPanel,
    Acon3dShadowControlPanel,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)