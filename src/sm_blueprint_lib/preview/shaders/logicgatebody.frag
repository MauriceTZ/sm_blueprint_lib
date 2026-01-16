#version 450 core

in vec2 UV;
in vec3 COLOR;
in float ALPHA;

uniform sampler2D tex;

out vec4 output_color;

void main()
{
    vec4 diff = texture(tex, UV);
    output_color = diff + vec4(COLOR, 1) * (1 - diff.a);
    output_color.a = ALPHA;
}