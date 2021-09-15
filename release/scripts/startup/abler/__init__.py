# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


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

from . import custom_properties
from . import credential_modal
from . import general
from . import scene_control
from . import edge_control
from . import face_control
from . import image_adjustment
from . import shadow_control
from . import view_control
from . import layer_control
from . import render_control
from . import pref


# =========================================================================
# Registration:
# =========================================================================


def register():
    try: custom_properties.register()
    except: print("Abler: Failed to register custom properties")
    try: credential_modal.register()
    except: print("Abler: Failed to register credential modal operators")
    try: general.register()
    except: print("Abler: Failed to register general panel")
    try: scene_control.register()
    except: print("Abler: Failed to register scene control panel")
    try: edge_control.register()
    except: print("Abler: Failed to register edge control panel")
    try: face_control.register()
    except: print("Abler: Failed to register face control panel")
    try: image_adjustment.register()
    except: print("Abler: Failed to register image adjustment panel")
    try: shadow_control.register()
    except: print("Abler: Failed to register shadow control panel")
    try: view_control.register()
    except: print("Abler: Failed to register view control panel")
    try: layer_control.register()
    except: print("Abler: Failed to register layer control panel")
    try: render_control.register()
    except: print("Abler: Failed to register render control panel")
    try: pref.register()
    except: print("Abler: Failed to register preference handler")


def unregister():
    try: pref.unregister()
    except: print("Abler: Failed to unregister preference handler")
    try: render_control.unregister()
    except: print("Abler: Failed to unregister render control panel")
    try: layer_control.unregister()
    except: print("Abler: Failed to unregister layer control panel")
    try: view_control.unregister()
    except: print("Abler: Failed to unregister view control panel")
    try: shadow_control.unregister()
    except: print("Abler: Failed to unregister shadow control panel")
    try: image_adjustment.unregister()
    except: print("Abler: Failed to unregister image adjustment panel")
    try: face_control.unregister()
    except: print("Abler: Failed to unregister face control panel")
    try: edge_control.unregister()
    except: print("Abler: Failed to unregister edge control panel")
    try: scene_control.unregister()
    except: print("Abler: Failed to unregister scene control panel")
    try: general.unregister()
    except: print("Abler: Failed to unregister general panel")
    try: credential_modal.unregister()
    except: print("Abler: Failed to unregister credential modal operators")
    try: custom_properties.register()
    except: print("Abler: Failed to unregister custom properties")


if __name__ == "__main__":
    register()
