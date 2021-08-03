import bpy
from .lib import materials, common


def toggleToonEdge(self, context):
    node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
    if not node_group: return

    toonEdgeFactorValue = 0
    if context.scene.ACON_prop.toggle_toon_edge:
        toonEdgeFactorValue = 1

    node = node_group.nodes.get('ACON_node_toonEdgeFactor')
    if node: node.inputs[0].default_value = toonEdgeFactorValue


def toggleToonFace(self, context):
    node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
    if not node_group: return

    toonFaceFactorValue = 0
    if context.scene.ACON_prop.toggle_toon_face:
        toonFaceFactorValue = 1

    node = node_group.nodes.get('ACON_nodeGroup_toonFace')
    if node: node.inputs[4].default_value = toonFaceFactorValue


def toggleTexture(self, context):
    node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
    if not node_group: return

    textureFactorValue = 1
    if context.scene.ACON_prop.toggle_texture:
        textureFactorValue = 0

    node = node_group.nodes.get('ACON_node_textureMixFactor')
    if node: node.inputs[0].default_value = textureFactorValue


def toggleShading(self, context):
    node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
    if not node_group: return

    shadingFactorValue = 1
    if context.scene.ACON_prop.toggle_shading:
        shadingFactorValue = 0

    node = node_group.nodes.get('ACON_node_shadeMixFactor')
    if node: node.inputs[0].default_value = shadingFactorValue


def changeToonDepth(self, context):
    node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
    if not node_group: return

    toonFaceFactorValue = 1
    if context.scene.ACON_prop.toon_shading_depth == "2":
        toonFaceFactorValue = 0

    node = node_group.nodes.get('ACON_nodeGroup_toonFace')
    if node: node.inputs[1].default_value = toonFaceFactorValue


def add_view_items_from_collection(self, context):
    items = []
    collection = bpy.data.collections.get('ACON_col_cameras')

    if collection:
        for item in collection.objects:
            items.append((item.name, item.name, ""))

    return items


def goToCustomCamera(self, context):
    common.makeSureCameraExists()
    viewCamera = context.scene.camera
    targetCamera = bpy.data.objects[context.scene.ACON_prop.view]
    viewCamera.location[0] = targetCamera.location[0]
    viewCamera.location[1] = targetCamera.location[1]
    viewCamera.location[2] = targetCamera.location[2]
    viewCamera.rotation_mode = targetCamera.rotation_mode
    viewCamera.rotation_euler[0] = targetCamera.rotation_euler[0]
    viewCamera.rotation_euler[1] = targetCamera.rotation_euler[1]
    viewCamera.rotation_euler[2] = targetCamera.rotation_euler[2]
    viewCamera.scale[0] = targetCamera.scale[0]
    viewCamera.scale[1] = targetCamera.scale[1]
    viewCamera.scale[2] = targetCamera.scale[2]
    common.turnOnCameraView()


def changeSunRotation(self, context):
    obj = bpy.data.objects.get("ACON_sun")
    if not obj: return

    prop = context.scene.ACON_prop

    obj.rotation_euler.x = prop.sun_rotation_x
    obj.rotation_euler.y = prop.sun_rotation_y
    obj.rotation_euler.z = prop.sun_rotation_z


def changeImageAdjustBrightness(self, context):
    
    node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
    if not node_group: return

    brightContrast = node_group.nodes.get('ACON_node_brightContrast')
    if not brightContrast: return

    inputs = brightContrast.inputs

    prop = context.scene.ACON_prop
    value = prop.image_adjust_brightness

    inputs[1].default_value = value


def changeImageAdjustContrast(self, context):
    
    node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
    if not node_group: return

    brightContrast = node_group.nodes.get('ACON_node_brightContrast')
    if not brightContrast: return

    inputs = brightContrast.inputs

    prop = context.scene.ACON_prop
    value = prop.image_adjust_contrast

    inputs[2].default_value = value


def changeImageAdjustColor(self, context):
    
    node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
    if not node_group: return

    brightContrast = node_group.nodes.get('ACON_node_colorBalance')
    if not brightContrast: return

    inputs = brightContrast.inputs

    prop = context.scene.ACON_prop
    r = prop.image_adjust_color_r
    g = prop.image_adjust_color_g
    b = prop.image_adjust_color_b
    color = (r, g, b, 1)

    inputs[2].default_value = color


