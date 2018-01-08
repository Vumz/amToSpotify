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
                fail.write(itunesLib['Tracks'][trackID]['Name'] + '\n')
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
            retries = 2
            while retries > 0:
                try:
                    #requests for track details from Spotify API
                    trackPayload['q'] = '{} artist:{}'.format(song, artist)
                    getResponse = requests.get(trackEndpoint, params=trackPayload, headers=accessHeader)
                    trackData = json.loads(getResponse.text)
                    #checks if the track can be found by exluding the features
                    if (trackData['tracks']['items'] == []):
                        songF = getNoFeat(song)
                        if songF is not None:
                            trackPayload['q'] = '{} artist:{}'.format(songF, artist)
                            getResponse = requests.get(trackEndpoint, params=trackPayload, headers=accessHeader)
                            trackData = json.loads(getResponse.text)
                    #checks if the track can be found with a single artist
                    if (trackData['tracks']['items'] == []):
                        artistS = getSingleArtist(artist)
                        if artistS is not None:
                            trackPayload['q'] = '{} artist:{}'.format(song, artistS)
                            getResponse = requests.get(trackEndpoint, params=trackPayload, headers=accessHeader)
                            trackData = json.loads(getResponse.text)
                    #if getResponse.status_code == 429:
                        #time.sleep(retry after seconds)
                        # need to handle when the API rate limit is reached^
                    #adds the trackID to trackList
                    trackList.append(trackData['tracks']['items'][0]['uri'])
                    retries = 0
                except:
                    print(trackData)
                    retries -= 1
                    #retry track details request in case there was a bad gateway error
                    if retries > 0:
                        continue
                    #write to track to failure file if the track cannot be found
                    fail.write(song + "-" + artist + "\n")
    return trackList

#returns True if the the tracks were added to the user's playlist, False if not
def addToPlaylist(trackIDs, playlist, accessHeader):
    #gets user's playlists data
    userPEndpoint = "{}/me/playlists".format(spotifyAPIURL)
    getResponse = requests.get(userPEndpoint, headers=accessHeader)
    playlistData = json.loads(getResponse.text)
    try:
        #gets the playlist ID (of the playlist the user entered) and Owner ID
        itemNum = [pos for pos in xrange(len(playlistData['items']))
                            if (playlist.lower() == (playlistData['items'][pos]['name']).lower())][0]
        playlistID = playlistData['items'][itemNum]['id']
        userID = playlistData['items'][itemNum]['owner']['id']
    except:
        print("something went wrong, make sure the playlist you entered is existing in your account")
        return False
    playlistEndpoint = "{}/users/{}/playlists/{}/tracks".format(spotifyAPIURL, userID, playlistID)
    tempHeader = {'Authorization': accessHeader['Authorization'],
                    'Content-Type': 'application/json'}
    lastI = 0
    #adds the tracks with valid IDs from the itunes xml to the user's selected playlist (in increments of a 100)
    for i in xrange(0, len(trackIDs), 100):
        playlistPayload = {'uris': trackIDs[lastI:i]}
        lastI = i
        postResponse = requests.post(playlistEndpoint, headers=tempHeader, data=json.dumps(playlistPayload))
    #adds the remaining tracks to the user's selected playlist
    if ((len(trackIDs) - lastI) > 0):
        playlistPayload = {'uris': trackIDs[lastI:]}
        postResponse = requests.post(playlistEndpoint, headers=tempHeader, data=json.dumps(playlistPayload))
    return True

#returns the string of the track without the feature section
def getNoFeat(song):
    index = song.find('(feat.')
    if(index > -1):
        return song[:index]
    index = song.find('[feat.')
    if(index > -1):
        return song[:index]
    return None

#returns the string of the first artist
def getSingleArtist(artist):
    index = artist.find(',')
    if(index > -1):
        return artist[:index]
    index = artist.find('&')
    if(index > -1):
        return artist[:index]
    return None



