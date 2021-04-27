/*
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 *
 * Copyright 2011, Blender Foundation.
 */

#include "BKE_global.h"
#include "WM_api.h"
#include "GPU_framebuffer.h"
#include "GPU_texture.h"
#include "GPU_shader.h"
#include "GPU_glew.h"
#include "DRW_engine.h"
#include "GPU_matrix.h"

#include "COM_GlslOperation.h"
#include <iostream>

namespace blender::compositor {

    GlslOperation::GlslOperation() : SingleThreadedOperation()
    {
        for (int i = 0; i < GLSL_CHANNELS; i++) {
            this->addInputSocket(DataType::Color);
            this->m_channelLinked[i] = false;
        }
        for (int i = 0; i < GLSL_VALUE_SOCKETS; i++) {
            this->addInputSocket(DataType::Value);
        }
        this->addOutputSocket(DataType::Color);
        this->setResolutionInputSocketIndex(0);
        this->m_data = NULL;
    }

    void GlslOperation::initExecution()
    {
        SingleThreadedOperation::initExecution();
    }

    void GlslOperation::deinitExecution()
    {
        SingleThreadedOperation::deinitExecution();
    }

    struct GlslChannelInput {
        float pixel[4];
        float* rgba;
        int width;
        int height;
    };

    struct ThreadResult {
        ThreadCondition condition;
        ThreadMutex mutex;
        const GlslOperationParams *params;
        GlslChannelInput inputs[GLSL_CHANNELS];
        std::string script;
        int width;
        int height;
        float *output;
    };

    GPUShader *createShader(ThreadResult *data);
    void glslMainThreadCallback(void* userData);
    void setFloat(GPUShader *shader, const char *name, const float *value, int length);
    void setUniforms(GPUShader *shader, ThreadResult *data);
    void drawImage(GPUShader *shader, ThreadResult *data, std::vector<GPUTexture*> *textures);
    std::vector<GPUTexture*> createTextures(ThreadResult *data);
    void freeTextures(std::vector<GPUTexture*> *textures);
    std::string readScriptContent(const std::string& path);

    const char* GLSL_NODE_UNIFORMS =
    "uniform vec3		iResolution;\n"
    "uniform float		iTime;\n"
    "uniform float		iTimeDelta;\n"
    "uniform float		iFrame;\n"
    "uniform float		iChannelTime[4];\n"
    "uniform vec4		iMouse;\n"
    "uniform vec4		iDate;\n"
    "uniform float		iSampleRate;\n"
    "uniform vec3		iChannelResolution[4];\n"
    "uniform sampler2D  iChannel0;\n"
    "uniform sampler2D  iChannel1;\n"
    "uniform sampler2D  iChannel2;\n"
    "uniform sampler2D  iChannel3;\n"
    "uniform vec4		userInput;\n" //Our addition
    ;

    const char *GLSL_DEFINES =
    "#define input0 userInput.x\n"
    "#define input1 userInput.y\n"
    "#define input2 userInput.z\n"
    "#define input3 userInput.w\n"
    ;

    const char *GLSL_NODE_VS =
    "in vec4 position;\n"
    "out vec2 varTex;\n"

    "void main() {\n"
    "	gl_Position.xyz = vec3(position.x, position.y, 0.0);\n"
    "	gl_Position.w = 1.0;\n"
    "	varTex = position.zw;\n"
    "}\n"
    ;

    const char *GLSL_NODE_PS =
    "in vec2 varTex;\n"
    "out vec4 glFragColor;\n"
    "void main() {\n"
    "	mainImage(glFragColor, gl_FragCoord.xy);\n"
    "}\n"
    ;

    const float FULLSCREEN_QUAD[] = {
        -1, -1, 0.0, 0.0, //Bottom left
        1, -1, 1.0, 0.0, //Bottom right
        - 1, 1, 0.0, 1.0, //Top left
        1, 1, 1.0, 1.0, //Top right
    };

    GPUShader *createShader(ThreadResult *data)
    {
        if (data->script.empty()) {
            return NULL;
        }

        std::string fragment;
        fragment += GLSL_NODE_UNIFORMS;
        fragment += data->script;
        fragment += "\n";
        fragment += GLSL_NODE_PS;

        return GPU_shader_create(GLSL_NODE_VS, fragment.c_str(), NULL, NULL, GLSL_DEFINES, __func__);
    }

    void setFloat(GPUShader *shader, const char *name, const float *value, int length)
    {
    	int location = GPU_shader_get_uniform(shader, name);
        if (location != -2) {
            GPU_shader_uniform_vector(shader, location, length, 1, value);
        }
    }

