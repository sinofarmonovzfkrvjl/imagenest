from PIL import Image
import io

def image_to_bytes(image_path):
    with Image.open(image_path) as img:
        img_byte_arr = 