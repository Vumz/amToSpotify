from __future__ import print_function
import sys
import plistlib
from flask import request
import requests
import json



spotifyAPIURL = "https://api.spotify.com/v1"

#returns dictionary of songs(key) and artists(value)
def getAppleMusic(xmlItunes, playlist):
    itunesLib = plistlib.readPlist(xmlItunes)
    with open("failure.txt", "w") as fail:
        trackIDs = [str(key['Track ID'])
                        for playlist in itunesLib['Playlists']
                            if playlist['Name'] == 'Drive'
                                for key in playlist['Playlist Items']]
        songs = {}
        for trackID in trackIDs:
            try:
                songs[itunesLib['Tracks'][trackID]['Name']] = itunesLib['Tracks'][trackID]['Artist']
                # songs[(itunesLib['Tracks'][trackID]['Name']).encode("ascii", "ignore")] =
                #             (itunesLib['Tracks'][trackID]['Artist']).encode("ascii", "ignore")
            except:
                fail.write(itunesLib['Tracks'][trackID]['Name'] + "\n")
    return songs

def getTrackURIs(songs, accessHeader):
    trackEndpoint = "{}/search".format(spotifyAPIURL)
    trackPayload = {'type': 'track',
                       'limit': 1,
                       'offset': 0}
    trackList = []
    for song, artist in songs:
        trackPayload['q'] = '{} artist:{}'.format(song, artist)
        getResponse = requests.get(trackEndpoint, params=trackPayload, headers=accessHeader)
        trackData = json.loads(getResponse.text)
        trackList = trackList.append(trackData['tracks']['items']['uri'])

'''
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