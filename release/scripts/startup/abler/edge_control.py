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


class Acon3dEdgePanel(bpy.types.Panel):
    bl_idname = "ACON_PT_Edge_Main"
    bl_label = "Edges Control"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="MESH_UVSPHERE")

    def draw(self, context):
        return


class EdgeSubPanel(bpy.types.Panel):
    bl_parent_id = "ACON_PT_Edge_Main"
    bl_idname = "ACON_PT_Edge_Sub"
    bl_label = "Toon Style"
    bl_category = "ACON3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        layout = self.layout
        layout.prop(context.scene.ACON_prop, "toggle_toon_edge", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        
        if context.scene.ACON_prop.toggle_toon_edge:
        
            node_group = bpy.data.node_groups['ACON_nodeGroup_combinedToon']
            outlineInputs = None

            for node in node_group.nodes:
                
                if node.name == 'ACON_nodeGroup_outline':
                    outlineInputs = node.inputs
            
            col = layout.column()
            col.prop(outlineInputs[0], "default_value", text="Min Line Width", slider=True)
            col.prop(outlineInputs[1], "default_value", text="Max Line Width", slider=True)
            col.prop(outlineInputs[3], "default_value", text="Line Detail", slider=True)



classes = (
    Acon3dEdgePanel,
    EdgeSubPanel,
)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)