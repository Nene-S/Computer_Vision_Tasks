import cv2 as cv
import argparse
import matplotlib.pyplot as plt
import numpy as np

def rotate_image(image, theta=45):
    """
    A function to rotate an image by an angle theta.
    Parameters:
        image: Input image (numpy array)
        theta: Angle of rotation in degrees (default: 45 degrees)
    Returns:
        Rotated image
    """
    height, width = image.shape[:2]
    cx, cy = width // 2, height // 2
    theta = np.radians(theta)

    cos_theta, sin_theta = np.cos(theta), np.sin(theta)
    rotation_matrix = np.array([
        [cos_theta, -sin_theta, 0],
        [sin_theta, cos_theta, 0],
        [0, 0, 1]])
    
    corners = np.array([
        [0, 0, 1],         # Top-left
        [width, 0, 1],     # Top-right
        [0, height, 1],    # Bottom-left
        [width, height, 1] # Bottom-right
]).T

    rotated_corners = np.dot(rotation_matrix, corners)
    min_x, max_x = rotated_corners[0].min(), rotated_corners[0].max()
    min_y, max_y = rotated_corners[1].min(), rotated_corners[1].max()
    new_width = int(np.ceil(max_x - min_x))
    new_height = int(np.ceil(max_y - min_y))

    translation_matrix = np.array([
        [1, 0, -min_x],
        [0, 1, -min_y],
        [0, 0, 1]
    ])

    transformation_matrix = np.dot(translation_matrix, rotation_matrix)
    rotated_image = np.zeros((new_height, new_width, image.shape[2]), dtype=image.dtype)

    for x in range(new_width):
        for y in range(new_height):
            original_coords = np.linalg.inv(transformation_matrix) @ np.array([x, y, 1])
            orig_x, orig_y = int(original_coords[0]), int(original_coords[1])
            if 0 <= orig_x < width and 0 <= orig_y < height:
                rotated_image[y, x] = image[orig_y, orig_x]

    return rotated_image
 
def translate_image(image,shift=(10,4)):
    ''' A function to translate/shift an image about an x,y axis 
    parameter:
        image: input image
        shift: axis to shift image to
    returns:
        translated image
    '''
    tx, ty = shift
    height, width, channel = image.shape
    canvas_height, canvas_width = height + ty, width + tx
    translated = np.zeros((canvas_height, canvas_width, channel), dtype=image.dtype)

    scaling_matrix = np.array([[1, 0, tx], 
                               [0, 1, ty], 
                               [0, 0, 1]])
    for x in range(width):
        for y in range(height):
            coords = np.array([x, y, 1])
            new_coords = np.dot(scaling_matrix, coords)
            nx, ny = new_coords[0], new_coords[1] 
            if 0 <=  nx < canvas_width and 0 <= ny < canvas_height:
                translated[int(ny), int(nx)] = image[y, x]
    return translated

def scale_image(image, scale=(1,-0.5)):
    ''' A function to scale an image
    parameter:
        image: input image
        scale: axis of scaling
    returns:
        scaled image
    '''
    tx, ty = scale
    height, width = image.shape[:2]

    new_width = int(abs(width * tx))
    new_height = int(abs(height * ty))
    scaled = np.zeros((new_height, new_width, image.shape[2]), dtype=image.dtype)
    scaled_matrix = np.array([[tx, 0, 0], 
                               [0, ty, 0], 
                               [0, 0, 1]])
    for x in range(width):
        for y in range(height):
            coords = np.array([x, y, 1])
            new_coords = np.dot(scaled_matrix, coords)
            nx, ny = new_coords[0], new_coords[1] 

            if int(nx) < new_width and int(ny) < new_height:
                scaled[int(ny), int(nx)] = image[y, x]
    return scaled

def skew_image(image, skew=(0, 1)):
    """
    A function to skew/shear an image.
    Parameters:
        image: Input image (numpy array)
        skew: Tuple specifying the skew factors along x and y axes (sx, sy)
    Returns:
        Skewed image with adjusted canvas
    """
    sx, sy = skew
    height, width = image.shape[:2]
    skewing_matrix = np.array([[1, sx, 0],
                                [sy, 1, 0],
                                [0,  0, 1]])
    
    corners = np.array([
        [0, 0, 1],
        [width, 0, 1],      
        [0, height, 1],     
        [width, height, 1]  
    ]).T
    transformed_corners = np.dot(skewing_matrix, corners)
    min_x, max_x = transformed_corners[0].min(), transformed_corners[0].max()
    min_y, max_y = transformed_corners[1].min(), transformed_corners[1].max()

    new_width = int(np.ceil(max_x - min_x))
    new_height = int(np.ceil(max_y - min_y))

    translation_matrix = np.array([
        [1, 0, -min_x],
        [0, 1, -min_y],
        [0, 0, 1]
    ])

    transformation_matrix = np.dot(translation_matrix, skewing_matrix)
    skewed_image = np.zeros((new_height, new_width, image.shape[2]), dtype=image.dtype)


    for x in range(new_width):
        for y in range(new_height):
            original_coords = np.linalg.inv(transformation_matrix) @ np.array([x, y, 1])
            orig_x, orig_y = int(original_coords[0]), int(original_coords[1])

            if 0 <= orig_x < width and 0 <= orig_y < height:
                skewed_image[y, x] = image[orig_y, orig_x]

    return skewed_image
 
