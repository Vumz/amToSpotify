from flask import Flask, request, redirect, url_for
import auth
import envVariables as eVar
import webbrowser
import ast
import processing



itunesXMLFile = 'itunes Music Library.xml'
playlistApple = 'Drive'
playlistSpotify = 'Drive'

app = Flask(__name__)

@app.route('/')
def index():
    #directs the user to the spotify authentication url to request permission
    authURL = auth.getAuthURL()
    return redirect(authURL)

@app.route('/login')
def login():
    #gets token data from the authentication callback
    tokenData = auth.getAuthTokens()
    return redirect(url_for('convert', tokenData=tokenData))

@app.route('/convert')
def convert():
    try:
        #get the tokenData from the url
        tokenData = ast.literal_eval(request.args.get('tokenData'))
    except ValueError as v:
        #if user cancels spotify authentication, return them to the authentication page again
        return redirect('http://127.0.0.1:8080/')
    accessHeader = auth.getAccessHeader(tokenData)
    itunesSongs = processing.getAppleMusic(itunesXMLFile, playlistApple)
    trackURIs = processing.getTrackURIs(itunesSongs, accessHeader)
    if processing.addToPlaylist(trackURIs, playlistSpotify, accessHeader):
        return "Success"
    return "Failed"

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8080/')
    app.run(debug=False,port=8080)