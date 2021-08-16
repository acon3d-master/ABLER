bl_info = {
    "name": "ACON3D Panel",
    "description": "",
    "author": "sdk@acon3d.com",
    "version": (0, 0, 1),
    "blender": (2, 93, 0),
    "location": "",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "ACON3D"
}
import bpy
from bpy.app.handlers import persistent
from .lib import layers


@persistent
def load_handler(dummy):
    layers.subscribeToGroupedObjects()


class Acon3dCreateGroupOperator(bpy.types.Operator):
    """Create Group"""
    bl_idname = "acon3d.create_group"
    bl_label = "Create Group"
    bl_translation_context = "*"

    def execute(self, context):
        # add camera to designated collection (create one if not exists)
        collection = bpy.data.collections.get("Groups")
        if not collection:
            collection = bpy.data.collections.new("Groups")
            context.scene.collection.children.link(collection)
            layer_collection = context.view_layer.layer_collection
            layer_collection.children.get("Groups").exclude = True

        col_group = bpy.data.collections.new("ACON_group")
        collection.children.link(col_group)
        for obj in context.selected_objects:
            col_group.objects.link(obj)

        return {'FINISHED'}


class Acon3dExplodeGroupOperator(bpy.types.Operator):
    """Explode Group"""
    bl_idname = "acon3d.explode_group"
    bl_label = "Explode Group"
    bl_translation_context = "*"

    def execute(self, context):
        col_group = bpy.data.collections.get("Groups")

        found_col = None
        for col in col_group.children:
            not_this_col = False
            for obj in context.selected_objects:
                if not col.all_objects.get(obj.name):
                    not_this_col = True
                    break
            if not_this_col: continue
            else:
                found_col = col
                break
        
        bpy.data.collections.remove(found_col)

        return {'FINISHED'}


class Acon3dLayerPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_idname = "ACON3D_PT_Layer"
    bl_label = "Layer"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="OUTLINER")

    def _draw_collection(
        self,
        layout,
        view_layer,
        use_local_collections,
        collection,
        index
    ):
        findex = 0
        for child in collection.children:
            index += 1

            icon = 'OUTLINER_COLLECTION'

            row = layout.row()
            row.use_property_decorate = False
            sub = row.split(factor=0.98)
            subrow = sub.row()
            subrow.alignment = 'LEFT'
            subrow.label(text=child.name, icon=icon)

            sub = row.split()
            subrow = sub.row(align=True)
            subrow.alignment = 'RIGHT'
            target = bpy.context.scene.l_exclude[findex]
            row.active = target.value
            # Parent collection runtime visibility
            subrow.prop(target, "value", text="")
            findex += 1

        return index

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False

        view = context.space_data
        view_layer = context.view_layer

        if 'Layers' in view_layer.layer_collection.children:

            self._draw_collection(
                layout,
                view_layer,
                view.use_local_collections,
                view_layer.layer_collection.children['Layers'],
                1
            )


classes = (
    Acon3dCreateGroupOperator,
    Acon3dExplodeGroupOperator,
    Acon3dLayerPanel,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.app.handlers.load_post.append(load_handler)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    
    bpy.app.handlers.load_post.remove(load_handler)