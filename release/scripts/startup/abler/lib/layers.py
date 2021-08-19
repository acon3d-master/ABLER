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


import bpy


def obj_active_callback():
    
    selected_object = bpy.context.active_object
    group_props = selected_object.ACON_prop.group

    if not len(group_props): return
    
    last_group_prop = group_props[len(group_props) - 1]
    
    selected_group = bpy.data.collections.get(last_group_prop.name)
    if not selected_group: return

    for obj in selected_group.all_objects:
        obj.select_set(True)


owner = object()


def subscribeToGroupedObjects():
    
    subscribe_to = bpy.types.LayerObjects, "active"
    
    bpy.msgbus.subscribe_rna(
        key=subscribe_to,
        owner=owner,
        args=(),
        notify=obj_active_callback,
    )


def clearSubscribers():
    
    bpy.msgbus.clear_by_owner(owner)

