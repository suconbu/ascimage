#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_RESIZE_IMPLEMENTATION
#include "stb_image_resize.h"

extern "C" {

unsigned char* load_image(const char* filename, int* width_out, int* height_out, int channels)
{
    int n = 0;
    return stbi_load(filename, width_out, height_out, &n, channels);
}

float* load_imagef(const char* filename, int* width_out, int* height_out, int channels)
{
    int n = 0;
    return stbi_loadf(filename, width_out, height_out, &n, channels);
}

int resize_image(
    const unsigned char* input, int input_width, int input_height, int input_row_stride,
    unsigned char* output, int output_width, int output_height, int output_row_stride,
    int channels)
{
    return stbir_resize_uint8(
        input, input_width, input_height, input_row_stride,
        output, output_width, output_height, output_row_stride,
        channels);
}

int resize_imagef(
    const float* input, int input_width, int input_height, int input_row_stride,
    float* output, int output_width, int output_height, int output_row_stride,
    int channels)
{
    return stbir_resize_float(
        input, input_width, input_height, input_row_stride,
        output, output_width, output_height, output_row_stride,
        channels);
}

void free_image(void* data)
{
    stbi_image_free(data);
}

} // extern "C"
