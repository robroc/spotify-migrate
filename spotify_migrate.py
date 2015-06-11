import spotipy
import spotipy.util as util
import csv
import glob

username = "YOUR-USER-NAME"
client_id = "YOUR-CLIENT-ID"
client_secret = "YOUR-CLIENT-SECRET"
redirect_uri="YOUR-REDIRECT-URI"
scope = "playlist-modify-public" #This is the scope needed to modify public playlists only
token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth=token)
fail_file = open("failed_tracks.csv", "w")
fail_csv = csv.writer(fail_file)
fail_csv.writerow(["playlist","playlist_id","track","artist"])


def main():
    files = glob.glob('*.csv')    
    for f in files:
        if "failed_tracks" in f:
            continue
        track_list = []
        data = open(f)
        reader = csv.reader(data)
        list_name = f[:f.find(".")]
        print ""
        print "PROCESSING PLAYLIST {}".format(list_name)
        print ""
        new_list = sp.user_playlist_create(username, list_name)
        new_list_id = new_list["id"]
        reader.next()
        reader_list = list(reader)
        reader_length = len(reader_list)
        for line in reader_list:
            if len(line) > 0:
                track = line[0].strip()
                artist = line[1].strip()
                album = line[2].strip()
                track_list.append(get_track_id(list_name, new_list_id, track, artist))                
            else:
                continue
        track_list = filter(None, track_list)
        
        # Add tracks to playlist
        if len(track_list) <= 100:
            add_tracks_to_playlist(new_list_id, track_list)
        else:  # If playlist has more than 100 tracks, split it into chunks of 100
            multi_list = split_list(track_list)
            for list_part in multi_list:
                add_tracks_to_playlist(new_list_id, list_part)
            
        print ""
        print "Added {0} tracks out of {1} total".format(str(len(track_list)), str(reader_length))
        print "---------------------"
        data.close()
    fail_file.close()
  

def get_track_id(playlist, playlist_id, track, artist):
    results = sp.search(q=track + " artist:" +artist, type='track')
    items = results["tracks"]["items"]
    if len(items) > 0:
        track_id = items[0]["id"]
        print "Adding track: {}".format(track)
        return track_id
    else:
        failed_tracks(playlist, playlist_id, track, artist)
        

def add_tracks_to_playlist(list_id, track_list):
    sp.user_playlist_add_tracks(username, list_id, track_list)
    
    
def split_list(a_list):
    return list(chunks(a_list, 100))
    
    
def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n] 
    
    
def failed_tracks(playlist, playlist_id, track, artist):
    print "No tracks found for {0} by {1}".format(track, artist)
    fail_csv.writerow([playlist, playlist_id, track, artist])
    
    
if __name__ == '__main__':
    main()