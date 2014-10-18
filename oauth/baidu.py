import logging
import json 
from urllib import urlencode
from urllib2 import Request, HTTPError

from social_auth.utils import dsa_urlopen
from social_auth.exceptions import AuthCanceled
from social_auth.backends import BaseOAuth2, OAuthBackend
from social_auth.exceptions import SocialAuthBaseException
import requests


logger = logging.getLogger(__name__)


class BaiduBackend(OAuthBackend):
    name = 'baidu'
    EXTRA_DATA = [
        ('portrait', 'portrait'),
    ]

    def get_user_id(self, details, response):
        try:
            return response['userid']
        except:
            raise SocialAuthBaseException('fail to get userid')

    def get_user_details(self, response):
        logger.debug(str(response))
        return {
            'username': response.get('username', ''),
            'first_name': response.get('realname', '')
        }


class BaiduAuth(BaseOAuth2):
    AUTHORIZATION_URL = 'https://openapi.baidu.com/oauth/2.0/authorize'
    ACCESS_TOKEN_URL = 'https://openapi.baidu.com/oauth/2.0/token'
    AUTH_BACKEND = BaiduBackend
    SETTINGS_KEY_NAME = 'BAIDU_CLIENT_KEY'
    SETTINGS_SECRET_NAME = 'BAIDU_CLIENT_SECRET'
    REDIRECT_STATE = False

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        self.process_error(self.data)
        params = self.auth_complete_params(self.validate_state())
        request = Request(self.ACCESS_TOKEN_URL, data=urlencode(params),
                          headers=self.auth_headers())

        try:
            result = dsa_urlopen(request).read()
            logger.debug('result: %s', result)
            response = json.loads(result)
        except HTTPError, e:
            logger.debug('code: %d, reason: %s', e.code, e.reason)
            logger.debug('error result: %s', e.read())
            if e.code == 400:
                raise AuthCanceled(self)
            else:
                raise
        except (ValueError, KeyError):
            raise AuthUnknownError(self)

        self.process_error(response)
        return self.do_auth(response['access_token'], response=response,
                            *args, **kwargs)

    def user_data(self, access_token, *args, **kwargs):
        url = 'https://openapi.baidu.com/rest/2.0/passport/users/getInfo'
        try:
            data = requests.get(url, params={
                'access_token': access_token
            }).json()
            logger.debug(data)
            return data
        except: 
            logger.exception('hydra!')
            return {}


BACKENDS = {
    'baidu': BaiduAuth
}
