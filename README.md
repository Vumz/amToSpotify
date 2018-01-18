# amToSpotify -  Music to Spotify playlist converter

## Description

This application converts a user's playlist from Apple Music (Itunes Music Library xml file) to his/her playlist in Spotify (using Spotify's API). The songs that couldn't be converted will be written to "failure.txt" and the rest should be added to your selected Spotify playlist.

The plan is to further develop and deploy the web app in the near future!

## Dependencies

- Python 2
- Flask

## Startup
To get started, clone this repository to your local environment.

```bash
git clone git://github.com/Vumz/amToSpotify.git
```

Then locate your [Itunes Music Library XML file](https://support.apple.com/en-us/HT201610) and copy it into the repository folder. Make sure the name of the XML file and the below in main.py are the same.

```python
itunesXMLFile = 'itunes Music Library.xml'
```

Type client credentials in auth.py from your own spotify app, which can be made [here](https://beta.developer.spotify.com/dashboard/login)
```python
clientID = envVariables.clientID
clientSecret = envVariables.clientSecret
```

Type in the Apple Music playlist in your library that you want to convert and the Spotify playlist in your library that you want to append the songs to in main.py
```python
playlistApple = 'Drive'
playlistSpotify = 'Drive'
```

To run the program, cd into the project directory and enter the following in terminal
```python
python main.py
```

## Reporting Issues

If there are any suggestions, issues, or bugs please list them [here](https://github.com/Vumz/amToSpotify/issues).
