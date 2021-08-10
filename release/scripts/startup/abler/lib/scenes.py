import bpy
from . import shadow
from .materials import materials_handler
from types import SimpleNamespace


def genSceneName(name, i=1):
    found = None
    combinedName = name + str(i)

    for scene in bpy.data.scenes:
        if scene.name == combinedName:
            found = True
            break

    if found: return genSceneName(name, i+1)
    else: return combinedName


def add_scene_items(self, context):
    items = []
    for item in bpy.data.scenes:
        items.append((item.name, item.name, ""))

    return items


def loadScene(self, context):
    current_scene = context.scene
    target_scene = bpy.data.scenes[current_scene.ACON_prop.scene]

    if current_scene is target_scene: return

    override = SimpleNamespace()
    override.scene = target_scene
    
    # cameras.goToCustomCamera(self, context)
    materials_handler.toggleToonEdge(self, override)
    materials_handler.changeLineProps(self, override)
    materials_handler.toggleToonFace(self, override)
    materials_handler.toggleTexture(self, override)
    materials_handler.toggleShading(self, override)
    materials_handler.changeToonDepth(self, override)
    materials_handler.changeToonShadingBrightness(self, override)
    shadow.changeSunRotation(self, override)
    materials_handler.changeImageAdjustBrightness(self, override)
    materials_handler.changeImageAdjustContrast(self, override)
    materials_handler.changeImageAdjustColor(self, override)
    materials_handler.changeImageAdjustHue(self, override)
    materials_handler.changeImageAdjustSaturation(self, override)
    
    context.window.scene = target_scene

    target_scene.ACON_prop.scene = current_scene.ACON_prop.scene