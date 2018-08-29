import logging

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
