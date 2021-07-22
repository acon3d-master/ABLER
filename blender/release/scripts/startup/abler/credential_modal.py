import bpy
from bpy.app.handlers import persistent


class AconProperty(bpy.types.PropertyGroup):
    @classmethod
    def register(cls):
        bpy.types.Scene.ACON_prop = bpy.props.PointerProperty(type=AconProperty)

    @classmethod
    def unregister(cls):
        del bpy.types.Scene.ACON_prop

    username : bpy.props.StringProperty(
        name="Username",
        description="Username"
    )

    password : bpy.props.StringProperty(
        name="Password",
        description="Password",
        subtype="PASSWORD"
    )

    logged_in : bpy.props.BoolProperty(
        name="Logged In",
    )


class AconModalOperator(bpy.types.Operator):
    bl_idname = "acon3d.modal_operator"
    bl_label = "Simple Modal Operator"

    def execute(self, context):
        return {'FINISHED'}

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE':
            bpy.ops.wm.splash('INVOKE_DEFAULT')
        
        if context.scene.ACON_prop.logged_in:
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        bpy.ops.wm.splash('INVOKE_DEFAULT')
        return {'RUNNING_MODAL'}


@persistent
def open_credential_modal(dummy):
    prefs = bpy.context.preferences
    prefs.view.show_splash = False
    bpy.context.scene.ACON_prop.logged_in = False
    bpy.ops.acon3d.modal_operator('INVOKE_DEFAULT')


classes = (
    AconProperty,
    AconModalOperator,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.app.handlers.load_post.append(open_credential_modal)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    bpy.app.handlers.load_post.remove(open_credential_modal)