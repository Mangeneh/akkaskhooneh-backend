import re

from PIL import Image
from django.core.exceptions import ValidationError


def validate_tag(tag_obj):
    if len(tag_obj) > 40 or not re.match(r'^\w+$', tag_obj):
        raise ValidationError("Tag is not valid.")


def validate_image(field_file_obj):
    file_size = field_file_obj.file.size
    megabyte_limit = 3.0
    if file_size > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" %
                              str(megabyte_limit))

    im = Image.open(field_file_obj.file)
    width, height = im.size
    if width > 1080 or height > 1080:
        raise ValidationError("Maximum file resolution is 1080.")
