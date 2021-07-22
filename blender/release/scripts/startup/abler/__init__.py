bl_info = {
    "name": "ACON3D Panel",
    "description": "",
    "author": "sdk@acon3d.com, hoie@acon3d.com",
    "version": (0, 0, 1),
    "blender": (2, 93, 0),
    "location": "",
    "warning": "",  # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "ACON3D"
}

# Main imports
import bpy

from . import file_control
from . import edge_control
from . import face_control
from . import image_adjustment
from . import shadow_control
from . import view_control
from . import layer_control
from . import render_control

# =========================================================================
# Registration:
# =========================================================================

def register():
    file_control.register()
    edge_control.register()
    face_control.register()
    image_adjustment.register()
    shadow_control.register()
    view_control.register()
    layer_control.register()
    render_control.register()


def unregister():
    render_control.unregister()
    layer_control.unregister()
    view_control.unregister()
    shadow_control.unregister()
    image_adjustment.unregister()
    face_control.unregister()
    edge_control.unregister()
    file_control.unregister()

if __name__ == "__main__":
    register()
