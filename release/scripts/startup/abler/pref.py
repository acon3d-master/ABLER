import bpy
from bpy.app.handlers import persistent


@persistent
def init_setting(dummy):
    prefs = bpy.context.preferences
    pref_sys = prefs.system
    prefs_view = prefs.view
    init_screen = bpy.data.screens['ACON3D'].areas[0].spaces[0]
    init_screen.show_region_header = False
    init_screen.show_gizmo = True
    init_screen.show_gizmo_navigate = True
    init_screen.show_gizmo_tool = True
    init_screen.show_gizmo_context = True
    pref_sys.use_region_overlap = False
    prefs_view.show_layout_ui = True
    prefs_view.show_navigate_ui = False
    prefs_view.show_developer_ui = False
    prefs_view.show_tooltips_python = False


def register():
    bpy.app.handlers.load_factory_startup_post.append(init_setting)
    bpy.app.handlers.load_post.append(init_setting)


def unregister():
    bpy.app.handlers.load_post.remove(init_setting)
    bpy.app.handlers.load_factory_startup_post.remove(init_setting)
