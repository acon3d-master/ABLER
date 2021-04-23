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

#pragma once

#include <string>

#include "COM_NodeOperation.h"
#include "COM_SingleThreadedOperation.h"

#define GLSL_CHANNELS 4
#define GLSL_VALUE_SOCKETS 5

struct GlslOperationParams {
    std::string fragment;
    float input0[4];
    float frameCurrent;
    float frameTime;
    float frameDelta;
};

namespace blender::compositor {

class GlslOperation : public SingleThreadedOperation {
 private:
    GlslOperationParams m_params;
    const NodeGlsl *m_data;
    bool m_channelLinked[GLSL_CHANNELS];

 public:
    GlslOperation();

    void initExecution();
    void deinitExecution();
    bool determineDependingAreaOfInterest(rcti *input, ReadBufferOperation *readOperation, rcti *output);

    void setParams(const GlslOperationParams& params) { this->m_params = params; }
    void setData(const NodeGlsl *data) { this->m_data = data; }
    void setChannelLinked(int index, bool linked) { this->m_channelLinked[index] = linked; }

protected:
    MemoryBuffer *createMemoryBuffer(rcti *rect);
};

}  // namespace blender::compositor
