import bpy, math


def changeSunRotation(self, context):
    obj = bpy.data.objects.get("ACON_sun")
    if not obj: return

    prop = context.scene.ACON_prop

    obj.rotation_euler.x = math.radians(90) - prop.sun_rotation_x
    obj.rotation_euler.y = 0
    obj.rotation_euler.z = prop.sun_rotation_z


def setupSharpShadow():
    bpy.context.scene.eevee.shadow_cube_size = "4096"
    bpy.context.scene.eevee.shadow_cascade_size = "4096"
    bpy.context.scene.eevee.use_soft_shadows = True

    if "ACON_sun" in bpy.data.objects:
        bpy.data.objects["ACON_sun"].data.angle = 0
