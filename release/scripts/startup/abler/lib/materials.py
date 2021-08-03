import bpy

from . import common
from .. import custom_properties


def createOutlineNodeGroup():
    
    node_group = bpy.data.node_groups.new('ACON_nodeGroup_outline', 'ShaderNodeTree')

    nodes = node_group.nodes

    outputs = nodes.new('NodeGroupOutput')
    node_group.outputs.new('NodeSocketColor', 'Color')

    inputs = nodes.new('NodeGroupInput')
    node_group.inputs.new('NodeSocketFloat', 'Min Line Width')
    node_group.inputs.new('NodeSocketFloat', 'Max Line Width')
    node_group.inputs.new('NodeSocketFloat', 'Line Width Range')
    node_group.inputs.new('NodeSocketFloat', 'Line Detail')
    node_group.inputs.new('NodeSocketFloat', 'Negative Detail Max Distance')

    node_multiply_2 = nodes.new("ShaderNodeMath")
    node_multiply_2.operation = "MULTIPLY"
    node_group.links.new(node_multiply_2.outputs[0], outputs.inputs[0])

    node_greaterThan = nodes.new("ShaderNodeMath")
    node_greaterThan.operation = "GREATER_THAN"
    node_greaterThan.inputs[0].default_value = 1
    node_group.links.new(node_greaterThan.outputs[0], node_multiply_2.inputs[0])

    node_multiply_1 = nodes.new("ShaderNodeMath")
    node_multiply_1.operation = "MULTIPLY"
    node_multiply_1.inputs[1].default_value = 1
    node_group.links.new(node_multiply_1.outputs[0], node_greaterThan.inputs[1])
    node_group.links.new(inputs.outputs[3], node_multiply_1.inputs[1])

    node_divide_1 = nodes.new("ShaderNodeMath")
    node_divide_1.operation = "DIVIDE"
    node_group.links.new(node_divide_1.outputs[0], node_multiply_1.inputs[0])

    node_subtract_2 = nodes.new("ShaderNodeMath")
    node_subtract_2.operation = "SUBTRACT"
    node_group.links.new(node_subtract_2.outputs[0], node_divide_1.inputs[0])

    node_subtract_3 = nodes.new("ShaderNodeMath")
    node_subtract_3.operation = "SUBTRACT"
    node_group.links.new(node_subtract_3.outputs[0], node_subtract_2.inputs[0])

    node_maximum_1 = nodes.new("ShaderNodeMath")
    node_maximum_1.operation = "MAXIMUM"
    node_group.links.new(node_maximum_1.outputs[0], node_subtract_3.inputs[0])

    node_outline_1 = nodes.new("ShaderNodeOutline")
    node_group.links.new(node_outline_1.outputs[0], node_maximum_1.inputs[0])
    node_group.links.new(node_outline_1.outputs[2], node_maximum_1.inputs[1])
    node_group.links.new(node_outline_1.outputs[5], node_divide_1.inputs[1])

    node_lessThan = nodes.new("ShaderNodeMath")
    node_lessThan.operation = "LESS_THAN"
    node_group.links.new(node_lessThan.outputs[0], node_multiply_2.inputs[1])
    node_group.links.new(inputs.outputs[4], node_lessThan.inputs[1])

    node_subtract_1 = nodes.new("ShaderNodeMath")
    node_subtract_1.operation = "SUBTRACT"
    node_group.links.new(node_subtract_1.outputs[0], node_lessThan.inputs[0])

    node_length_1 = nodes.new("ShaderNodeVectorMath")
    node_length_1.operation = "LENGTH"
    node_group.links.new(node_length_1.outputs[1], node_subtract_1.inputs[0])
    node_group.links.new(node_outline_1.outputs[3], node_length_1.inputs[0])

    node_length_2 = nodes.new("ShaderNodeVectorMath")
    node_length_2.operation = "LENGTH"
    node_group.links.new(node_length_2.outputs[1], node_subtract_1.inputs[1])
    node_group.links.new(node_outline_1.outputs[1], node_length_2.inputs[0])

    node_power_1 = nodes.new("ShaderNodeMath")
    node_power_1.operation = "POWER"
    node_power_1.inputs[1].default_value = 2
    node_group.links.new(node_power_1.outputs[0], node_subtract_2.inputs[1])

    node_multiply_3 = nodes.new("ShaderNodeMath")
    node_multiply_3.operation = "MULTIPLY"
    node_multiply_3.inputs[1].default_value = 10
    node_group.links.new(node_multiply_3.outputs[0], node_power_1.inputs[0])

    node_power_2 = nodes.new("ShaderNodeMath")
    node_power_2.operation = "POWER"
    node_power_2.inputs[1].default_value = 1.5
    node_group.links.new(node_power_2.outputs[0], node_multiply_3.inputs[0])
    node_group.links.new(node_power_2.outputs[0], node_subtract_3.inputs[1])

    node_multiply_4 = nodes.new("ShaderNodeMath")
    node_multiply_4.operation = "MULTIPLY"
    node_multiply_4.inputs[1].default_value = 0.003
    node_group.links.new(node_multiply_4.outputs[0], node_power_2.inputs[0])

    node_power_3 = nodes.new("ShaderNodeMath")
    node_power_3.operation = "POWER"
    node_power_3.inputs[1].default_value = 2
    node_group.links.new(node_power_3.outputs[0], node_multiply_4.inputs[0])

    node_divide_2 = nodes.new("ShaderNodeMath")
    node_divide_2.operation = "DIVIDE"
    node_divide_2.inputs[0].default_value = 1
    node_group.links.new(node_divide_2.outputs[0], node_power_3.inputs[0])

    node_dot = nodes.new("ShaderNodeVectorMath")
    node_dot.operation = "DOT_PRODUCT"
    node_group.links.new(node_dot.outputs[1], node_divide_2.inputs[1])

    node_geometry = nodes.new("ShaderNodeNewGeometry")
    node_group.links.new(node_geometry.outputs[1], node_dot.inputs[0])
    node_group.links.new(node_geometry.outputs[4], node_dot.inputs[1])

    node_mapRange = nodes.new("ShaderNodeMapRange")
    node_group.links.new(node_mapRange.outputs[0], node_outline_1.inputs[1])
    node_group.links.new(inputs.outputs[0], node_mapRange.inputs[3])
    node_group.links.new(inputs.outputs[1], node_mapRange.inputs[4])
    node_group.links.new(inputs.outputs[2], node_mapRange.inputs[2])

    node_maximum_2 = nodes.new("ShaderNodeMath")
    node_maximum_2.operation = "MAXIMUM"
    node_group.links.new(node_maximum_2.outputs[0], node_mapRange.inputs[0])

    node_outline_2 = nodes.new("ShaderNodeOutline")
    node_group.links.new(node_outline_2.outputs[0], node_maximum_2.inputs[0])
    node_group.links.new(node_outline_2.outputs[2], node_maximum_2.inputs[1])
    node_group.links.new(inputs.outputs[1], node_outline_2.inputs[1])

    node_group.inputs[0].default_value = 1
    node_group.inputs[0].min_value = 0
    node_group.inputs[0].max_value = 5
    node_group.inputs[1].default_value = 1
    node_group.inputs[1].min_value = 0
    node_group.inputs[1].max_value = 5
    node_group.inputs[2].default_value = 2
    node_group.inputs[3].default_value = 5
    node_group.inputs[3].min_value = 0
    node_group.inputs[3].max_value = 20
    node_group.inputs[4].default_value = 1
    
    return node_group


