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
from .lib import scenes


class CreateSceneOperator(bpy.types.Operator):
    bl_idname = "acon3d.create_scene"
    bl_label = "Create Scene"
    bl_translation_context = "*"

    def execute(self, context):
        old_scene = context.scene
        new_scene = old_scene.copy()

        sceneName = scenes.genSceneName("ACON_Scene_")
        new_scene.name = sceneName

        new_scene.camera = old_scene.camera.copy()
        new_scene.camera.data = old_scene.camera.data.copy()
        new_scene.collection.objects.link(new_scene.camera)

        try: new_scene.collection.objects.unlink(old_scene.camera)
        except: print("Failed to unlink camera from old scene.")
        
        context.scene.ACON_prop.scene = new_scene.name

        return {'FINISHED'}


class DeleteSceneOperator(bpy.types.Operator):
    bl_idname = "acon3d.delete_scene"
    bl_label = "Delete Scene"
    bl_translation_context = "*"

    def execute(self, context):
        sceneName = context.scene.ACON_prop.scene
        scene = bpy.data.scenes[sceneName]
        bpy.data.scenes.remove(scene)

        return {'FINISHED'}


class Acon3dScenesPanel(bpy.types.Panel):
    bl_idname = "ACON3D_PT_scenes"
    bl_label = "Scenes"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="SCENE_DATA")

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        row = layout.row(align=True)
        row.prop(scene.ACON_prop, "scene", text="")
        row.operator("acon3d.create_scene", text="", icon='ADD')
        row.operator("acon3d.delete_scene", text="", icon='REMOVE')


classes = (
    CreateSceneOperator,
    DeleteSceneOperator,
    Acon3dScenesPanel,
)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)