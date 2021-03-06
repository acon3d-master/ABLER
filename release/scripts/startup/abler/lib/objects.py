import bpy
from . import cameras


def toggleConstraintToCamera(self, context):

    cameras.makeSureCameraExists()

    obj = context.object
    setConstraintToCameraByObject(obj, context)


def setConstraintToCameraByObject(obj, context=None):

    if not context:
        context = bpy.context

    look_at_me = obj.ACON_prop.constraint_to_camera_rotation_z

    for obj in context.selected_objects:

        prop = obj.ACON_prop
        const = obj.constraints.get("ACON_const_copyRotation")

        if look_at_me:

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

        if prop.constraint_to_camera_rotation_z != look_at_me:
            prop.constraint_to_camera_rotation_z = look_at_me


def step(edge0: tuple[float], edge1: tuple[float], x: float) -> tuple[float]:
    return tuple(edge0[i] + ((edge1[i] - edge0[i]) * x) for i in [0, 1, 2])


def toggleUseState(self, context):

    use_state = context.object.ACON_prop.use_state

    for obj in context.selected_objects:

        prop = obj.ACON_prop

        if use_state:

            if obj == context.object or not prop.use_state:

                for att in ["location", "rotation_euler", "scale"]:

                    vector = getattr(obj, att)
                    setattr(prop.state_begin, att, vector)
                    setattr(prop.state_end, att, vector)

        elif obj == context.object or prop.use_state:

            for att in ["location", "rotation_euler", "scale"]:

                vector = getattr(prop.state_begin, att)
                setattr(obj, att, vector)
                setattr(prop.state_end, att, vector)

        if prop.use_state != use_state:
            prop.use_state = use_state


def moveState(self, context):

    state_slider = context.object.ACON_prop.state_slider

    for obj in context.selected_objects:

        prop = obj.ACON_prop

        if not prop.use_state:
            continue

        for att in ["location", "rotation_euler", "scale"]:

            vector_begin = getattr(prop.state_begin, att)
            vector_end = getattr(prop.state_end, att)
            vector_mid = step(vector_begin, vector_end, state_slider)

            setattr(obj, att, vector_mid)

        if prop.state_slider != state_slider:
            prop.state_slider = state_slider
