import logging
# django提供的数据库异常
from django.db import DatabaseError
# redis异常
from redis.exceptions import RedisError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


# 获取在配置文件中定义的日志器，用来记录日志信息
logger = logging.getLogger('django')


def custom_exception_handler(exc, context):
    """
    自定义异常处理，补充处理mysql异常和redis异常
    :param exc: 异常对象
    :param context: 抛出异常额上下文
    :return: Response
    """
    # 先调用drf框架的异常处理方法
    response = exception_handler(exc, context)

    # drf框架处理不了的异常，我们再处理
    if not response:
        view = context['view']   # 出错的视图，即本次用户访问的视图对象
        if isinstance(exc, DatabaseError) or isinstance(exc,RedisError):
            # 数据库异常
            logger.error('[%s] : %s' % (view, exc))
            response = Response({'message': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

    return response

