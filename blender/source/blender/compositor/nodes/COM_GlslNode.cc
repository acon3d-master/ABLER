#include "COM_GlslNode.h"

#include "COM_GlslOperation.h"
#include "COM_GammaOperation.h"
#include "COM_ExecutionSystem.h"
#include "BKE_scene.h"
#include "BKE_global.h"
#include "BKE_main.h"
#include "BLI_path_util.h"
#include "DNA_text_types.h"
#include <fstream>

GlslNode::GlslNode(bNode *editorNode) : Node(editorNode)
{
/* pass */
}

static std::string get_text_datablock_content(ID* id)
{
    Text *text = (Text *)id;
    if(text)
    {
        std::string output;
        TextLine *ln;
        for (ln = (TextLine *)text->lines.first; ln; ln = ln->next) {
            output += ln->line;
            output += '\n';
        }
        return output;

    }
    return "";
}

std::string readScriptContent(const std::string& path)
{
    std::ifstream input(path);
    std::stringstream buffer;
    buffer << input.rdbuf();
    return buffer.str();
}

void GlslNode::convertToOperations(NodeConverter &converter, const CompositorContext &context) const
{
    const NodeGlsl* rna = (NodeGlsl*)this->getbNode()->storage;
    bNode *node = this->getbNode();
    const Scene* scene = context.getScene();

    std::string fragment;

    switch (rna->mode) {
      case NODE_GLSL_EXTERNAL:
        fragment = readScriptContent(rna->filepath);
        break;
      case NODE_GLSL_INTERNAL:
            if (node->id) {
                fragment = get_text_datablock_content(node->id);
            }else
            {
                fragment = "\n";
            }
        break;
    }
    GlslOperationParams params;
    params.fragment = fragment;
    params.frameCurrent = BKE_scene_frame_get(scene);
    params.frameTime = 0; //Set later
    params.frameDelta = 1.0f / scene->r.frs_sec; //Assume steady progress

    GlslOperation *operation = new GlslOperation();
    operation->setParams(params);
    operation->setData(rna);
    converter.addOperation(operation);

    for (int i = 0; i < GLSL_CHANNELS; i++) {
        bool linked = getInputSocket(i)->isLinked();
        operation->setChannelLinked(i, linked);
        converter.mapInputSocket(getInputSocket(i), operation->getInputSocket(i));
    }
    for (int i = GLSL_CHANNELS; i < GLSL_CHANNELS + GLSL_VALUE_SOCKETS; i++) {
        converter.mapInputSocket(getInputSocket(i), operation->getInputSocket(i));
    }

    //Force node resolution to render settings
    //change for dev
    int w = (scene->r.size * scene->r.xsch) / 100;
    int h = (scene->r.size * scene->r.ysch) / 100;
    unsigned int size[2] = {(unsigned int) w, (unsigned int)h };
    operation->setResolution(size);

    if (rna->flag & CMP_NODE_GLSL_GAMMA) {
        GammaOperation *gamma = new GammaOperation();
        converter.addOperation(gamma);
        converter.addLink(operation->getOutputSocket(0), gamma->getInputSocket(0));
        converter.addInputValue(gamma->getInputSocket(1), 2.2f); //For OpenGL sRGB...
        converter.mapOutputSocket(this->getOutputSocket(0), gamma->getOutputSocket(0));
    }
    else {
        converter.mapOutputSocket(this->getOutputSocket(0), operation->getOutputSocket(0));
    }
}