def createToonFaceNodeGroup():
    
    node_group = bpy.data.node_groups.new('ACON_nodeGroup_toonFace', 'ShaderNodeTree')
    
    nodes = node_group.nodes
    
    outputs = nodes.new('NodeGroupOutput')
    node_group.outputs.new('NodeSocketColor', 'Color')
    
    node_multiply_1 = nodes.new('ShaderNodeMixRGB')
    node_multiply_1.blend_type = 'MULTIPLY'
    node_multiply_1.inputs[0].default_value = 1
    node_group.links.new(node_multiply_1.outputs[0], outputs.inputs[0])

    node_mix = nodes.new('ShaderNodeMixRGB')
    node_mix.blend_type = 'MIX'
    node_group.links.new(node_mix.outputs[0], node_multiply_1.inputs[2])

    node_map = nodes.new('ShaderNodeMapRange')
    node_map.inputs[1].default_value = 0
    node_map.inputs[2].default_value = 1
    node_map.inputs[3].default_value = 0
    node_map.inputs[4].default_value = 0.5
    node_group.links.new(node_map.outputs[0], node_mix.inputs[2])

    node_overlay = nodes.new('ShaderNodeMixRGB')
    node_overlay.blend_type = 'OVERLAY'
    node_group.links.new(node_overlay.outputs[0], node_map.inputs[0])

    node_colorRamp_1 = nodes.new('ShaderNodeValToRGB')
    node_colorRamp_1.color_ramp.interpolation = 'CONSTANT'
    node_colorRamp_1.color_ramp.elements[0].position = 0
    node_colorRamp_1.color_ramp.elements[0].color = (0.1, 0.1, 0.1, 1)
    node_colorRamp_1.color_ramp.elements[1].position = 0.5
    node_colorRamp_1.color_ramp.elements[1].color = (1, 1, 1, 1)
    node_group.links.new(node_colorRamp_1.outputs[0], node_overlay.inputs[1])

    node_multiply_2 = nodes.new("ShaderNodeMath")
    node_multiply_2.operation = "MULTIPLY"
    node_group.links.new(node_multiply_2.outputs[0], node_colorRamp_1.inputs[0])

    node_colorRamp_2 = nodes.new('ShaderNodeValToRGB')
    node_colorRamp_2.color_ramp.interpolation = 'CONSTANT'
    node_colorRamp_2.color_ramp.elements[0].position = 0
    node_colorRamp_2.color_ramp.elements[0].color = (0.5, 0.5, 0.5, 1)
    node_colorRamp_2.color_ramp.elements[1].position = 0.5
    node_colorRamp_2.color_ramp.elements[1].color = (1, 1, 1, 1)
    node_group.links.new(node_colorRamp_2.outputs[0], node_overlay.inputs[2])

    node_multiply_3 = nodes.new("ShaderNodeMath")
    node_multiply_3.operation = "MULTIPLY"
    node_group.links.new(node_multiply_3.outputs[0], node_colorRamp_2.inputs[0])

    node_shaderToRGB_1 = nodes.new('ShaderNodeShaderToRGB')
    node_group.links.new(node_shaderToRGB_1.outputs[0], node_multiply_2.inputs[0])
    node_group.links.new(node_shaderToRGB_1.outputs[0], node_multiply_3.inputs[0])
    node_group.links.new(node_shaderToRGB_1.outputs[0], node_mix.inputs[1])

    node_diffuseBSDF = nodes.new('ShaderNodeBsdfDiffuse')
    node_diffuseBSDF.inputs[0].default_value = (1, 1, 1, 1)
    node_group.links.new(node_diffuseBSDF.outputs[0], node_shaderToRGB_1.inputs[0])
    
    inputs = nodes.new('NodeGroupInput')
    node_group.inputs.new('NodeSocketColor', 'Color')
    node_group.inputs.new('NodeSocketFloat', 'Second Shade Factor')
    node_group.inputs.new('NodeSocketFloat', 'Brightness 1')
    node_group.inputs.new('NodeSocketFloat', 'Brightness 2')
    node_group.inputs.new('NodeSocketFloat', 'Mix Factor')
    node_group.inputs.new('NodeSocketFloat', 'Map Factor')
    node_group.links.new(inputs.outputs[0], node_multiply_1.inputs[1])
    node_group.links.new(inputs.outputs[1], node_overlay.inputs[0])
    node_group.links.new(inputs.outputs[2], node_multiply_2.inputs[1])
    node_group.links.new(inputs.outputs[3], node_multiply_3.inputs[1])
    node_group.links.new(inputs.outputs[4], node_mix.inputs[0])
    node_group.links.new(inputs.outputs[5], node_map.inputs[4])

    node_group.inputs[1].default_value = 0
    node_group.inputs[1].min_value = 0
    node_group.inputs[1].max_value = 1

    node_group.inputs[2].default_value = 3
    node_group.inputs[2].min_value = 0
    node_group.inputs[2].max_value = 10

    node_group.inputs[3].default_value = 5
    node_group.inputs[3].min_value = 0
    node_group.inputs[3].max_value = 10
    
    node_group.inputs[5].default_value = 1

    node_group.inputs[0].default_value = (1, 1, 1, 1)
    
    return node_group


