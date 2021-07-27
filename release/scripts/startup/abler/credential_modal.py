import bpy
from bpy.app.handlers import persistent
import requests, webbrowser, pickle, os


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

    login_status : bpy.props.StringProperty(
        name="Login Status",
        description="Login Status",
    )


class AconModalOperator(bpy.types.Operator):
    bl_idname = "acon3d.modal_operator"
    bl_label = "Login Modal Operator"

    def execute(self, context):
        return {'FINISHED'}

    def modal(self, context, event):
        if context.scene.ACON_prop.login_status == 'SUCCESS':
            return {'FINISHED'}

        if event.type == 'LEFTMOUSE':
            bpy.ops.wm.splash('INVOKE_DEFAULT')

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        bpy.ops.wm.splash('INVOKE_DEFAULT')
        return {'RUNNING_MODAL'}


def requestLogin():
    try:
        path = os.getcwd()
        path_cookiesFolder = os.path.join(path, 'cookies')
        path_cookiesFile = os.path.join(path_cookiesFolder, 'acon3d_session')

        prop = bpy.context.scene.ACON_prop

        response = requests.post(
            'https://api-v2.acon3d.com/auth/acon3d/signin',
            data = {
                'account': prop.username,
                'password': prop.password
            }
        )

        if response.status_code == 200:
            prop.login_status = 'SUCCESS'
            cookiesFile = open(path_cookiesFile, "wb")
            pickle.dump(response.cookies, cookiesFile)
            cookiesFile.close()
        else: prop.login_status = 'FAIL'

        prop.username = ""
        prop.password = ""

        window = bpy.context.window
        width = window.width
        height = window.height
        window.cursor_warp(width / 2, (height / 2))
        bpy.app.timers.register(moveMouse, first_interval=0.1)

    except: print("Login request has failed.")


def moveMouse():
    window = bpy.context.window
    width = window.width
    height = window.height
    window.cursor_warp(width / 2, (height / 2) - 100)


class AconLoginOperator(bpy.types.Operator):
    bl_idname = "acon3d.login"
    bl_label = "Simple Modal Operator"

    def execute(self, context):
        bpy.context.scene.ACON_prop.login_status = 'LOADING'
        bpy.app.timers.register(requestLogin, first_interval=0.1)
        return {'FINISHED'}


class AconAnchorOperator(bpy.types.Operator):
    bl_idname = "acon3d.anchor"
    bl_label = "Simple Modal Operator"

    href : bpy.props.StringProperty(
        name="href",
        description="href"
    )

    def execute(self, context):
        webbrowser.open(self.href)

        return {'FINISHED'}


@persistent
def open_credential_modal(dummy):
    prefs = bpy.context.preferences
    prefs.view.show_splash = False
    prop = bpy.context.scene.ACON_prop
    prop.login_status = 'IDLE'

    try:
        path = os.getcwd()
        path_cookiesFolder = os.path.join(path, 'cookies')
        path_cookiesFile = os.path.join(path_cookiesFolder, 'acon3d_session')

        if not os.path.isdir(path_cookiesFolder):
            os.mkdir(path_cookiesFolder)
        
        if not os.path.exists(path_cookiesFile):
            raise

        cookiesFile = open(path_cookiesFile, "rb")
        cookies = pickle.load(cookiesFile)
        cookiesFile.close()
        response = requests.get(
            'https://api-v2.acon3d.com/auth/acon3d/refresh',
            cookies = cookies
        )

        responseData = response.json()
        token = responseData['accessToken']

        if token: prop.login_status = 'SUCCESS'

    except: print("Failed to load cookies")
    
    bpy.ops.acon3d.modal_operator('INVOKE_DEFAULT')


classes = (
    AconProperty,
    AconModalOperator,
    AconLoginOperator,
    AconAnchorOperator,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.app.handlers.load_post.append(open_credential_modal)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    bpy.app.handlers.load_post.remove(open_credential_modal)