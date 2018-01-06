from __future__ import print_function
import sys
import plistlib
from flask import request
import requests
import json
import time



spotifyAPIURL = "https://api.spotify.com/v1"

#returns dictionary of songs(key) and artists(value)
def getAppleMusic(xmlItunes, playlist):
    itunesLib = plistlib.readPlist(xmlItunes)
    with open('failure.txt', 'w') as fail:
        trackIDs = [str(key['Track ID'])
                        for playlist in itunesLib['Playlists']
                            if playlist['Name'] == 'Drive'
                                for key in playlist['Playlist Items']]
        songs = {}
        for trackID in trackIDs:
            try:
                songs[(itunesLib['Tracks'][trackID]['Name']).encode('utf-8')] = (itunesLib['Tracks'][trackID]['Artist']).encode('utf-8')
            except:
                fail.write(itunesLib['Tracks'][trackID]['Name'] + "\n")
    return songs

#returns a list of the Spotify trackIDs from the songs dictionary passed in
def getTrackURIs(songs, accessHeader):
    trackEndpoint = "{}/search".format(spotifyAPIURL)
    trackPayload = {'type': 'track',
                       'limit': 1,
                       'offset': 0}
    trackList = []
    with open('failure.txt', 'a') as fail:
        for song, artist in songs.iteritems():
            trackPayload['q'] = '{} artist:{}'.format(song, artist)
            getResponse = requests.get(trackEndpoint, params=trackPayload, headers=accessHeader)
            trackData = json.loads(getResponse.text)
            try:
                #checks if the track can be found by exluding the features
                if (trackData['tracks']['items'] == []):
                    songF = getNoFeat(song)
                    if songF:
                        trackPayload['q'] = '{} artist:{}'.format(songF, artist)
                        getResponse = requests.get(trackEndpoint, params=trackPayload, headers=accessHeader)
                        trackData = json.loads(getResponse.text)
                #checks if the track can be found with a single artist
                if (trackData['tracks']['items'] == []):
                    artistS = getSingleArtist(artist)
                    if artistS:
                        trackPayload['q'] = '{} artist:{}'.format(song, artistS)
                        getResponse = requests.get(trackEndpoint, params=trackPayload, headers=accessHeader)
                        trackData = json.loads(getResponse.text)
                #if getResponse.status_code == 429:
                    #time.sleep(retry after seconds)
                    # need to handle when the API rate limit is reached^
                #adds the trackID to trackList
                trackList.append(trackData['tracks']['items'][0]['uri'])
            except:
                print(trackData)
                fail.write(song + "-" + artist + "\n")
    return trackList


def getNoFeat(song):
    index = song.find('(feat.')
    if(index > -1):
        return song[:index]
    index = song.find('[feat.')
    if(index > -1):
        return song[:index]
    return None

def getSingleArtist(artist):
    index = artist.find(',')
    if(index > -1):
        return artist[:index]
    index = artist.find('&')
    if(index > -1):
        return artist[:index]
    return None
