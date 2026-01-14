#version 450 core

in vec2 UV;
in vec3 COLOR;
in float STATE;
in float TYPE;
in float ALPHA;

uniform sampler2D tex;

out vec4 output_color;

void main()
{
    vec2 offset = vec2(0.1666670 * TYPE, -0.16450 * STATE);
    vec4 diff = texture(tex, UV + offset);
    output_color = diff + vec4(COLOR, 1) * (1 - diff.a);
    output_color.a = ALPHA;
}