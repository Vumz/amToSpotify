import envVariables
import urllib
from flask import request
import requests
import base64
import json


#API client keys
clientID = envVariables.clientID
clientSecret = envVariables.clientSecret

#URLS
spotifyAuthURL = 'https://accounts.spotify.com/authorize'
spotifyTokenURL = 'https://accounts.spotify.com/api/token'

#payload parameters
redirectURI = 'http://127.0.0.1:8080/login'
scope = 'playlist-modify-public'

#header for requesting tokens
authHeader = {'Authorization':
        'Basic {}'.format(base64.b64encode('{}:{}'.format(clientID, clientSecret)))}
        #or {'Authorization': 'Basic {}'.format(('{}:{}'.format(clientID, clientSecret)).encode('base64', 'strict'))}


#returns authentication URL
def getAuthURL():
    authPayload = {'client_id': clientID,
                       'response_type': 'code',
                       'redirect_uri': redirectURI,
                       'scope': scope}
    urlparams = urllib.urlencode(authPayload)
    return '{}/?{}'.format(spotifyAuthURL, urlparams)


#returns dictionary of authentication tokens
def getAuthTokens():
    authCode = request.args.get('code')
    if not authCode:
        return None
    authPayload = {'grant_type': 'authorization_code',
                       'code': authCode,
                       'redirect_uri': redirectURI}
    postResponse = requests.post(spotifyTokenURL, headers=authHeader, data=authPayload)
    return json.loads(postResponse.text)


#returns a dictionary of the access header
def getAccessHeader(tokenData):
    accessToken = tokenData['access_token']
    return {'Authorization': 'Bearer {}'.format(accessToken)}

#returns a dictionary of updated authentication tokens
def refreshTokens(tokenData):
    authPayload = {'grant_type': 'refresh_token',
                       'refresh_token': tokenData['refresh_token']}
    postResponse = requests.post(spotifyTokenURL, header=authHeader, data=authPayload)
    return json.loads(postResponse.text)
