#version 450 core

in vec2 UV;
in vec3 NORMAL;
in vec3 COLOR;
in float ALPHA;

uniform sampler2D tex;

out vec4 output_color;

void main()
{
    vec4 diff = texture(tex, UV);
    // Take the default color of timers (0xDF7F01)
    output_color = diff + vec4(COLOR - vec3(0.8745098039215686, 0.4980392156862745, 0.00392156862745098), 1) * (1 - diff.a);
    output_color.a = ALPHA;
}