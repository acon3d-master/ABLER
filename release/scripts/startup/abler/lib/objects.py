import bpy
from . import cameras


def toggleConstraintToCamera(self, context):
    
    cameras.makeSureCameraExists()

    obj = context.object
    setConstraintToCameraByObject(obj, context)


def setConstraintToCameraByObject(obj, context=None):

    if not context: context = bpy.context

    camera = context.scene.camera
    camera.rotation_mode == "XYZ"
    const = obj.constraints.get("ACON_const_copyRotation")
    
    if obj.ACON_prop.constraint_to_camera_rotation_z:
    
        if not const:
            const = obj.constraints.new(type="COPY_ROTATION")
            const.name = "ACON_const_copyRotation"
            const.mix_mode = 'BEFORE'
            const.use_x = False
            const.use_y = False
            const.use_z = True

        const.target = context.scene.camera
        const.mute = False
        obj.rotation_mode == "XYZ"
        obj.rotation_euler.z = 0

    elif const:

        obj.rotation_euler.z = camera.rotation_euler.z
        const.mute = True