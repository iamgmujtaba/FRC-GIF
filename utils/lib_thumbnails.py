import os
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array, load_img

def extract_thumbnails(container_path, thumb_path):
    # Count files in the container directory
    _, _, files = next(os.walk(container_path))
    file_count = len(files)
    print("Extracting frames from containers: %s" % file_count)

    print("Processing...")
    # Thumbnail Size
    crop_width = 160
    crop_height = 90

    frame_number = 0

    # Load all images in the directory
    for image_name in os.listdir(container_path):
        start_y = 0
        start_x = 0

        filename = os.path.splitext(image_name)[0]  # filename without extension

        img = np.array(Image.open(os.path.join(container_path, image_name)))
        for i in range(25):
            crop = img[start_y:start_y + crop_height, start_x:start_x + crop_width, :]
            Image.fromarray(crop).save(os.path.join(thumb_path, f"{filename}_{i+1}.jpg"))

            start_x += crop_width
            if i in {4, 9, 14, 19}:
                start_x = 0
                start_y += crop_height

        frame_number += 1
    print("containers_path %s : thumbanils_path %s" % (container_path, thumb_path))
    print('thumbnails extraction process completed')

# Process an image to be passed to networks
def process_image(image_path, target_shape):
    """Given an image, process it and return the array."""
    # Load and resize the image.
    height, width, _ = target_shape
    image = load_img(image_path, target_size=(height, width))

    # Convert to numpy array, normalize, and return.
    img_array = img_to_array(image)
    processed_image = (img_array / 255.).astype(np.float32)

    return processed_image

