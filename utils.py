import logging
from django.core.exceptions import ValidationError
from PIL import Image
from django.core.paginator import Paginator

logger = logging.getLogger('method')


def start_method_log(name, **kwargs):
    log = '({}) method started!'.format(name)
    if len(kwargs) != 0:
        log += '('
    for key in kwargs:
        log += ' {}: {}'.format(key, kwargs[key])
    if len(kwargs) != 0:
        log += ')'
    logger.info(log)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def validate_image(uploadedfile):

    filesize = uploadedfile.size
    megabyte_limit = 3.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" %
                              str(megabyte_limit))

    im = Image.open(uploadedfile)
    width, height = im.size
    if width > 1080 or height > 1080:
        raise ValidationError("Maximum file resolution is 1080.")


def paginator(queryset, limit=10, page=1):

    pages = Paginator(queryset, limit)
    result = pages.get_page(page)
    count = pages.count
    if result.has_next():
        next_page_number = result.next_page_number()
    else:
        next_page_number = None
    if result.has_previous():
        previous_page_number = result.previous_page_number()
    else:
        previous_page_number = None
    data = {
        "count": count,
        "next_page_number": next_page_number,
        "previous_page_number": previous_page_number,
        "result": result
    }

    return data
