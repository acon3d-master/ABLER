import bpy


def handleLayerVisibilityOnSceneChange(oldScene, newScene):
    if not oldScene or not newScene: return

    i = 0
    for oldProp in oldScene.l_exclude:
        newProp = newScene.l_exclude[i]

        if oldProp.value is not newProp.value:
            target_layer = bpy.data.collections[newProp.name]
            for objs in target_layer.objects:
                objs.hide_viewport = not(newProp.value)
                objs.hide_render = not(newProp.value)

        if oldProp.lock is not newProp.lock:
            target_layer = bpy.data.collections[newProp.name]
            for objs in target_layer.objects:
                objs.hide_select = newProp.lock

        i += 1