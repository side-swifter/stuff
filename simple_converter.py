#!/usr/bin/env python3
"""
Simple PNG to LVGL v5 C array converter using only built-in libraries
Creates a small test image for brain flash display
"""

def create_test_brain_flash():
    """Create a simple test image as C array for brain flash"""
    # Create a simple 64x64 test pattern (brain flash placeholder)
    width, height = 64, 64
    
    # Generate simple gradient pattern
    pixel_data = []
    for y in range(height):
        for x in range(width):
            # Create a simple pattern - white center fading to blue
            center_x, center_y = width // 2, height // 2
            dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            max_dist = (width // 2)
            
            if dist < max_dist * 0.3:
                # White center
                r, g, b = 255, 255, 255
            elif dist < max_dist * 0.7:
                # Blue ring
                r, g, b = 0, 100, 255
            else:
                # Dark blue edge
                r, g, b = 0, 50, 150
            
            # Convert to RGB565
            r5 = (r >> 3) & 0x1F
            g6 = (g >> 2) & 0x3F
            b5 = (b >> 3) & 0x1F
            rgb565 = (r5 << 11) | (g6 << 5) | b5
            pixel_data.append(f"0x{rgb565:04x}")
    
    # Generate C file content
    c_content = f'''#include "team_logo.h"

const lv_img_dsc_t team_logo = {{
    .header = {{
        .always_zero = 0,
        .w = {width},
        .h = {height},
        .cf = LV_IMG_CF_TRUE_COLOR
    }},
    .data_size = {len(pixel_data) * 2},
    .data = (const uint8_t[]) {{
'''
    
    # Add pixel data in rows of 8
    for i in range(0, len(pixel_data), 8):
        row = pixel_data[i:i+8]
        c_content += f"        {', '.join(row)},\n"
    
    c_content += '''    }
};
'''
    
    # Write to team_logo.c
    with open('src/team_logo.c', 'w') as f:
        f.write(c_content)
    
    print(f"Generated src/team_logo.c with {width}x{height} test brain flash image")
    print("This creates a white center with blue gradient - replace with actual converted image data")

if __name__ == "__main__":
    create_test_brain_flash()