class AconSceneProperty(bpy.types.PropertyGroup):
    @classmethod
    def register(cls):
        bpy.types.Scene.ACON_prop = bpy.props.PointerProperty(type=AconSceneProperty)

    @classmethod
    def unregister(cls):
        del bpy.types.Scene.ACON_prop

    toggle_toon_edge : bpy.props.BoolProperty(
        name="Toon Style",
        default=True,
        update=toggleToonEdge
    )

    toggle_toon_face : bpy.props.BoolProperty(
        name="Toon Style",
        default=True,
        update=toggleToonFace
    )

    toggle_texture : bpy.props.BoolProperty(
        name="Texture",
        default=True,
        update=toggleTexture
    )

    toggle_shading : bpy.props.BoolProperty(
        name="Shading",
        default=True,
        update=toggleShading
    )

    toon_shading_depth : bpy.props.EnumProperty(
        name="Toon Color Depth",
        description="depth",
        items=[("2", "2 depth", ""), ("3", "3 depth", "")],
        update=changeToonDepth
    )

    view : bpy.props.EnumProperty(
        name="View",
        description="view",
        items=add_view_items_from_collection,
        update=goToCustomCamera
    )

    sun_rotation_x : bpy.props.FloatProperty(
        name="sun_rotation_x",
        subtype="ANGLE",
        unit="ROTATION",
        update=changeSunRotation
    )

    sun_rotation_y : bpy.props.FloatProperty(
        name="sun_rotation_y",
        subtype="ANGLE",
        unit="ROTATION",
        update=changeSunRotation
    )

    sun_rotation_z : bpy.props.FloatProperty(
        name="sun_rotation_z",
        subtype="ANGLE",
        unit="ROTATION",
        update=changeSunRotation
    )

    image_adjust_brightness : bpy.props.FloatProperty(
        name="brightness",
        default=0,
        min=-1,
        max=1,
        update=changeImageAdjustBrightness
    )

    image_adjust_contrast : bpy.props.FloatProperty(
        name="contrast",
        default=0,
        min=-1,
        max=1,
        update=changeImageAdjustContrast
    )

    image_adjust_color_r : bpy.props.FloatProperty(
        name="image_adjust_color_r",
        default=1,
        min=0,
        max=1,
        update=changeImageAdjustColor
    )

    image_adjust_color_g : bpy.props.FloatProperty(
        name="image_adjust_color_g",
        default=1,
        min=0,
        max=1,
        step=1,
        update=changeImageAdjustColor
    )

    image_adjust_color_b : bpy.props.FloatProperty(
        name="image_adjust_color_b",
        default=1,
        min=0,
        max=1,
        step=1,
        update=changeImageAdjustColor
    )


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


class AconMaterialProperty(bpy.types.PropertyGroup):
    @classmethod
    def register(cls):
        bpy.types.Material.ACON_prop = bpy.props.PointerProperty(type=AconMaterialProperty)

    @classmethod
    def unregister(cls):
        del bpy.types.Material.ACON_prop

    type : bpy.props.EnumProperty(
        name="Type",
        description="Material Type",
        items=[
            ("Diffuse", "Diffuse", ""),
            ("Mirror", "Reflection", ""),
            ("Glow", "Emission", ""),
            ("Clear", "Transparent", "")
        ],
        update=changeMaterialType
    )


class AconMeshProperty(bpy.types.PropertyGroup):
    @classmethod
    def register(cls):
        bpy.types.Mesh.ACON_prop = bpy.props.PointerProperty(type=AconMeshProperty)

    @classmethod
    def unregister(cls):
        del bpy.types.Mesh.ACON_prop

    username : bpy.props.StringProperty(
        name="Username",
        description="Username"
    )

    password : bpy.props.StringProperty(
        name="Password",
        description="Password",
        subtype="PASSWORD"
    )

    login_status : bpy.props.StringProperty(
        name="Login Status",
        description="Login Status",
    )


classes = (
    AconSceneProperty,
    AconMaterialProperty,
    AconMeshProperty,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)