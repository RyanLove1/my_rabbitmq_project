# 
# coding=utf8
import datetime
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _

from django.core.cache import cache

EXPIRE_MINUTES = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES', 1)


class ExpiringTokenAuthentication(TokenAuthentication):
    """Set up token expired time"""

    def authenticate_credentials(self, key):
        # Search token in cache
        cache_user = cache.get(key)
        if cache_user:
            return (cache_user, key)

        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        # 获取当前时间
        time_now = datetime.datetime.now()

        if key[:4] == 'WXD-':
            if token.created <= time_now - datetime.timedelta(minutes=60*24*7):#过期时间
                token.delete()
                # raise exceptions.AuthenticationFailed(_('Token has expired then delete.'))
                raise exceptions.AuthenticationFailed(_('登录过期,重新登录!'))
        else:
            if token.created < time_now - datetime.timedelta(minutes=EXPIRE_MINUTES):
                token.delete()
                # raise exceptions.AuthenticationFailed(_('Token has expired then delete.'))
                raise exceptions.AuthenticationFailed(_('登录过期,重新登录!'))

        if token:
            # Cache token
            cache.set(key, token.user, EXPIRE_MINUTES * 60)

        return (token.user, token)
#