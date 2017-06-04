import base64
import urllib

import requests

demo_url = 'https://account-d.docusign.com'
live_url = 'https://account.docusign.com'


class Docusign:
    def __init__(self, client_id='', secret_key='', server_type='live', access_token='', refresh_token=''):
        self.client_id = client_id
        self.secret_key = secret_key
        self.basic_auth_token = base64.b64encode(self.client_id + ":" + self.secret_key)
        self.auth_url = '/oauth/auth?'
        self.token_url = '/oauth/token'
        self.user_info_url = '/oauth/userinfo'
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_type = 'Bearer'
        if server_type == 'demo':
            self.base_url = demo_url
        else:
            self.base_url = live_url

    def get_autheniation_url(self, redirect_uri, scope='signature', state='1', response_type='code'):
        return self.base_url + self.auth_url + "response_type=" + response_type + "&scope=" + scope + "&client_id=" + self.client_id + "&state=" + state + "&redirect_uri=" + redirect_uri

    def get_access_token(self, code='', grant_type='authorization_code'):
        url = self.base_url + self.token_url
        data = {
            "grant_type": grant_type,
            "code": code,
            "refresh_token": self.refresh_token
        }
        headers = {
            "Authorization": "Basic " + self.basic_auth_token,
            "content-type": "application/x-www-form-urlencoded"
        }
        responds = requests.post(url, urllib.urlencode(data), headers=headers)
        if responds.status_code == 200:
            self.access_token = responds.json().get('access_token')
            self.refresh_token = responds.json().get('refresh_token')
            self.token_type = responds.json().get('token_type')
            return responds.json()
        else:
            return "Invalid credentials"

    def refresh_access_token(self):
        return self.get_access_token(grant_type='refresh_token')

    def user_info(self):
        url = self.base_url + self.user_info_url
        if not self.access_token:
            return "Enter access token to get user info"
        headers = {
            "Authorization": self.token_type + " " + self.access_token
        }
        responds = requests.get(url, headers=headers)
        if responds.status_code == 200:
            return responds.json()
        else:
            return "Invalid token or token expired. Refreshyour token"
