from django.core.files import File
from io import BytesIO
from PIL import Image
import os



class ImageCompression:
    @staticmethod
    def compress_image(image):
        """This method compress the image uploaded in jpg or png format to a webp in to system"""

        im = Image.open(image)
        if im.mode != "RGB":
            im = im.convert("RGB")
        im_io = BytesIO()
        im.save(im_io, "WEBP", quality=60, optimize=True)
        new_image = File(im_io, name=os.path.splitext(image.name)[0] + ".webp")

        return new_image

