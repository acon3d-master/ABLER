import bpy


def toggleToonEdge(self, context):
    node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
    if not node_group: return

    toonEdgeFactorValue = 0
    if context.scene.ACON_prop.toggle_toon_edge:
        toonEdgeFactorValue = 1

    node = node_group.nodes.get('ACON_node_toonEdgeFactor')
    if node: node.inputs[0].default_value = toonEdgeFactorValue


def toggleToonFace(self, context):
    node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
    if not node_group: return

    toonFaceFactorValue = 0
    if context.scene.ACON_prop.toggle_toon_face:
        toonFaceFactorValue = 1

    node = node_group.nodes.get('ACON_nodeGroup_toonFace')
    if node: node.inputs[4].default_value = toonFaceFactorValue


def toggleTexture(self, context):
    node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
    if not node_group: return

    textureFactorValue = 1
    if context.scene.ACON_prop.toggle_texture:
        textureFactorValue = 0

    node = node_group.nodes.get('ACON_node_textureMixFactor')
    if node: node.inputs[0].default_value = textureFactorValue


def toggleShading(self, context):
    node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
    if not node_group: return

    shadingFactorValue = 1
    if context.scene.ACON_prop.toggle_shading:
        shadingFactorValue = 0

    node = node_group.nodes.get('ACON_node_shadeMixFactor')
    if node: node.inputs[0].default_value = shadingFactorValue


def changeToonDepth(self, context):
    node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
    if not node_group: return

    toonFaceFactorValue = 1
    if context.scene.ACON_prop.toon_shading_depth == "2":
        toonFaceFactorValue = 0

    node = node_group.nodes.get('ACON_nodeGroup_toonFace')
    if node: node.inputs[1].default_value = toonFaceFactorValue


def setMaterialParametersByType(mat):

    type = mat.ACON_prop.type
    
    toonNode = mat.node_tree.nodes.get("ACON_nodeGroup_combinedToon")
    if not toonNode: return
    
    if type == "Diffuse":
        mat.blend_method = "OPAQUE"
        mat.shadow_method = "OPAQUE"
        toonNode.inputs[1].default_value = 0
        toonNode.inputs[3].default_value = 1
    
    if type == "Mirror":
        bpy.context.scene.eevee.use_ssr = True
        mat.blend_method = "OPAQUE"
        mat.shadow_method = "OPAQUE"
        toonNode.inputs[1].default_value = 0
        toonNode.inputs[2].default_value = 1
        toonNode.inputs[3].default_value = 0
        
    if type == "Glow":
        mat.blend_method = "OPAQUE"
        mat.shadow_method = "OPAQUE"
        toonNode.inputs[1].default_value = 0
        toonNode.inputs[2].default_value = 0
        toonNode.inputs[3].default_value = 0
        
    if type == "Clear":
        mat.blend_method = "BLEND"
        mat.shadow_method = "NONE"
        toonNode.inputs[1].default_value = 1
        toonNode.inputs[3].default_value = 1


def changeMaterialType(self, context):
    
    try:
        material_slots = context.active_object.material_slots
        
        for mat_slot in material_slots:
            mat = mat_slot.material
            setMaterialParametersByType(mat)
    
    except:
        print("ACON Material Type change handler could not complete.")


def changeImageAdjustBrightness(self, context):
    
    node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
    if not node_group: return

    brightContrast = node_group.nodes.get('ACON_node_brightContrast')
    if not brightContrast: return

    inputs = brightContrast.inputs

    prop = context.scene.ACON_prop
    value = prop.image_adjust_brightness

    inputs[1].default_value = value


def changeImageAdjustContrast(self, context):
    
    node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
    if not node_group: return

    brightContrast = node_group.nodes.get('ACON_node_brightContrast')
    if not brightContrast: return

    inputs = brightContrast.inputs

    prop = context.scene.ACON_prop
    value = prop.image_adjust_contrast

    inputs[2].default_value = value


def changeImageAdjustColor(self, context):
    
    node_group = bpy.data.node_groups.get('ACON_nodeGroup_combinedToon')
    if not node_group: return

    brightContrast = node_group.nodes.get('ACON_node_colorBalance')
    if not brightContrast: return

    inputs = brightContrast.inputs

    prop = context.scene.ACON_prop
    r = prop.image_adjust_color_r
    g = prop.image_adjust_color_g
    b = prop.image_adjust_color_b
    color = (r, g, b, 1)

    inputs[2].default_value = color