#version 450 core

in vec2 UV;
in vec3 NORMAL;

uniform vec3 color;
uniform float alpha;
uniform sampler2D tex;

out vec4 output_color;

void main()
{
    vec4 diff = texture(tex, UV);
    output_color = diff + vec4(color, 0) * (1 - diff.a) * 0.80;
    output_color.a = alpha;
}
