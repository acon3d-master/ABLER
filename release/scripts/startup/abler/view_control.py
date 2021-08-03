bl_info = {
    "name": "ACON3D Panel",
    "description": "",
    "author": "hoie@acon3d.com",
    "version": (0, 0, 1),
    "blender": (2, 93, 0),
    "location": "",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "ACON3D"
}
import bpy

from .lib import cameras


def genCameraName(name, i=1):
    found = None
    combinedName = name + str(i)

    collection = bpy.data.collections.get('ACON_col_cameras')

    if collection:
        for object in collection.objects:
            if object.name == combinedName:
                found = True
                break

    if found: return genCameraName(name, i+1)
    else: return name + str(i)



class CreateCameraOperator(bpy.types.Operator):
    """Create new camera with current view"""
    bl_idname = "acon3d.create_camera"
    bl_label = "Create New Camera"
    bl_translation_context = "*"

    def execute(self, context):
        cameras.makeSureCameraExists()
        
        cameraName = genCameraName("ACON_Camera_")

        # duplicate camera
        viewCameraObject = context.scene.camera
        camera_object = viewCameraObject.copy()
        camera_object.name = cameraName
        camera_object.hide_viewport = True
        
        # add camera to designated collection (create one if not exists)
        collection = bpy.data.collections.get("ACON_col_cameras")
        if not collection:
            collection = bpy.data.collections.new("ACON_col_cameras")
            context.scene.collection.children.link(collection)
            layer_collection = context.view_layer.layer_collection
            layer_collection.children.get("ACON_col_cameras").exclude = True
        collection.objects.link(camera_object)

        # select created camera in custom view ui
        context.scene.ACON_prop.view = camera_object.name
        return {'FINISHED'}


class UpdateCustomCameraOperator(bpy.types.Operator):
    """Move view to user-created camera"""
    bl_idname = "acon3d.update_custom_camera"
    bl_label = "Update"
    bl_translation_context = "*"

    def execute(self, context):
        cameras.makeSureCameraExists()
        viewCamera = context.scene.camera
        targetCamera = bpy.data.objects[context.scene.ACON_prop.view]
        targetCamera.location[0] = viewCamera.location[0]
        targetCamera.location[1] = viewCamera.location[1]
        targetCamera.location[2] = viewCamera.location[2]
        targetCamera.rotation_mode = viewCamera.rotation_mode
        targetCamera.rotation_euler[0] = viewCamera.rotation_euler[0]
        targetCamera.rotation_euler[1] = viewCamera.rotation_euler[1]
        targetCamera.rotation_euler[2] = viewCamera.rotation_euler[2]
        targetCamera.scale[0] = viewCamera.scale[0]
        targetCamera.scale[1] = viewCamera.scale[1]
        targetCamera.scale[2] = viewCamera.scale[2]
        return {'FINISHED'}


class DeleteCameraOperator(bpy.types.Operator):
    """Delete selected user-created camera"""
    bl_idname = "acon3d.delete_camera"
    bl_label = "Delete"
    bl_translation_context = "*"

    def execute(self, context):
        currentCameraName = context.scene.ACON_prop.view
        camera = bpy.data.objects[currentCameraName]
        bpy.data.objects.remove(camera)
        
        return {'FINISHED'}


class Acon3dViewPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_idname = "ACON3D_PT_view"
    bl_label = "Camera Control"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="CAMERA_DATA")

    def draw(self, context):
        return


class Acon3dNavigatePanel(bpy.types.Panel):
    bl_label = "Navigate"
    bl_idname = "ACON3D_PT_navigate"
    bl_parent_id = "ACON3D_PT_view"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.operator('view3d.walk', text='Fly (shift + `)', text_ctxt="*")


class Acon3dCameraPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_parent_id = "ACON3D_PT_view"
    bl_idname = "ACON3D_PT_camera"
    bl_label = "Cameras"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        row = layout.row()
        row.scale_y = 1.0
        row.operator("acon3d.create_camera", text="Create New Camera")

        scene = context.scene
        collection = bpy.data.collections.get('ACON_col_cameras')
        
        if collection is not None and len(collection.objects):
            row = layout.row()
            row.prop(scene.ACON_prop, "view")

            row = layout.row()
            row.operator("acon3d.update_custom_camera", text="Update")
            row.operator("acon3d.delete_camera", text="Delete")
        
        if bpy.context.scene.camera is not None:
            cam = bpy.context.scene.camera.data
            row = layout.row()
            row.prop(cam, "lens")


