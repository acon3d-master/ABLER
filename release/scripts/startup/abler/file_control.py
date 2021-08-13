bl_info = {
    "name": "ACON3D Panel",
    "description": "",
    "author": "hoie@acon3d.com",
    "version": (0, 0, 1),
    "blender": (2, 93, 0),
    "location": "",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "ACON3D"
}
import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.app.handlers import persistent

from .lib import cameras, shadow, render, scenes
from .lib.materials import materials_setup


@persistent
def load_handler(dummy):
    cameras.makeSureCameraExists()
    cameras.switchToRendredView()
    cameras.turnOnCameraView(False)
    shadow.setupSharpShadow()
    render.setupBackgroundImagesCompositor()
    materials_setup.applyAconToonStyle()
    scenes.setupPresets()


class ImportOperator(bpy.types.Operator, ImportHelper):
    """Import objects according to the current settings"""
    bl_idname = "acon3d.import_blend"
    bl_label = "Import"
    bl_translation_context = "*"

    filter_glob: bpy.props.StringProperty(
        default='*.blend', options={'HIDDEN'}
    )

    def execute(self, context):

        for obj in bpy.data.objects:
            obj.select_set(False)

        FILEPATH = self.filepath
        
        col_layers = bpy.data.collections.get("Layers")
        if not col_layers:
            col_layers = bpy.data.collections.new("Layers")
            context.scene.collection.children.link(col_layers)

        with bpy.data.libraries.load(FILEPATH) as (data_from, data_to):
            data_to.collections = data_from.collections
            data_to.objects = [name for name in data_from.objects]
        
        children_names = {}

        for coll in data_to.collections:
            for child in coll.children.keys():
                children_names[child] = True
        
        for coll in data_to.collections:
            
            found = False
            for child in children_names:
                if coll.name == child:
                    found = True
            
            if not found:
    
                added_l_exclude = context.scene.l_exclude.add()
                added_l_exclude.name = coll.name
                added_l_exclude.value = True
                col_layers.children.link(coll)

                for obj in coll.objects:
                    if obj.type == "MESH":
                        obj.select_set(True)
        
        materials_setup.applyAconToonStyle()
        cameras.switchToRendredView()
        cameras.turnOnCameraView()

        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                ctx = bpy.context.copy()
                ctx['area'] = area
                ctx['region'] = area.regions[-1]
                bpy.ops.view3d.view_selected(ctx)

        return {'FINISHED'}


class ToggleToolbarOperator(bpy.types.Operator):
    """Toggle toolbar visibility"""
    bl_idname = "acon3d.context_toggle"
    bl_label = "Toggle Toolbar"
    bl_translation_context = "*"

    def execute(self, context):
        context.scene.render.engine = "BLENDER_EEVEE"
        for area in context.screen.areas: 
            if area.type == 'VIEW_3D':
                for space in area.spaces: 
                    if space.type == 'VIEW_3D':
                        value = space.show_region_toolbar
                        space.show_region_toolbar = not value

        return {'FINISHED'}


class Acon3dImportPanel(bpy.types.Panel):
    bl_idname = "ACON3D_PT_import"
    bl_label = "File Control"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="FILE")

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.scale_y = 1.0
        row.operator("wm.open_mainfile").load_ui = False
        row.operator("acon3d.import_blend", text="Import")
        
        row = layout.row()

        prefs = context.preferences
        view = prefs.view

        row.prop(view, "language")
        row = layout.row()
        row.operator("acon3d.context_toggle")


classes = (
    Acon3dImportPanel,
    ToggleToolbarOperator,
    ImportOperator,
)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.app.handlers.load_post.append(load_handler)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)
    
    bpy.app.handlers.load_post.remove(load_handler)