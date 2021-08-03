import bpy
from .lib import cameras, shadow
from .lib.materials import materials_handler


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
        update=materials_handler.toggleToonEdge
    )

    toggle_toon_face : bpy.props.BoolProperty(
        name="Toon Style",
        default=True,
        update=materials_handler.toggleToonFace
    )

    toggle_texture : bpy.props.BoolProperty(
        name="Texture",
        default=True,
        update=materials_handler.toggleTexture
    )

    toggle_shading : bpy.props.BoolProperty(
        name="Shading",
        default=True,
        update=materials_handler.toggleShading
    )

    toon_shading_depth : bpy.props.EnumProperty(
        name="Toon Color Depth",
        description="depth",
        items=[("2", "2 depth", ""), ("3", "3 depth", "")],
        update=materials_handler.changeToonDepth
    )

    view : bpy.props.EnumProperty(
        name="View",
        description="view",
        items=cameras.add_view_items_from_collection,
        update=cameras.goToCustomCamera
    )

    sun_rotation_x : bpy.props.FloatProperty(
        name="sun_rotation_x",
        subtype="ANGLE",
        unit="ROTATION",
        update=shadow.changeSunRotation
    )

    sun_rotation_y : bpy.props.FloatProperty(
        name="sun_rotation_y",
        subtype="ANGLE",
        unit="ROTATION",
        update=shadow.changeSunRotation
    )

    sun_rotation_z : bpy.props.FloatProperty(
        name="sun_rotation_z",
        subtype="ANGLE",
        unit="ROTATION",
        update=shadow.changeSunRotation
    )

    image_adjust_brightness : bpy.props.FloatProperty(
        name="brightness",
        default=0,
        min=-1,
        max=1,
        update=materials_handler.changeImageAdjustBrightness
    )

    image_adjust_contrast : bpy.props.FloatProperty(
        name="contrast",
        default=0,
        min=-1,
        max=1,
        update=materials_handler.changeImageAdjustContrast
    )

    image_adjust_color_r : bpy.props.FloatProperty(
        name="image_adjust_color_r",
        default=1,
        min=0,
        max=2,
        step=1,
        update=materials_handler.changeImageAdjustColor
    )

    image_adjust_color_g : bpy.props.FloatProperty(
        name="image_adjust_color_g",
        default=1,
        min=0,
        max=2,
        step=1,
        update=materials_handler.changeImageAdjustColor
    )

    image_adjust_color_b : bpy.props.FloatProperty(
        name="image_adjust_color_b",
        default=1,
        min=0,
        max=2,
        step=1,
        update=materials_handler.changeImageAdjustColor
    )


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
        update=materials_handler.changeMaterialType
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