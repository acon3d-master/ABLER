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
    custom_properties.register()
    credential_modal.register()
    general.register()
    scene_control.register()
    edge_control.register()
    face_control.register()
    image_adjustment.register()
    shadow_control.register()
    view_control.register()
    layer_control.register()
    render_control.register()
    pref.register()


def unregister():
    pref.register()
    render_control.unregister()
    layer_control.unregister()
    view_control.unregister()
    shadow_control.unregister()
    image_adjustment.unregister()
    face_control.unregister()
    edge_control.unregister()
    scene_control.unregister()
    general.unregister()
    credential_modal.unregister()
    custom_properties.register()


if __name__ == "__main__":
    register()
