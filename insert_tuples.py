import pandas
import sqlite3

# songID = 1
# albumID = 2
# artistID = 4
# songName = 16
# albumName = 3
# artistName = 8
# artistLocation = 6
# year = 17

def connect():
    con = sqlite3.connect("data.db")
    return con

def close(con):
    con.commit()
    con.close()

def read_file(cursor):
    # open excel file
    df = pandas.read_csv("SongCSV.csv", encoding = "latin1")
    
    for i in range(1, 10001):
        # get songID and userID
        songID = df['SongID'][i]
        artistID = df['ArtistID'][i]

        # get song, album and artist names
        songName = df['Title'][i]
        artistName = df['ArtistName'][i]
        albumName = df['AlbumName'][i]

        # get artist location
        location = df['ArtistLocation'][i]

        # get year made
        year = df['Year'][i]
        plays = 20*(i%5 + 1)
        
        # insert into song, artist and album tables
        song_tuple = (songID, artistID, albumName, songName, plays)
        artist_tuple = (artistID, location)
        album_tuple = (artistID, albumName, int(year))
        
        # song
        c.execute('INSERT OR IGNORE INTO Song (Song_ID, User_ID, Album_Name, Name, Plays) VALUES (?, ?, ?, ?, ?)', song_tuple)

        # artist
        c.execute('INSERT OR IGNORE INTO Artist (User_ID, Location) VALUES (?, ?)', artist_tuple)

        # album
        c.execute('INSERT OR IGNORE INTO Album (User_ID, Name, Year) VALUES (?, ?, ?)', album_tuple)

if __name__ == "__main__":
    con = connect()
    c = con.cursor()
    read_file(c)
    close(con)
