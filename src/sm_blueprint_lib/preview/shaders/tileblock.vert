#version 450 core

layout (location = 0) in vec2 uv;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec3 vert;

uniform mat4 M;
uniform mat4 V;
uniform mat4 P;
uniform vec2 bounds;
uniform vec2 offset;

out vec2 UV;
out vec3 NORMAL;

void main() {
    UV = uv * bounds + offset;

    NORMAL = normal;
    gl_Position = P * V * M * vec4(vert, 1);
}
