#version 450 core

in vec2 UV;
in vec3 NORMAL;
in vec3 COLOR;
in float STATE;
in float ALPHA;

uniform sampler2D tex;

out vec4 output_color;

void main()
{
    vec2 offset = vec2(
        mod(STATE, 256.001) / 256.0 ,
        1 - floor(STATE / (256.0 - 0.0001)) * 97.0 / 512.0 + 0.0001
    );
    vec4 diff = texture(tex, UV + offset).rgba;
    output_color = vec4(diff.xyz*pow(diff.a,1) + COLOR*(1-pow(diff.a,0.5)), 1);
    output_color.a = ALPHA;
}