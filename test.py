import sys
import weibo
import webbrowser

APP_KEY = 'your key'
MY_APP_SECRET = 'your secret'
REDIRECT_URL = 'your redirect url'

api = weibo.APIClient(APP_KEY, MY_APP_SECRET)

authorize_url = api.get_authorize_url(REDIRECT_URL)

print(authorize_url)

webbrowser.open_new(authorize_url)

code = raw_input()

request = api.request_access_token(code, REDIRECT_URL)

access_token = request.access_token

expires_in = request.expires_in

api.set_access_token(access_token, expires_in)

print(api.statuses__public_timeline())

