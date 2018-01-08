from flask import Flask, request, redirect, url_for
import auth
import envVariables as eVar
import webbrowser
import ast
import processing



itunesXMLFile = 'itunes Music Library.xml'
playlist = 'Drive'

app = Flask(__name__)

@app.route('/')
def index():
    authURL = auth.getAuthURL()
    return redirect(authURL)

@app.route('/login')
def login():
    tokenData = auth.getAuthTokens()
    #if not accessToken:
        #go back to login page
    return redirect(url_for('convert', tokenData=tokenData))

@app.route('/convert')
def convert():
    tokenData = ast.literal_eval(request.args.get('tokenData'))
    accessHeader = auth.getAccessHeader(tokenData)
    itunesSongs = processing.getAppleMusic(itunesXMLFile, playlist)
    trackURIs = processing.getTrackURIs(itunesSongs, accessHeader)
    if processing.addToPlaylist(trackURIs, playlist, accessHeader):
        return "Success"
    return "Failed"

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8080/')
    app.run(debug=False,port=8080)