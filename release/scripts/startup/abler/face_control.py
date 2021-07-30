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
from .lib import materials


def toggleToonFace(self, context):
    node_group = bpy.data.node_groups['ACON_nodeGroup_combinedToon']
    toonFaceFactorValue = 0
    if bpy.context.scene.ToggleToonFace:
        toonFaceFactorValue = 1

    for node in node_group.nodes:
        if node.name == 'ACON_nodeGroup_toonFace':
            node.inputs[4].default_value = toonFaceFactorValue


def toggleTexture(self, context):
    node_group = bpy.data.node_groups['ACON_nodeGroup_combinedToon']
    textureFactorValue = 1
    if bpy.context.scene.ToggleTexture:
        textureFactorValue = 0

    for node in node_group.nodes:
        if node.name == 'ACON_node_textureMixFactor':
            node.inputs[0].default_value = textureFactorValue


def toggleShading(self, context):
    node_group = bpy.data.node_groups['ACON_nodeGroup_combinedToon']
    shadingFactorValue = 1
    if bpy.context.scene.ToggleShading:
        shadingFactorValue = 0

    for node in node_group.nodes:
        if node.name == 'ACON_node_shadeMixFactor':
            node.inputs[0].default_value = shadingFactorValue


def changeToonDepth(self, context):
    node_group = bpy.data.node_groups['ACON_nodeGroup_combinedToon']
    toonFaceInputs = None

    for node in node_group.nodes:
        if node.name == 'ACON_nodeGroup_toonFace':
            toonFaceInputs = node.inputs

    if bpy.context.scene.toon_depth.depth == "2 depth":
        toonFaceInputs[1].default_value = 0
    else:
        toonFaceInputs[1].default_value = 1


def changeMaterialType(self, context):

    try:
        material_slots = context.active_object.material_slots
        
        for mat_slot in material_slots:
            mat = mat_slot.material

            if not "ACON_nodeGroup_combinedToon" in mat.node_tree.nodes:
                continue

            materials.setMaterialParametersByType(mat)
    
    except:
        print("ACON Material Type change handler could not complete.")


class MaterialTypeEnumProperty(bpy.types.PropertyGroup):
    @classmethod
    def register(cls):
        bpy.types.Material.ACON_prop = bpy.props.PointerProperty(type=MaterialTypeEnumProperty)

    @classmethod
    def unregister(cls):
        del bpy.types.Material.ACON_prop

    type : bpy.props.EnumProperty(
        name="Type",
        description="Material Type",
        items = [
            ("Diffuse", "Diffuse", ""),
            ("Mirror", "Reflection", ""),
            ("Glow", "Emission", ""),
            ("Clear", "Transparent", "")
        ],
        update = changeMaterialType
    )