def createAconMatNodeGroups():
    
    node_group_data_outline = createOutlineNodeGroup()
    
    node_group_data_toonFace = createToonFaceNodeGroup()
    
    node_group = bpy.data.node_groups.new('ACON_nodeGroup_combinedToon', 'ShaderNodeTree')
    
    nodes = node_group.nodes
    
    outputs = nodes.new('NodeGroupOutput')
    node_group.outputs.new('NodeSocketShader', 'Shader')

    node_mixShader = nodes.new('ShaderNodeMixShader')
    node_group.links.new(node_mixShader.outputs[0], outputs.inputs[0])

    node_mixShader_2 = nodes.new('ShaderNodeMixShader')
    node_group.links.new(node_mixShader_2.outputs[0], node_mixShader.inputs[2])
    
    node_subtract_1 = nodes.new("ShaderNodeMath")
    node_subtract_1.operation = "SUBTRACT"
    node_subtract_1.inputs[0].default_value = 1
    node_group.links.new(node_subtract_1.outputs[0], node_mixShader_2.inputs[0])
    
    node_multiply_1 = nodes.new("ShaderNodeMath")
    node_multiply_1.operation = "MULTIPLY"
    node_group.links.new(node_multiply_1.outputs[0], node_subtract_1.inputs[1])

    node_mixShader_3 = nodes.new('ShaderNodeMixShader')
    node_group.links.new(node_mixShader_3.outputs[0], node_mixShader.inputs[1])
    
    node_emission = nodes.new('ShaderNodeEmission')
    node_emission.inputs[0].default_value = (1, 1, 1, 1)
    node_group.links.new(node_emission.outputs[0], node_mixShader_3.inputs[1])
    
    node_glossy = nodes.new('ShaderNodeBsdfGlossy')
    node_glossy.inputs[0].default_value = (1, 1, 1, 1)
    node_group.links.new(node_glossy.outputs[0], node_mixShader_3.inputs[2])
    
    node_subtract_2 = nodes.new("ShaderNodeMath")
    node_subtract_2.operation = "SUBTRACT"
    node_subtract_2.inputs[0].default_value = 1
    node_group.links.new(node_subtract_2.outputs[0], node_glossy.inputs[1])

    node_multiply_2 = nodes.new('ShaderNodeMixRGB')
    node_multiply_2.name = 'ACON_node_toonEdgeFactor'
    node_multiply_2.blend_type = 'MULTIPLY'
    node_multiply_2.inputs[0].default_value = 1
    node_group.links.new(node_multiply_2.outputs[0], node_mixShader_2.inputs[2])
    
    node_mixColor_2 = nodes.new('ShaderNodeMixRGB')
    node_mixColor_2.name = 'ACON_node_shadeMixFactor'
    node_mixColor_2.blend_type = 'MIX'
    node_mixColor_2.inputs[0].default_value = 0
    node_group.links.new(node_mixColor_2.outputs[0], node_multiply_2.inputs[1])
    
    node_group_toonFace = nodes.new(type='ShaderNodeGroup')
    node_group_toonFace.name = 'ACON_nodeGroup_toonFace'
    node_group_toonFace.node_tree = node_group_data_toonFace
    node_group_toonFace.inputs[4].default_value = 1
    node_group.links.new(node_group_toonFace.outputs[0], node_mixColor_2.inputs[1])
    
    node_group_outline = nodes.new(type='ShaderNodeGroup')
    node_group_outline.name = 'ACON_nodeGroup_outline'
    node_group_outline.node_tree = node_group_data_outline
    node_group.links.new(node_group_outline.outputs[0], node_multiply_2.inputs[2])

    node_transparent = nodes.new('ShaderNodeBsdfTransparent')
    node_transparent.inputs[0].default_value = (1, 1, 1, 1)
    node_group.links.new(node_transparent.outputs[0], node_mixShader_2.inputs[1])

    node_mixColor = nodes.new('ShaderNodeMixRGB')
    node_mixColor.name = 'ACON_node_textureMixFactor'
    node_mixColor.blend_type = 'MIX'
    node_group.links.new(node_mixColor.outputs[0], node_mixColor_2.inputs[2])
    node_group.links.new(node_mixColor.outputs[0], node_group_toonFace.inputs[0])
    node_group.links.new(node_mixColor.outputs[0], node_emission.inputs[0])
    node_group.links.new(node_mixColor.outputs[0], node_glossy.inputs[0])
    node_mixColor.inputs[0].default_value = 0
    node_mixColor.inputs[2].default_value = (1, 1, 1, 1)

    node_hueSaturation = nodes.new('ShaderNodeHueSaturation')
    node_hueSaturation.name = 'ACON_node_hueSaturation'
    node_group.links.new(node_hueSaturation.outputs[0], node_mixColor.inputs[1])

    node_colorBalance = nodes.new('ShaderNodeMixRGB')
    node_colorBalance.name = 'ACON_node_colorBalance'
    node_colorBalance.blend_type = 'MULTIPLY'
    node_colorBalance.inputs[0].default_value = 1
    node_colorBalance.inputs[2].default_value = (1, 1, 1, 1)
    node_group.links.new(node_colorBalance.outputs[0], node_hueSaturation.inputs[4])

    node_brightContrast = nodes.new('ShaderNodeBrightContrast')
    node_brightContrast.name = 'ACON_node_brightContrast'
    node_group.links.new(node_brightContrast.outputs[0], node_colorBalance.inputs[1])

    inputs = nodes.new('NodeGroupInput')
    node_group.inputs.new('NodeSocketColor', 'Color')
    node_group.inputs.new('NodeSocketFloat', 'AlphaMixFactor')
    node_group.inputs.new('NodeSocketFloat', 'MixFactor1')
    node_group.inputs.new('NodeSocketFloat', 'MixFactor2')
    node_group.inputs.new('NodeSocketFloat', 'MixFactor3')
    node_group.inputs.new('NodeSocketFloat', 'Strength')
    node_group.inputs.new('NodeSocketFloat', 'Smoothness')
    node_group.inputs.new('NodeSocketFloat', 'Negative Alpha')
    node_group.links.new(inputs.outputs[0], node_brightContrast.inputs[0])
    node_group.links.new(inputs.outputs[1], node_multiply_1.inputs[1])
    node_group.links.new(inputs.outputs[2], node_mixShader_3.inputs[0])
    node_group.links.new(inputs.outputs[3], node_mixShader.inputs[0])
    node_group.links.new(inputs.outputs[5], node_emission.inputs[1])
    node_group.links.new(inputs.outputs[6], node_subtract_2.inputs[1])
    node_group.links.new(inputs.outputs[7], node_multiply_1.inputs[0])

    node_group.inputs[0].default_value = (1, 1, 1, 1)
    node_group.inputs[1].default_value = 0
    node_group.inputs[1].min_value = 0
    node_group.inputs[1].max_value = 1
    node_group.inputs[2].default_value = 1
    node_group.inputs[3].default_value = 1
    node_group.inputs[5].default_value = 1
    node_group.inputs[5].min_value = 0
    node_group.inputs[6].default_value = 0.5
    node_group.inputs[6].min_value = 0
    node_group.inputs[6].max_value = 1
    node_group.inputs[7].default_value = 0
    node_group.inputs[7].min_value = 0
    node_group.inputs[7].max_value = 1

    context = bpy.context

    custom_properties.toggleToonEdge(None, context)
    custom_properties.toggleToonFace(None, context)
    custom_properties.toggleTexture(None, context)
    custom_properties.toggleShading(None, context)
    custom_properties.changeToonDepth(None, context)
    custom_properties.changeImageAdjustBrightness(None, context)
    custom_properties.changeImageAdjustContrast(None, context)
    custom_properties.changeImageAdjustColor(None, context)
    
    return node_group