    void setUniforms(GPUShader *shader, ThreadResult *data)
    {
        float value[4] = { 0 };

        value[0] = data->width;
        value[1] = data->height;
        value[3] = 1;
        setFloat(shader, "iResolution", value, 3);

        value[0] = data->params->frameTime;
        setFloat(shader, "iTime", value, 1);

        value[0] = data->params->frameDelta;
        setFloat(shader, "iTimeDelta", value, 1);

        value[0] = data->params->frameCurrent;
        setFloat(shader, "iFrame", value, 1);

        float resolutions[3 * GLSL_CHANNELS];
        for (int i = 0; i < GLSL_CHANNELS; i++) {
            int index = i * 3;
            resolutions[index] = data->inputs[i].width;
            resolutions[index + 1] = data->inputs[i].height;
            resolutions[index + 2] = 1;
        }
        GPU_shader_uniform_vector(shader, GPU_shader_get_uniform(shader, "iChannelResolution"), 3, GLSL_CHANNELS, resolutions);

        setFloat(shader, "userInput", data->params->input0, 4);
    }

    void drawImage(GPUShader *shader, ThreadResult *data, std::vector<GPUTexture*> *textures)
    {
        GPU_shader_bind(shader);

        setUniforms(shader, data);

        for (int i = 0; i < textures->size(); i++) {
            std::string name = "iChannel" + std::to_string(i);
            int loc = GPU_shader_get_uniform(shader, name.c_str());
            int slot = GPU_shader_get_texture_binding(shader, name.c_str());
            

            if (textures->at(i) && loc != -1 && slot != -1) {
                // int slot = GPU_shader_get_texture_binding(shader, name);
                GPU_texture_bind(textures->at(i), i);
                // GPU_shader_uniform_texture(shader, loc, textures->at(i));
                // std::cout << std::to_string(textures->size()) << std::endl;
                // std::string hame = "hihi" + std::to_string(loc) + " " + std::to_string((textures->at(i))->number);
                // std::cout << hame << std::endl;
                // int idid = (reinterpret_cast<Texture *>(textures->at(i)))->tex_id_;
                // std::cout << std::to_string(idid) << std::endl;
                std::cout << "integer: " + std::to_string(GPU_texture_format(textures->at(i))) << std::endl;
                // std::cout << "integer: " + std::to_string(GPU_texture_(textures->at(i))) << std::endl;
                // std::cout << "integer: " + std::to_string(GPU_texture_integer(textures->at(i))) << std::endl;
                GPU_shader_uniform_int(shader, loc, GPU_texture_format(textures->at(i)));
            }
        }

        GLuint buffer;
        glGenBuffers(1, &buffer);
        glBindBuffer(GL_ARRAY_BUFFER, buffer);
        glBufferData(GL_ARRAY_BUFFER, sizeof(FULLSCREEN_QUAD), FULLSCREEN_QUAD, GL_STATIC_DRAW);

        GLuint array = 0;
        glGenVertexArrays(1, &array);
        glBindVertexArray(array);
        glBindBuffer(GL_ARRAY_BUFFER, buffer);

        int index = GPU_shader_get_attribute(shader, "position");
        glVertexAttribPointer(index, 4, GL_FLOAT, GL_FALSE, 0, 0);
        glEnableVertexAttribArray(index);

        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4);

        glDisableVertexAttribArray(index);

