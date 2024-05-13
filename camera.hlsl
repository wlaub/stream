float4 render(float2 uv){
    float4 rgba = image.Sample(builtin_texture_sampler, uv);
    rgba.r=1-rgba.r;
    rgba.g=1-rgba.g;
    rgba.b=1-rgba.b;
    if(rgba.a < .02 || rgba.r < 0.9)
    {
    //    rgba.a= 0;
    }
    else
    {
    rgba.a=rgba.a*3;
    
    }
    
    return rgba;
}

