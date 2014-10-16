import uuid
import logging
import json 
from urllib import urlencode


from social_auth.backends import BaseOAuth2, OAuthBackend
from social_auth.utils import dsa_urlopen
import requests


logger = logging.getLogger(__name__)


class QQBackend(OAuthBackend):
    name = 'qq'
    EXTRA_DATA = [
        ('figureurl_2', 'figureurl_2'),
    ]

    def get_user_id(self, details, response):
        return 'QQ' + str(uuid.uuid4())

    def get_user_details(self, response):
        return {
            'username': response.get('nickname', ''),
            'first_name': response.get('nickname', '')
        }


class QQAuth(BaseOAuth2):
    AUTHORIZATION_URL = 'https://graph.qq.com/oauth2.0/authorize'
    ACCESS_TOKEN_URL = 'https://graph.qq.com/oauth2.0/token'
    AUTH_BACKEND = QQBackend
    SETTINGS_KEY_NAME = 'QQ_CLIENT_KEY'
    SETTINGS_SECRET_NAME = 'QQ_CLIENT_SECRET'
    REDIRECT_STATE = False

    def user_data(self, access_token, *args, **kwargs):
        url = 'https://graph.qq.com/user/get_user_info'
        try:
            data = requests.get(url, params={
                'access_token': access_token
            }).json()
            logger.debug(data)
            return data
        except (ValueError, KeyError, IOError):
            logger.exception()
            return None

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        self.process_error(self.data)
        params = self.auth_complete_params(self.validate_state())

        from urllib2 import Request
        request = Request(self.ACCESS_TOKEN_URL, data=urlencode(params),
                          headers=self.auth_headers())

        try:
            result = dsa_urlopen(request).read()
            import urlparse
            response = urlparse.parse_qs(result)
        except HTTPError, e:
            if e.code == 400:
                raise AuthCanceled(self)
            else:
                raise
        except (ValueError, KeyError):
            raise AuthUnknownError(self)

        self.process_error(response)
        return self.do_auth(response['access_token'], response=response,
                            *args, **kwargs)


BACKENDS = {
    'qq': QQAuth
}