        for (int i = 0; i < textures->size(); i++) {
            if (textures->at(i)) {
                GPU_texture_unbind(textures->at(i));
            }
        }
        glBindVertexArray(0);
        GPU_shader_unbind();
    }

    std::vector<GPUTexture*> createTextures(ThreadResult *data)
    {
        std::vector<GPUTexture*> results;
        // char error[256];

        for (int i = 0; i < GLSL_CHANNELS; i++) {
            GlslChannelInput *input = &data->inputs[i];
            GPUTexture *tex = NULL;
            if (input->rgba) {
                tex = GPU_texture_create_2d("glslNodeTexture " + i, input->width, input->height, 1, GPU_RGBA16F, NULL);
                if (tex) {
                    GPU_texture_bind(tex, 0);
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
                    GPU_texture_unbind(tex);
                }
            }
            results.push_back(tex);
        }
        return results;
    }

    void freeTextures(std::vector<GPUTexture*> *textures)
    {
        for (int i = 0; i < textures->size(); i++) {
            if (textures->at(i)) {
                GPU_texture_free(textures->at(i));
            }
        }
        textures->clear();
    }

    void glslMainThreadCallback(void* userData)
    {
        BLI_assert(BLI_thread_is_main());

        ThreadResult* data = (ThreadResult*)userData;

        std::vector<GPUTexture*> textures = createTextures(data);

        GPUShader *shader = createShader(data);
        if (shader) {
            char error[256];
            DRW_opengl_context_enable(); /* Offscreen creation needs to be done in DRW context. */
            GPUOffScreen *offscreen = GPU_offscreen_create(data->width, data->height, false, false, error);
            DRW_opengl_context_disable();

            bool resized = false;
            if (offscreen) {
                if (GPU_offscreen_width(offscreen) != data->width || GPU_offscreen_height(offscreen) != data->height) {
                    printf("Invalid offscreen size!\n");
                    resized = true;
                }
            }
            else {
                printf("Can't create an offscreen buffer: %s, %ix%i\n", error, data->width, data->height);
            }

            if (offscreen) {
                GPU_offscreen_bind(offscreen, true);

                if (!resized) {
                    drawImage(shader, data, &textures);

                    GPU_offscreen_read_pixels(offscreen, GPU_DATA_FLOAT, data->output);
                }
                GPU_offscreen_unbind(offscreen, true);

                GPU_offscreen_free(offscreen);
            }
            GPU_shader_free(shader);
        }

        freeTextures(&textures);

        BLI_condition_notify_all(&data->condition);
    }

    MemoryBuffer *GlslOperation::createMemoryBuffer(rcti *source)
    {
        rcti rect;
        rect.xmin = 0;
        rect.ymin = 0;
        rect.xmax = source->xmax;
        rect.ymax = source->ymax;
        MemoryBuffer *result = new MemoryBuffer(DataType::Color, rect);

        const float invalid[] = { 1, 0, 0, 1 };
        for (int y = 0; y < rect.ymax; y++) {
            for (int x = 0; x < rect.xmax; x++) {
                result->writePixel(x, y, invalid);
            }
        }

        if (G.background) {
            printf("GLSL node not supported in background mode\n");
            return result;
        }

        ThreadResult threadResult;
        BLI_mutex_init(&threadResult.mutex);
        BLI_condition_init(&threadResult.condition);

        memset(threadResult.inputs, 0, sizeof(threadResult.inputs));
        for (int i = 0; i < GLSL_CHANNELS; i++) {
            GlslChannelInput *input = &threadResult.inputs[i];
            SocketReader *reader = getInputSocketReader(i);

            if (m_channelLinked[i]) {
                MemoryBuffer *tile = (MemoryBuffer*)reader->initializeTileData(NULL);
                if (tile) {
                    input->width = tile->getWidth();
                    input->height = tile->getHeight();
                    input->rgba = tile->getBuffer();
                }
            }
            else {
                //Save memory by using a single color 1x1 texture
                input->width = 1;
                input->height = 1;
                input->rgba = input->pixel;
                reader->readSampled(input->rgba, 0, 0, PixelSampler::Nearest);
            }
        }

        float value[4] = {};
        getInputSocketReader(GLSL_CHANNELS)->readSampled(value, 0, 0, PixelSampler::Nearest);
        m_params.frameTime = value[0];

        for (int i = 0; i < 4; i++) {
            getInputSocketReader(GLSL_CHANNELS + 1 + i)->readSampled(value, 0, 0, PixelSampler::Nearest);
            m_params.input0[i] = value[0];
        }

        threadResult.params = &m_params;
        threadResult.width = rect.xmax;
        threadResult.height = rect.ymax;
        threadResult.output = result->getBuffer();
        threadResult.script = m_params.fragment;

        // Run OpenGL operations in the main thread and wait until they are ready
        WM_run_in_main_thread(glslMainThreadCallback, &threadResult);
        BLI_condition_wait(&threadResult.condition, &threadResult.mutex);

        BLI_mutex_end(&threadResult.mutex);
        BLI_condition_end(&threadResult.condition);
        return result;
    }

    bool GlslOperation::determineDependingAreaOfInterest(rcti * /*input*/, ReadBufferOperation *readOperation, rcti *output)
    {
        if (isCached()) {
            return false;
        }
        else {
            rcti newInput;
            newInput.xmin = 0;
            newInput.ymin = 0;
            newInput.xmax = this->getWidth();
            newInput.ymax = this->getHeight();
            return NodeOperation::determineDependingAreaOfInterest(&newInput, readOperation, output);
        }
    }
}