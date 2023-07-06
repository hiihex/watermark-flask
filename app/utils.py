from app import ALLOWED_EXTENSIONS
from PIL import Image, ImageOps
import io
import os
import zipfile

CURRENT_PATH = os.path.dirname(__file__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def watermark_image(image: bytes, watermark: bytes) -> bytes:
    watermark_image_path = CURRENT_PATH + '/static/irish-reps-logo.png'
    watermark_logo = Image.open(io.BytesIO(watermark))
    watermark_size = 240, 130
    watermark_logo = ImageOps.contain(watermark_logo, watermark_size)

    image = Image.open(io.BytesIO(image))
    image_crop_size = 1080, 1080

    cropped = image.resize(image_crop_size)

    cropped.paste(watermark_logo, (40, cropped.height - watermark_logo.height - 40), watermark_logo)

    final_image = io.BytesIO()
    cropped.save(final_image, format='PNG')
    final_image = final_image.getvalue()

    return final_image


def create_zip_file(files, watermark):
    zip_bytes = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_bytes, mode='w')

    for file in files:
        zip_file.writestr(file.filename, watermark_image(file.read(), watermark[0].read()))

    zip_file.close()
    zip_bytes.seek(0)

    return zip_bytes