def scene_mychosenobject_poll(self, object):
    return object.type == 'CAMERA'


class Acon3dDOFPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_parent_id = "ACON3D_PT_view"
    bl_idname = "ACON3D_PT_dof"
    bl_label = "Depth of Field"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw_header(self, context):
        if bpy.context.scene.camera is not None:
            cam = bpy.context.scene.camera.data
            dof = cam.dof
            self.layout.prop(dof, "use_dof", text="")
        else:
            self.layout.active = False

    def draw(self, context):
        if bpy.context.scene.camera is not None:
            layout = self.layout
            layout.use_property_split = True
            layout.use_property_decorate = False  # No animation.

            cam = bpy.context.scene.camera.data
            dof = cam.dof
            layout.active = dof.use_dof

            col = layout.column()
            col.prop(dof, "focus_object", text="Focus on Object")
            sub = col.column()
            sub.active = (dof.focus_object is None)
            sub.prop(dof, "focus_distance", text="Focus Distance")
            sub = col.column()
            sub.active = (dof.focus_object is None)
            sub.prop(dof, "aperture_fstop", text="F-stop")


class RemoveBackgroundOperator(bpy.types.Operator):
    bl_idname = "acon3d.background_image_remove"
    bl_label = "Remove Background Image"
    bl_translation_context = "*"

    index: bpy.props.IntProperty(
        name = 'Index',
        default = 0
        )

    def execute(self, context):
        image = bpy.context.scene.camera.data.background_images[self.index]
        bpy.context.scene.camera.data.background_images.remove(image)
        return {'FINISHED'}


class Acon3dBackgroundPanel(bpy.types.Panel):
    bl_parent_id = "ACON3D_PT_view"
    bl_idname = "ACON3D_PT_background"
    bl_label = "Background Images"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        if bpy.context.scene.camera is not None:
            cam = bpy.context.scene.camera.data
            self.layout.prop(cam, "show_background_images", text="")
        else:
            self.layout.active = False

    def draw(self, context):
        layout = self.layout
        layout.operator('view3d.background_image_add', text="Add Image", text_ctxt="*")

        camObj = bpy.context.scene.camera
        active = camObj and camObj.data.show_background_images

        layout.active = active
        layout.use_property_split = True
        layout.use_property_decorate = False
        
        if bpy.context.scene.camera is not None:
            cam = bpy.context.scene.camera.data
            
            for i, bg in enumerate(cam.background_images):
                box = layout.box()
                row = box.row(align=True)
                row.prop(bg, "show_expanded", text="", emboss=False)
                
                if bg.source == 'IMAGE' and bg.image:
                    row.prop(bg.image, "name", text="", emboss=False)
                elif bg.source == 'MOVIE_CLIP' and bg.clip:
                    row.prop(bg.clip, "name", text="", emboss=False)
                elif bg.source and bg.use_camera_clip:
                    row.label(text="Active Clip")
                else:
                    row.label(text="Not Set")
                    
                row.operator("acon3d.background_image_remove", text="Remove Background Image", emboss=False, icon='X').index = i

                if bg.show_expanded:
                    row = box.row()
                    row.prop(bg, "source", expand=True)
                    row = box.row()
                    row.template_ID(bg, "image", new="image.open")
                    row = box.row()
                    row.prop(bg, "alpha")
                    row = box.row()
                    row.prop(bg, "display_depth", text="Placement", expand=True)
                    row = box.row()
                    row.prop(bg, "frame_method", expand=True)
                    row = box.row()
                    row.prop(bg, "offset")
                    row = box.row()
                    row.prop(bg, "rotation")
                    row = box.row()
                    row.prop(bg, "scale")
                    row = box.row(heading="Flip")
                    row.prop(bg, "use_flip_x", text="X")
                    row.prop(bg, "use_flip_y", text="Y")


classes = (
    Acon3dViewPanel,
    Acon3dNavigatePanel,
    Acon3dCameraPanel,
    CreateCameraOperator,
    UpdateCustomCameraOperator,
    DeleteCameraOperator,
    Acon3dDOFPanel,
    RemoveBackgroundOperator,
    Acon3dBackgroundPanel,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)