def affine_transformation(image, translate, scale, rotate=None):
    """
    Applies affine transformation on an image.
    Parameters:
        image: Input image (numpy array)
        translate: Translation (tx, ty)
        scale: Scaling factors (sx, sy)
        rotate: Optional. Rotation angle in degrees
    Returns:
        Transformed image with adjusted canvas
    """
    height, width = image.shape[:2]
    sx, sy = scale
    tx, ty = translate
    affine_matrix = None

    if rotate is not None:
        theta = np.radians(rotate)
        affine_matrix = np.array([
            [sx * np.cos(theta), -sy * np.sin(theta), tx],
            [sx * np.sin(theta),  sy * np.cos(theta), ty],
            [0, 0, 1]
        ])
    else:
        affine_matrix = np.array([
            [sx, 0, tx],
            [0, sy, ty],
            [0, 0, 1]
        ])

    corners = np.array([
        [0, 0, 1],          # Top-left
        [width, 0, 1],      # Top-right
        [0, height, 1],     # Bottom-left
        [width, height, 1]  # Bottom-right
    ]).T

    transformed_corners = np.dot(affine_matrix, corners)
    min_x, max_x = transformed_corners[0].min(), transformed_corners[0].max()
    min_y, max_y = transformed_corners[1].min(), transformed_corners[1].max()

    new_width = int(np.ceil(max_x - min_x))
    new_height = int(np.ceil(max_y - min_y))

    translation_matrix = np.array([
        [1, 0, -min_x],
        [0, 1, -min_y],
        [0, 0, 1]
    ])

    transformation_matrix = np.dot(translation_matrix, affine_matrix)

    transformed_image = np.zeros((new_height, new_width, image.shape[2]), dtype=image.dtype)

    for x in range(new_width):
        for y in range(new_height):
            original_coords = np.linalg.inv(transformation_matrix) @ np.array([x, y, 1])
            orig_x, orig_y = int(original_coords[0]), int(original_coords[1])

            if 0 <= orig_x < width and 0 <= orig_y < height:
                transformed_image[y, x] = image[orig_y, orig_x]

    return transformed_image

def main():
    parser = argparse.ArgumentParser(description="Apply various transformations on images")

    parser.add_argument("image", type=str, help="Path to the input image")
    parser.add_argument("transformation", type=str, choices=["rotate", "translate", "scale", "skew", "affine"], help="Type of transformation to apply")
    parser.add_argument("--theta", type=float, default=45, help="Angle for rotation (degrees)")
    parser.add_argument("--shift", type=int, nargs=2, default=(10, 4), help="Translation shift (tx, ty)")
    parser.add_argument("--scale", type=float, nargs=2, default=(1, -0.5), help="Scaling factors (sx, sy)")
    parser.add_argument("--skew", type=float, nargs=2, default=(0, 1), help="Skew factors (sx, sy)")
    parser.add_argument("--output", type=str, help= "Path to save transformed image")
    args = parser.parse_args()

    image = cv.imread(args.image)
    if image is None:
        print(f"Error: Unable to read image at {args.image}")
        return
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    if args.transformation == "rotate":
        transformed_image = rotate_image(image, theta=args.theta)
    elif args.transformation == "translate":
        transformed_image = translate_image(image, shift=args.shift)
    elif args.transformation == "scale":
        transformed_image = scale_image(image, scale=args.scale)
    elif args.transformation == "skew":
        transformed_image = skew_image(image, skew=args.skew)
    elif args.transformation == "affine":
        transformed_image = affine_transformation(image, translate=args.shift, scale=args.scale, rotate=args.theta)
    else:
        print("Invalid transformation type.")
        return

    plt.imshow(transformed_image)
    plt.title(f"{args.transformation.capitalize()} Transformation")
    plt.axis("off")
    plt.show()

    plt.imsave(args.output, transformed_image)
    print(f"Transformed image saved to {args.output}")

if __name__ == "__main__":
    main()
      