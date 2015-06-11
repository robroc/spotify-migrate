Grooveshark to Spotify
======================

This is a Python script that takes your Grooveshark playlists (if you were quick enough to save them while you could), or any playlist, really, and turns them into Spotify playlists.

The playlists must be in CSV format, with a .csv extension, and look like this:

    SongName,Artist,Album
    "Dancing Queen","Abba","Greatest Hits"
    "Can't Buy Me Love","The Beatles","A Hard Day's Night"
etc.


The name of the CSV file should be the name of the Spotify playlist you wish to have, for example:

`Oldies.csv`


There should be one CSV per playlist. The CSVs should be in teh same folder as the `spotify_migrate.py` file.

You'll need [spotipy](http://spotipy.readthedocs.org/en/latest/) and requests installed for it to work. Installing spotipy will install reqeusts:

    pip install spotipy


You'll also need to register an app with the [Spotify API](https://developer.spotify.com/web-api/) and generate a client ID and client secret, as well as provide a redirect URI. Add these to lines 7-10, along with your user name.

The first time you run the script, you'll be asked to authorize this script with your Spotify account. Follow the directions and paste in the URL of the site you were redirected to.

When you're ready, just run the file from the command line, ensuring you're in teh same folder as the script.


How it works
------------

First, the script will go open each CSV, create a Spotify playlist for it. Then will go through each line and search Spotify for that track's unique ID. It's important that songs and artists be spelled correctly, or the search will fail.

Successful searches will return a track ID and add that track to the playlist.


Failed tracks
-------------

The script will generate a CSV of tracks that were not found in the search, including playlist name and ID. You can fix the spellings of the songs and artists in a spreadsheet and add these manually later. I plan on writing a script to add corrected tracks to their corresponding playlists later.

