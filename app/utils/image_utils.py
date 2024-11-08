from PIL import Image
import io

def change_image_format(image_stream, output_format):
    """Convert an image to the specified output format."""
    image = Image.open(image_stream)
    img_byte_arr = io.BytesIO()
    image.convert("RGB").save(img_byte_arr, format=output_format.upper())
    img_byte_arr.seek(0)
    return img_byte_arr
