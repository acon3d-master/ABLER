import bpy


def switchToRendredView():
    bpy.context.scene.render.engine = "BLENDER_EEVEE"
    for area in bpy.context.screen.areas: 
        if area.type == 'VIEW_3D':
            for space in area.spaces: 
                if space.type == 'VIEW_3D':
                    space.shading.type = 'RENDERED'


def makeSureCameraExists():
    # early out if scene camera exists
    if bpy.context.scene.camera: return

    # get camera to set to context
    camera_object = bpy.data.objects.get("View_Camera")

    # create camera if View_Camera does not exist
    if not camera_object or not camera_object.type == "CAMERA":
        camera_data = bpy.data.cameras.new("View_Camera")
        camera_object = bpy.data.objects.new("View_Camera", camera_data)
        camera_object.location[0] = 7.35889
        camera_object.location[1] = -6.92579
        camera_object.location[2] = 4.9583
        camera_object.rotation_mode = "XYZ"
        camera_object.rotation_euler[0] = 1.109319
        camera_object.rotation_euler[1] = 0
        camera_object.rotation_euler[2] = 0.814928
        bpy.context.scene.collection.objects.link(camera_object)

    # set context camera
    bpy.context.scene.camera = camera_object


# turn on camera view (set viewport to the current selected camera's view)
def turnOnCameraView(center_camera=True):
    makeSureCameraExists()
    # turn on camera view in the selected context(view pane)
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces[0].region_3d.view_perspective = 'CAMERA'
            area.spaces[0].lock_camera = True
            if center_camera:
                override = {}
                override['area'] = area
                bpy.ops.view3d.view_center_camera(override)
            break


def turnOffCameraView():
    # turn onff camera view in the selected context(view pane)
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces[0].region_3d.view_perspective = 'PERSP'
            break


def setupSharpShadow():
    bpy.context.scene.eevee.shadow_cube_size = "4096"
    bpy.context.scene.eevee.shadow_cascade_size = "4096"
    bpy.context.scene.eevee.use_soft_shadows = True

    if "ACON_sun" in bpy.data.objects:
        bpy.data.objects["ACON_sun"].data.angle = 0
