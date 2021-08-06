import bpy
from bpy.app.handlers import persistent
import requests, webbrowser, pickle, os


class AconModalOperator(bpy.types.Operator):
    bl_idname = "acon3d.modal_operator"
    bl_label = "Login Modal Operator"

    def execute(self, context):
        return {'FINISHED'}

    def modal(self, context, event):
        userInfo = bpy.data.meshes.get("ACON_userInfo")

        if userInfo and userInfo.ACON_prop.login_status == 'SUCCESS':
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

        userInfo = bpy.data.meshes.get("ACON_userInfo")
        prop = userInfo.ACON_prop

        cookies_godo = ""
        response_godo = None

        try:
            response_godo = requests.post(
                'https://www.acon3d.com/api/login.php',
                data = {
                    'loginId': prop.username,
                    'loginPwd': prop.password    
                }
            )
        except:
            response_godo = None

        try:
            success_msg = response_godo.json()['message']
            if success_msg != "success":
                response_godo = None
        except:
            response_godo = None

        if response_godo is not None:
            cookies_godo = response_godo.cookies
        response = requests.post(
            'https://api-v2.acon3d.com/auth/acon3d/signin',
            data = {
                'account': prop.username,
                'password': prop.password
            },
            cookies=cookies_godo
        )

        cookie_final = response.cookies
        if response_godo is not None:
            cookie_final = requests.cookies.merge_cookies(cookies_godo, response.cookies)
        
        if response.status_code == 200:
            prop.login_status = 'SUCCESS'
            cookiesFile = open(path_cookiesFile, "wb")
            pickle.dump(cookie_final, cookiesFile)
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
    window.cursor_warp(width / 2, (height / 2) - 150)


class AconLoginOperator(bpy.types.Operator):
    bl_idname = "acon3d.login"
    bl_label = "Login"
    bl_translation_context = "*"

    def execute(self, context):
        userInfo = bpy.data.meshes.get("ACON_userInfo")
        userInfo.ACON_prop.login_status = 'LOADING'
        bpy.app.timers.register(requestLogin, first_interval=0.1)
        return {'FINISHED'}


class AconAnchorOperator(bpy.types.Operator):
    bl_idname = "acon3d.anchor"
    bl_label = "Go to link"
    bl_translation_context = "*"

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

    userInfo = bpy.data.meshes.new("ACON_userInfo")
    userInfo.ACON_prop.login_status = 'IDLE'

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

        if token: userInfo.ACON_prop.login_status = 'SUCCESS'

    except: print("Failed to load cookies")
    
    bpy.ops.acon3d.modal_operator('INVOKE_DEFAULT')


classes = (
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