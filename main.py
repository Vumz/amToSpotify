from flask import Flask, request, redirect
import auth
import envVariables as eVar
import plistlib
import webbrowser

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
    return url_for('convert', tokenData)

@app.route('/convert')
def convert():
    accessHeader = auth.getAccessHeader(tokenData)

'''
xmlItunes = "itunes Music Library.xml"
itunesLib = plistlib.readPlist(xmlItunes)

with open("failure.txt", "w") as fail:
    with open("success.txt", "w") as success:
        for track, details in itunesLib['Tracks'].items():
            try:
                if (details.get("Kind") == "Apple Music AAC audio file"):
                    success.write(details.get("Name").encode("ascii", "ignore") + " , " + details.get("Artist").encode("ascii", "ignore") + "\n")
            except:
                fail.write(details.get("Name").encode("ascii", "ignore") + " , " + details.get("Artist").encode("ascii", "ignore") + "\n")
                print "something went wrong with the iTunes library XML parsing"
'''

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8080/')
    app.run(debug=True,port=8080)