class MATERIAL_UL_List(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.use_property_split = True
        layout.use_property_decorate = False
        ob = data
        slot = item
        ma = slot.material

        if ma:

            layout.prop(ma, "name", text="", emboss=False, icon_value=icon)
            layout.prop(ma.ACON_prop, "type", text="")

            toonNode = ma.node_tree.nodes["ACON_nodeGroup_combinedToon"]
            
            if ma.ACON_prop.type == "Diffuse":
                layout.label(text="", translate=False)
            
            if ma.ACON_prop.type == "Mirror":
                layout.prop(toonNode.inputs[6], "default_value", text="")

            if ma.ACON_prop.type == "Glow":
                layout.prop(toonNode.inputs[5], "default_value", text="")

            if ma.ACON_prop.type == "Clear":
                layout.prop(toonNode.inputs[7], "default_value", text="")


class CloneMaterialOperator(bpy.types.Operator):
    bl_idname = "acon3d.clone_material"
    bl_label = "Clone Material"

    def execute(self, context):
        mat = context.object.active_material.copy()
        context.object.active_material = mat
        return {'FINISHED'}


class MaterialPanel(bpy.types.Panel):
    bl_parent_id = "ACON_PT_Face_Main"
    bl_idname = "ACON_PT_Material"
    bl_label = "Object Material"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        obj = context.object

        row = layout.row()
        row.template_list(
            "MATERIAL_UL_List",
            "",
            obj,
            "material_slots",
            obj,
            "active_material_index",
            rows=2,
        )
        
        row = layout.row()
        row.template_ID(obj, "active_material", new="acon3d.clone_material", unlink="")


class FaceDepthEnumProperty(bpy.types.PropertyGroup):
    @classmethod
    def register(cls):
        bpy.types.Scene.toon_depth = bpy.props.PointerProperty(type=FaceDepthEnumProperty)

    @classmethod
    def unregister(cls):
        del bpy.types.Scene.toon_depth

    depth : bpy.props.EnumProperty(
        name="Toon Color Depth",
        description="depth",
        items = [("2 depth", "2 depth", ""), ("3 depth", "3 depth", "")],
        update = changeToonDepth
    )


class Acon3dFacePanel(bpy.types.Panel):
    bl_idname = "ACON_PT_Face_Main"
    bl_label = "Face Control"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="NODE_MATERIAL")

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(bpy.context.scene, "ToggleTexture")
        row.prop(bpy.context.scene, "ToggleShading")
        return


class FaceSubPanel(bpy.types.Panel):
    bl_parent_id = "ACON_PT_Face_Main"
    bl_idname = "ACON_PT_Face_sub"
    bl_label = "Toon Style"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw_header(self, context):
        layout = self.layout
        layout.prop(bpy.context.scene, "ToggleToonFace", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        
        if bpy.context.scene.ToggleToonFace:

            node_group = bpy.data.node_groups['ACON_nodeGroup_combinedToon']
            toonFaceInputs = None

            for node in node_group.nodes:
                
                if node.name == 'ACON_nodeGroup_toonFace':
                    toonFaceInputs = node.inputs
            
            col = layout.column()
            col.prop(bpy.context.scene.toon_depth, "depth")
            if toonFaceInputs is not None:
                if bpy.context.scene.toon_depth.depth == "2 depth":
                    col.prop(toonFaceInputs[2], "default_value", text="Brightness", slider=True)
                else:
                    col.prop(toonFaceInputs[2], "default_value", text="Brightness 1", slider=True)
                    col.prop(toonFaceInputs[3], "default_value", text="Brightness 2", slider=True)


class Acon3dBloomPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_parent_id = "ACON_PT_Face_Main"
    bl_idname = "ACON3D_BLOOM_PT_Main"
    bl_label = "Bloom"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_EEVEE'}
    
    def draw_header(self, context):
        scene = context.scene
        props = scene.eevee
        self.layout.prop(props, "use_bloom", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        scene = context.scene
        props = scene.eevee

        layout.active = props.use_bloom
        col = layout.column()
        col.prop(props, "bloom_threshold")
        col.prop(props, "bloom_knee")
        col.prop(props, "bloom_radius")
        col.prop(props, "bloom_color")
        col.prop(props, "bloom_intensity")
        col.prop(props, "bloom_clamp")


classes = (
    CloneMaterialOperator,
    FaceDepthEnumProperty,
    Acon3dFacePanel,
    FaceSubPanel,
    Acon3dBloomPanel,
    MaterialTypeEnumProperty,
    MATERIAL_UL_List,
    MaterialPanel,
)


def register():
    from bpy.utils import register_class

    bpy.types.Scene.ToggleToonFace = bpy.props.BoolProperty(
        name="Toon Style",
        default=True,
        update=toggleToonFace
    )

    bpy.types.Scene.ToggleTexture = bpy.props.BoolProperty(
        name="Texture",
        default=True,
        update=toggleTexture
    )
    
    bpy.types.Scene.ToggleShading = bpy.props.BoolProperty(
        name="Shading",
        default=True,
        update=toggleShading
    )

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)