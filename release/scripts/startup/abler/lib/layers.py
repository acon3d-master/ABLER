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


def obj_active_callback(ob):

    if "select_get" in ob and ob.select_get():

        col_group = bpy.data.collections.get("Groups")
        if not col_group: return

        for col in col_group.children:
            ob_2 = col.all_objects.get(ob.name)
            if ob_2:
                for ob_3 in col.all_objects:
                    ob_3.select_set(True)


def subscribeToGroupedObjects():
    
    for ob in bpy.data.objects:

        if ob.type != 'MESH':
            continue

        subscribe_to = bpy.types.LayerObjects, "active"

        bpy.msgbus.clear_by_owner(ob)
        bpy.msgbus.subscribe_rna(
            key=subscribe_to,
            owner=ob,
            args=(ob,),
            notify=obj_active_callback,
        )

