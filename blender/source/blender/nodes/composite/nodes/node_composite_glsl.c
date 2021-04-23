#include "node_composite_util.h"

static bNodeSocketTemplate cmp_node_glsl_in[] = {
    { SOCK_RGBA,  1, N_("Channel 0"),      0.0f, 0.0f, 0.0f, 1.0f },
    { SOCK_RGBA,  1, N_("Channel 1"),      0.0f, 0.0f, 0.0f, 1.0f },
    { SOCK_RGBA,  1, N_("Channel 2"),      0.0f, 0.0f, 0.0f, 1.0f },
    { SOCK_RGBA,  1, N_("Channel 3"),      0.0f, 0.0f, 0.0f, 1.0f },
    { SOCK_FLOAT, 1, N_("Time"),	       0.0f, 0.0f, 0.0f, 0.0f, 0.0f, FLT_MAX },
    { SOCK_FLOAT, 1, N_("Input 0"),	       0.0f, 0.0f, 0.0f, 0.0f, 0.0f, FLT_MAX },
    { SOCK_FLOAT, 1, N_("Input 1"),        0.0f, 0.0f, 0.0f, 0.0f, 0.0f, FLT_MAX },
    { SOCK_FLOAT, 1, N_("Input 2"),        0.0f, 0.0f, 0.0f, 0.0f, 0.0f, FLT_MAX },
    { SOCK_FLOAT, 1, N_("Input 3"),        0.0f, 0.0f, 0.0f, 0.0f, 0.0f, FLT_MAX },
    { -1, 0, "" }
};

static bNodeSocketTemplate cmp_node_glsl_out[] = {
    { SOCK_RGBA, 0, N_("Image") },
    { -1, 0, "" }
};

static void node_composit_init_glsl(bNodeTree *UNUSED(ntree), bNode *node)
{
    NodeGlsl *data = MEM_callocN(sizeof(NodeGlsl), "glsl node");

    data->flag = CMP_NODE_GLSL_GAMMA;
    memset(data->filepath, 0, sizeof(data->filepath));

    node->storage = data;
}

void register_node_type_cmp_glsl(void)
{
    static bNodeType ntype;

    cmp_node_type_base(&ntype, CMP_NODE_GLSL, "GLSL Shader", NODE_CLASS_OP_FILTER, 0);
    node_type_socket_templates(&ntype, cmp_node_glsl_in, cmp_node_glsl_out);
    node_type_init(&ntype, node_composit_init_glsl);
    node_type_storage(&ntype, "NodeGlsl", node_free_standard_storage, node_copy_standard_storage);

    nodeRegisterType(&ntype);
}