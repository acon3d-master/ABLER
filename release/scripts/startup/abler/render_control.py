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
from .lib import materials


class Acon3dRenderLineOperator(bpy.types.Operator):
    bl_idname = "acon3d.render_line"
    bl_label = "Line Render"

    def execute(self, context):
        scene = context.scene
        toggleTexture = scene.ToggleTexture
        toggleShading = scene.ToggleShading
        toggleToonEdge = scene.ToggleToonEdge
        use_lock_interface = scene.render.use_lock_interface

        def setTempMaterialSettings(dummy):
            scene.ToggleTexture = False
            scene.ToggleShading = False
            scene.ToggleToonEdge = True
            scene.render.use_lock_interface = True

            for mat in bpy.data.materials:
                mat.blend_method = "OPAQUE"
                mat.shadow_method = "OPAQUE"
                toonNode = mat.node_tree.nodes["ACON_nodeGroup_combinedToon"]
                toonNode.inputs[1].default_value = 0
                toonNode.inputs[3].default_value = 1

            bpy.app.handlers.render_pre.remove(setTempMaterialSettings)

        def rollbackMaterialSettings(dummy):
            scene.ToggleTexture = toggleTexture
            scene.ToggleShading = toggleShading
            scene.ToggleToonEdge = toggleToonEdge
            scene.render.use_lock_interface = use_lock_interface
            
            for mat in bpy.data.materials:
                materials.setMaterialParametersByType(mat)
            
            bpy.app.handlers.render_post.remove(rollbackMaterialSettings)

        bpy.app.handlers.render_pre.append(setTempMaterialSettings)
        bpy.app.handlers.render_post.append(rollbackMaterialSettings)
        bpy.ops.render.render('INVOKE_DEFAULT')

        return {'FINISHED'}


class Acon3dRenderShadowOperator(bpy.types.Operator):
    bl_idname = "acon3d.render_shadow"
    bl_label = "Shadow Render"

    def execute(self, context):
        scene = context.scene
        toggleTexture = scene.ToggleTexture
        toggleShading = scene.ToggleShading
        toggleToonEdge = scene.ToggleToonEdge
        use_lock_interface = scene.render.use_lock_interface
        node_group = bpy.data.node_groups['ACON_nodeGroup_combinedToon']

        def setTempMaterialSettings(dummy):
            scene.ToggleTexture = False
            scene.ToggleShading = True
            scene.ToggleToonEdge = False
            scene.render.use_lock_interface = True

            for node in node_group.nodes:
                if node.name == 'ACON_nodeGroup_toonFace':
                    node.inputs[5].default_value = 1

            for mat in bpy.data.materials:
                mat.blend_method = "OPAQUE"
                mat.shadow_method = "OPAQUE"
                toonNode = mat.node_tree.nodes["ACON_nodeGroup_combinedToon"]
                toonNode.inputs[1].default_value = 0
                toonNode.inputs[3].default_value = 1

            bpy.app.handlers.render_pre.remove(setTempMaterialSettings)

        def rollbackMaterialSettings(dummy):
            scene.ToggleTexture = toggleTexture
            scene.ToggleShading = toggleShading
            scene.ToggleToonEdge = toggleToonEdge
            scene.render.use_lock_interface = use_lock_interface

            for node in node_group.nodes:
                if node.name == 'ACON_nodeGroup_toonFace':
                    node.inputs[5].default_value = 0.5
            
            for mat in bpy.data.materials:
                materials.setMaterialParametersByType(mat)
            
            bpy.app.handlers.render_post.remove(rollbackMaterialSettings)

        bpy.app.handlers.render_pre.append(setTempMaterialSettings)
        bpy.app.handlers.render_post.append(rollbackMaterialSettings)
        bpy.ops.render.render('INVOKE_DEFAULT')

        return {'FINISHED'}


class Acon3dRenderPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_idname = "ACON3D_PT_render"
    bl_label = "Render"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_RENDER', 'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="RENDER_STILL")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        is_camera = False
        for obj in bpy.data.objects:
            if obj.type == 'CAMERA':
                is_camera = True
                break

        row = layout.row()
        row.operator("render.opengl", text="Quick Render")
        if is_camera:
            row.operator("render.render", text="Full Render")
        
        row = layout.row()
        row.operator("acon3d.render_line", text="Line Render")
        row.operator("acon3d.render_shadow", text="Shadow Render")


classes = (
    Acon3dRenderLineOperator,
    Acon3dRenderShadowOperator,
    Acon3dRenderPanel,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)