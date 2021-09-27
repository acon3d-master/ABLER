import bpy
from . import cameras


def toggleConstraintToCamera(self, context):

    cameras.makeSureCameraExists()

    obj = context.object
    setConstraintToCameraByObject(obj, context)


def setConstraintToCameraByObject(obj, context=None):

    if not context:
        context = bpy.context

    const = obj.constraints.get("ACON_const_copyRotation")

    if obj.ACON_prop.constraint_to_camera_rotation_z:

        if not const:
            const = obj.constraints.new(type="COPY_ROTATION")
            const.name = "ACON_const_copyRotation"
            const.use_x = False
            const.use_y = False
            const.use_z = True

        const.target = context.scene.camera
        const.mute = False

    elif const:

        const.mute = True
