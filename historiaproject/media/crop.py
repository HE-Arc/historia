import glob
from PIL import Image


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


for filename in glob.iglob('images/category/*.jpg', recursive=True):
    im = Image.open(filename)
    img = crop_center(im, 700, 350)
    img.save(filename, quality=95)