def removeAconMatNodeGroups():

    ACON_node_group_names = [
        'ACON_nodeGroup_outline',
        'ACON_nodeGroup_toonFace',
        'ACON_nodeGroup_combinedToon'
    ]
    
    for node_group in bpy.data.node_groups:
        for ACON_node_group_name in ACON_node_group_names:
            if ACON_node_group_name in node_group.name:
                bpy.data.node_groups.remove(node_group)
                break


def applyAconToonStyle():

    removeAconMatNodeGroups()
    node_group_data_combined = createAconMatNodeGroups()

    for obj in bpy.data.objects:

        if (obj.type == 'MESH') and ("ACON_mod_edgeSplit" not in obj.modifiers):
            obj.modifiers.new("ACON_mod_edgeSplit", type = "EDGE_SPLIT")
    
    for mat in bpy.data.materials:

        mat.use_nodes = True
        
        nodes = mat.node_tree.nodes
            
        node_texImage = None
        baseColor = (1, 1, 1, 1)
        nega_alpha = 0
        is_arleady_toonStyle = False
        
        for node in nodes:

            if node.name == "ACON_nodeGroup_combinedToon":
                node.node_tree = node_group_data_combined
                is_arleady_toonStyle = True
            
            elif node.type == "TEX_IMAGE":
                node_texImage = node
            
            elif node.type == "BSDF_PRINCIPLED":
                default_value = node.inputs[0].default_value
                baseColor = (default_value[0], default_value[1], default_value[2], default_value[3])
                nega_alpha = 1 - node.inputs[19].default_value
        
        if is_arleady_toonStyle:
            continue
        
        out_node = nodes.new(type='ShaderNodeOutputMaterial')
        
        node_combinedToon = nodes.new(type='ShaderNodeGroup')
        node_combinedToon.name = 'ACON_nodeGroup_combinedToon'
        node_combinedToon.node_tree = node_group_data_combined
        node_combinedToon.inputs[7].default_value = nega_alpha
        mat.node_tree.links.new(node_combinedToon.outputs[0], out_node.inputs[0])

        if node_texImage:
            mat.node_tree.links.new(node_texImage.outputs[0], node_combinedToon.inputs[0])
        else:
            node_combinedToon.inputs[0].default_value = baseColor
        
        for node in nodes:
            is_node_texImage = node == node_texImage
            is_out_node = node == out_node
            is_node_combinedToon = node == node_combinedToon

            if not is_node_texImage and not is_out_node and not is_node_combinedToon:
                mat.node_tree.nodes.remove(node)
        
        if "ACON_mat" in mat.name:
        
            if "mirror" in mat.name:
                mat.ACON_prop.type = "Mirror"
                
            if "light" in mat.name:
                mat.ACON_prop.type = "Glow"
            
                strength = 1
                
                try:
                    components = mat.name.split("_")
                    strength = 1.6 ** (int(components[3]) - 3.2)
                except:
                    print("Fllowing ACON_mat has invalid format")
                    print(mat.name)
                
                node_combinedToon.inputs[5].default_value = strength
                
            if "clear" in mat.name:
                mat.ACON_prop.type = "Clear"
        
        setMaterialParametersByType(mat)
        
    common.switchToRendredView()


def setMaterialParametersByType(mat):

    type = mat.ACON_prop.type
    toonNode = mat.node_tree.nodes["ACON_nodeGroup_combinedToon"]
    
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