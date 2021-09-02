# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


from .lib.materials import materials_handler
from .lib import render, cameras
import bpy
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


class Acon3dCameraViewOperator(bpy.types.Operator):
    """Fit Camera Region to Viewport"""
    bl_idname = "acon3d.camera_view"
    bl_label = "Camera View"
    bl_translation_context = "*"

    def execute(self, context):
        cameras.turnOnCameraView()

        return {'FINISHED'}


class Acon3dRenderFullOperator(bpy.types.Operator):
    """Render according to the set pixel"""
    bl_idname = "acon3d.render_full"
    bl_label = "Full Render"
    bl_translation_context = "*"

    def execute(self, context):
        render.setupBackgroundImagesCompositor()
        render.matchObjectVisibility()
        bpy.ops.render.render('INVOKE_DEFAULT')

        return {'FINISHED'}


class Acon3dRenderLineOperator(bpy.types.Operator):
    """Renders only lines according to the set pixel"""
    bl_idname = "acon3d.render_line"
    bl_label = "Line Render"
    bl_translation_context = "*"

    def execute(self, context):
        scene = context.scene
        prop = scene.ACON_prop
        toggleTexture = prop.toggle_texture
        toggleShading = prop.toggle_shading
        toggleToonEdge = prop.toggle_toon_edge
        useBloom = scene.eevee.use_bloom
        use_lock_interface = scene.render.use_lock_interface
        render.clearCompositor()

        def setTempMaterialSettings(dummy):
            prop.toggle_texture = False
            prop.toggle_shading = False
            prop.toggle_toon_edge = True
            scene.eevee.use_bloom = False
            scene.render.use_lock_interface = True

            for mat in bpy.data.materials:
                mat.blend_method = "OPAQUE"
                mat.shadow_method = "OPAQUE"
                toonNode = mat.node_tree.nodes.get(
                    "ACON_nodeGroup_combinedToon")
                if toonNode:
                    toonNode.inputs[1].default_value = 0
                    toonNode.inputs[3].default_value = 1

            bpy.app.handlers.render_pre.remove(setTempMaterialSettings)

        def rollbackMaterialSettings(dummy):
            prop.toggle_texture = toggleTexture
            prop.toggle_shading = toggleShading
            prop.toggle_toon_edge = toggleToonEdge
            scene.eevee.use_bloom = useBloom
            scene.render.use_lock_interface = use_lock_interface

            for mat in bpy.data.materials:
                materials_handler.setMaterialParametersByType(mat)

            bpy.app.handlers.render_post.remove(rollbackMaterialSettings)

        bpy.app.handlers.render_pre.append(setTempMaterialSettings)
        bpy.app.handlers.render_post.append(rollbackMaterialSettings)

        render.matchObjectVisibility()
        bpy.ops.render.render('INVOKE_DEFAULT')

        return {'FINISHED'}


class Acon3dRenderShadowOperator(bpy.types.Operator):
    """Renders only shadow according to the set pixel"""
    bl_idname = "acon3d.render_shadow"
    bl_label = "Shadow Render"
    bl_translation_context = "*"

    def execute(self, context):
        scene = context.scene
        prop = scene.ACON_prop
        toggleTexture = prop.toggle_texture
        toggleShading = prop.toggle_shading
        toggleToonEdge = prop.toggle_toon_edge
        useBloom = scene.eevee.use_bloom
        use_lock_interface = scene.render.use_lock_interface
        render.clearCompositor()

        node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
        if not node_group:
            return

        def setTempMaterialSettings(dummy):
            prop.toggle_texture = False
            prop.toggle_shading = True
            prop.toggle_toon_edge = False
            scene.eevee.use_bloom = False
            scene.render.use_lock_interface = True

            for mat in bpy.data.materials:
                mat.blend_method = "OPAQUE"
                mat.shadow_method = "OPAQUE"
                toonNode = mat.node_tree.nodes.get(
                    "ACON_nodeGroup_combinedToon")
                if toonNode:
                    toonNode.inputs[1].default_value = 0
                    toonNode.inputs[3].default_value = 1

            bpy.app.handlers.render_pre.remove(setTempMaterialSettings)

        def rollbackMaterialSettings(dummy):
            prop.toggle_texture = toggleTexture
            prop.toggle_shading = toggleShading
            prop.toggle_toon_edge = toggleToonEdge
            scene.eevee.use_bloom = useBloom
            scene.render.use_lock_interface = use_lock_interface

            for mat in bpy.data.materials:
                materials_handler.setMaterialParametersByType(mat)

            bpy.app.handlers.render_post.remove(rollbackMaterialSettings)

        bpy.app.handlers.render_pre.append(setTempMaterialSettings)
        bpy.app.handlers.render_post.append(rollbackMaterialSettings)

        render.matchObjectVisibility()
        bpy.ops.render.render('INVOKE_DEFAULT')

        return {'FINISHED'}


class Acon3dRenderQuickOperator(bpy.types.Operator):
    """Quick render with deselect_all"""
    bl_idname = "acon3d.render_quick"
    bl_label = "Quick Render"
    bl_translation_context = "*"

    def execute(self, context):
        ops = bpy.ops
        if ops.object.select_all.poll():
            ops.object.select_all(action="DESELECT")
        ops.render.opengl('INVOKE_DEFAULT')
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
        layout.use_property_decorate = False  # No animation.

        is_camera = False
        for obj in bpy.data.objects:
            if obj.type == 'CAMERA':
                is_camera = True
                break

        scene = context.scene
        col = layout.column(align=True)
        col.prop(scene.render, "resolution_x", text="Resolution X")
        col.prop(scene.render, "resolution_y", text="Y")
        row = layout.row()
        row.operator("acon3d.camera_view", text="Camera View",
                     icon="RESTRICT_VIEW_OFF")
        row = layout.row()
#        row.operator("render.opengl", text="Quick Render", text_ctxt="*")
        row.operator("acon3d.render_quick", text="Quick Render", text_ctxt="*")

        if is_camera:
            row.operator("acon3d.render_full", text="Full Render")

        row = layout.row()
        row.operator("acon3d.render_line", text="Line Render")
        row.operator("acon3d.render_shadow", text="Shadow Render")


classes = (
    Acon3dCameraViewOperator,
    Acon3dRenderFullOperator,
    Acon3dRenderLineOperator,
    Acon3dRenderShadowOperator,
    Acon3dRenderQuickOperator,
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
