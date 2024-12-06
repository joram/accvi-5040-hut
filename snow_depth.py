import os

import cv2
import numpy as np

POLE_BOTTOM = (2055, 1563)
POLE_TOP =  (2105, 945)

def debug_img(image_path, depth_percent):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to load.")



    debug_image = image.copy()
    bx, by = 2050, 1521
    tx, ty = 2050, 945
    length = by-ty
    segment_length = length/6+7
    width = 80

    def draw_segment_guides():
        y1 = ty
        y2 =y1+int(segment_length)
        y3 = y2+int(segment_length)
        y4 = y3+int(segment_length)
        y5 = y4+int(segment_length)
        y6 = y5+int(segment_length)
        y7 = y6+int(segment_length)
        segments = [
            (bx, y1, bx, y2),
            (bx, y2, bx, y3),
            (bx, y3, bx, y4),
            (bx, y4, bx, y5),
            (bx, y5, bx, y6),
            (bx, y6, bx, y7),
        ]

        colours = [
            (155,0,0),
            (0,155,0),
            (0,0,155),
            (155,0,0),
            (0,155,0),
            (0,0,155),
        ]
        for i in range(0, len(segments)):
            segment = segments[i]
            colour = colours[i]
            cv2.line(debug_image, (segment[0], segment[1]), (segment[2], segment[3]), colour, 1)
            # cv2.line(debug_image, (segment[0]+width, segment[1]), (segment[2]+width, segment[3]), colour, 1)

    def draw_pole():
        cv2.line(debug_image, POLE_TOP, POLE_BOTTOM, (0, 0, 255), 2)

    def draw_estimated_snow_depth_line():
        # Draw the snow depth
        snow_depth = int(depth_percent * length)
        x, y = POLE_BOTTOM
        y -= snow_depth
        colour = (0, 0, 255)
        # Draw the snow depth
        # cv2.line(debug_image, (0, y), (x-5,y), colour, 2)
        cv2.line(debug_image, (x+width, y), (x+int(width*2),y), colour, 2)

    def draw_snow_depth_text():
        cv2.rectangle(debug_image, (0, by+60), (bx+width*2, by+120), (255, 255, 255), -1)
        cv2.putText(
            debug_image,
            f"est. {round(depth_percent*600, 2)}cm",
            (bx-40, by+85),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 0, 0),
            2,
            cv2.LINE_AA,
        )

    draw_segment_guides()
    # draw_pole()
    draw_estimated_snow_depth_line()
    draw_snow_depth_text()

    buffer = 50
    text_room = 50
    debug_image = debug_image[ty-buffer:by+buffer+text_room, bx-buffer:bx+width+buffer]

    snow_depth_filepath = image_path.replace(".jpg", "_snow_depth.jpg")
    if os.path.exists(snow_depth_filepath):
        os.remove(snow_depth_filepath)
    cv2.imwrite(snow_depth_filepath, debug_image)

    snow_depth_cm = 0
    return snow_depth_cm

def walk_along_pole(image_path, bottom, top, debug=False):

    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to load.")

    # Get the dimensions of the image
    height, width, _ = image.shape

    # Ensure coordinates are within image bounds
    bottom = (min(max(bottom[0], 0), width - 1), min(max(bottom[1], 0), height - 1))
    top = (min(max(top[0], 0), width - 1), min(max(top[1], 0), height - 1))

    # Compute the line from bottom to top
    num_points = max(abs(bottom[0] - top[0]), abs(bottom[1] - top[1])) + 1
    x_coords = np.linspace(bottom[0], top[0], num_points).astype(int)
    y_coords = np.linspace(bottom[1], top[1], num_points).astype(int)

    # Read pixel colors along the line
    pixel_colors = [image[y, x].tolist() for x, y in zip(x_coords, y_coords)]

    return pixel_colors


def calc_snow_depth(image_path):
    fudge_factor = 5
    snow_brightness_threshold = 200
    snow_brightness_buffer = 5
    pixels = walk_along_pole(image_path, POLE_BOTTOM, POLE_TOP, debug=True)
    last_bright_pixel = 0
    num_dark_pixels = 0
    for i, color in enumerate(pixels):
        weight = sum(color)
        print(f"Segment {i + 1}: {weight} {color}")
        if weight > snow_brightness_threshold:
            last_bright_pixel = i
            continue

        num_dark_pixels += 1
        if num_dark_pixels > snow_brightness_buffer:
            ratio = (last_bright_pixel+fudge_factor)/len(pixels)
            return ratio
    return 0


def list_files(directory, extension):
    return [f for f in os.listdir(directory) if f.endswith(extension)]


# Example usage
for file in list_files('./data/webcam', '.jpg'):
    if "snow_depth" in file:
        continue
    image_filepath = os.path.abspath(os.path.join('data/webcam', file))
    ratio = calc_snow_depth(image_filepath)
    debug_img(image_filepath, ratio)

    depth = 600 * ratio
    print(f"Snow depth: {round(depth, 2)} cm")
