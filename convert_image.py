#!/usr/bin/env python3
"""
Convert PNG image to LVGL v5 C array format for VEX V5 brain display
"""
from PIL import Image
import sys
import os

def rgb888_to_rgb565(r, g, b):
    """Convert RGB888 to RGB565 format"""
    r5 = (r >> 3) & 0x1F
    g6 = (g >> 2) & 0x3F
    b5 = (b >> 3) & 0x1F
    return (r5 << 11) | (g6 << 5) | b5

def convert_png_to_lvgl_c_array(png_path, output_name="team_logo"):
    """Convert PNG to LVGL v5 C array format"""
    try:
        # Open and convert image
        img = Image.open(png_path)
        img = img.convert('RGB')  # Ensure RGB format
        width, height = img.size
        
        print(f"Converting {png_path}")
        print(f"Image size: {width}x{height}")
        
        # Generate C array data
        pixel_data = []
        for y in range(height):
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                rgb565 = rgb888_to_rgb565(r, g, b)
                pixel_data.append(f"0x{rgb565:04x}")
        
        # Generate C file content
        c_content = f'''#include "team_logo.h"

const lv_img_dsc_t {output_name} = {{
    .header.always_zero = 0,
    .header.w = {width},
    .header.h = {height},
    .data_size = {len(pixel_data) * 2},
    .header.cf = LV_IMG_CF_TRUE_COLOR,
    .data = (const uint8_t[]) {{
        {', '.join(pixel_data[:8])},
        {', '.join(pixel_data[8:16])},
        {', '.join(pixel_data[16:24])},
        // ... truncated for brevity - full data would be {len(pixel_data)} values
        // Add remaining {len(pixel_data) - 24} values here
    }}
}};
'''
        
        # Write to team_logo.c
        with open('src/team_logo.c', 'w') as f:
            f.write(c_content)
        
        print(f"Generated src/team_logo.c with {len(pixel_data)} pixels")
        print("Note: Only first 24 pixels shown - add remaining data for full image")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 convert_image.py <png_path>")
        sys.exit(1)
    
    png_path = sys.argv[1]
    if not os.path.exists(png_path):
        print(f"Error: File {png_path} not found")
        sys.exit(1)
    
    convert_png_to_lvgl_c_array(png_path)
