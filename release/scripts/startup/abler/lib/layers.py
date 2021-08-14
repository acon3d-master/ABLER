import bpy


def obj_active_callback(ob):
    if ob.select_get():
        col_group = bpy.data.collections.get("Group")

        found_col = None
        for col in col_group.children:
            for ob_2 in col.all_objects:
                if ob_2 == ob:
                    found_col = col
                    break
            if found_col: break

        if found_col:
            for ob_3 in found_col.all_objects:
                ob_3.select_set(True)


def subscribeToGroupedObjects():

    col_group = bpy.data.collections.get("Group")

    for ob in col_group.all_objects:

        if ob.type != 'MESH':
            continue
        subscribe_to = bpy.types.LayerObjects, "active"

        bpy.msgbus.subscribe_rna(
            key=subscribe_to,
            owner=ob,
            args=(ob,),
            notify=obj_active_callback,
        )