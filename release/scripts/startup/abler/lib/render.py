import bpy


def setupBackgroundImagesCompositor():

    context = bpy.context
    scene = context.scene

    scene.render.film_transparent = True
    scene.use_nodes = True
    tree = scene.node_tree
    nodes = tree.nodes

    for node in nodes:
        nodes.remove(node)

    node_composite = nodes.new("CompositorNodeComposite")
    node_rlayer = nodes.new("CompositorNodeRLayers")

    background_images = scene.camera.data.background_images

    node_entry_left_out = node_rlayer.outputs[0]
    node_entry_right_in = node_composite.inputs[0]
    tree.links.new(node_entry_left_out, node_entry_right_in)

    for background_image in reversed(background_images):
        
        image = background_image.image
        node_image = nodes.new("CompositorNodeImage")
        node_image.image = image
        
        node_setAlpha = nodes.new("CompositorNodeSetAlpha")
        node_setAlpha.inputs[1].default_value = background_image.alpha
        tree.links.new(node_image.outputs[0], node_setAlpha.inputs[0])
        
        node_scale = nodes.new("CompositorNodeScale")
        node_scale.space = "RENDER_SIZE"
        node_scale.frame_method = background_image.frame_method
        tree.links.new(node_setAlpha.outputs[0], node_scale.inputs[0])
        
        node_conditional = node_scale
        
        if background_image.use_flip_x or background_image.use_flip_y:
            node_conditional = nodes.new("CompositorNodeFlip")
            
            if background_image.use_flip_x and background_image.use_flip_y:
                node_conditional.axis = "XY"
            elif background_image.use_flip_y:
                node_conditional.axis = "Y"
                    
            tree.links.new(node_scale.outputs[0], node_conditional.inputs[0])
        
        node_transform = nodes.new("CompositorNodeTransform")
        node_transform.inputs[1].default_value = background_image.offset[0] * scene.render.resolution_x
        node_transform.inputs[2].default_value = background_image.offset[1] * scene.render.resolution_y
        node_transform.inputs[3].default_value = -1 * background_image.rotation
        node_transform.inputs[4].default_value = background_image.scale
        tree.links.new(node_conditional.outputs[0], node_transform.inputs[0])
        
        node_alphaOver = nodes.new("CompositorNodeAlphaOver")
        tree.links.new(node_alphaOver.outputs[0], node_entry_right_in)
        
        if background_image.display_depth == "BACK":
            tree.links.new(node_transform.outputs[0], node_alphaOver.inputs[1])
            tree.links.new(node_entry_left_out, node_alphaOver.inputs[2])
            node_entry_left_out = node_alphaOver.outputs[0]
        else:
            tree.links.new(node_transform.outputs[0], node_alphaOver.inputs[2])
            tree.links.new(node_entry_left_out, node_alphaOver.inputs[1])
            node_entry_right_in = node_alphaOver.inputs[1]


def clearCompositor():

    context = bpy.context
    scene = context.scene

    scene.render.film_transparent = True
    scene.use_nodes = True
    tree = scene.node_tree
    nodes = tree.nodes

    for node in nodes:
        nodes.remove(node)

    node_composite = nodes.new("CompositorNodeComposite")
    node_rlayer = nodes.new("CompositorNodeRLayers")

    node_entry_left_out = node_rlayer.outputs[0]
    node_entry_right_in = node_composite.inputs[0]
    tree.links.new(node_entry_left_out, node_entry_right_in)