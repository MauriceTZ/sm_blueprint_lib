#version 450 core

layout (location = 0) in vec2 uv;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec3 vert;

layout (location = 3) in vec4 M0;
layout (location = 4) in vec4 M1;
layout (location = 5) in vec4 M2;
layout (location = 6) in vec4 M3;

layout (location = 7) in vec3 color;
layout (location = 8) in float alpha;

uniform mat4 V;
uniform mat4 P;

out vec2 UV;
out vec3 NORMAL;
out vec3 COLOR;
out float ALPHA;

void main() {
    UV = uv;
    NORMAL = normal;
    COLOR = color;
    ALPHA = alpha;
    mat4 M = mat4(M0, M1, M2, M3);
    gl_Position = P * V * M * vec4(vert, 1);
}