import pandas
import sqlite3
import datetime

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
        artist_tuple = (artistID, artistName, location)
        album_tuple = (artistID, albumName, int(year))
        rateAlbums_tuple = (artistID, artistID, albumName, 5, datetime.datetime.now(), albumName)
        rateSongs_tuple = (artistID, songID, 5, datetime.datetime.now())

        # song
        c.execute('INSERT OR IGNORE INTO Song (Song_ID, User_ID, Album_Name, Name, Plays) VALUES (?, ?, ?, ?, ?)', song_tuple)

        # artist
        c.execute('INSERT OR IGNORE INTO Artist (User_ID, Name, Location) VALUES (?, ?, ?)', artist_tuple)

        # album
        #c.execute('INSERT OR IGNORE INTO Album (User_ID, Name, Year) VALUES (?, ?, ?)', album_tuple)
        query = "INSERT INTO Album (User_ID, Name, Year) SELECT "+"'"+artistID+"','"+albumName+"',"+str(year)+ " WHERE NOT EXISTS (SELECT 1 FROM Album WHERE Name = '"+albumName+"')"
        #print(query)
        c.execute(query)

        # rate song
        c.execute('INSERT OR IGNORE INTO RateSongs (Rater_User_ID, Song_ID, Stars, Rate_Date) VALUES (?,?,?,?)', rateSongs_tuple)

        # rate album
        query = "INSERT INTO RateAlbums (Rater_User_ID, Owner_User_ID, Name, Stars, Rate_Date) SELECT "+"'"+artistID+"','"+artistID+"','"+albumName+"',"+str(5)+",'"+str(datetime.datetime.now())+ "' WHERE NOT EXISTS (SELECT 1 FROM RateAlbums WHERE Name = '"+albumName+"')"
        #print(query)
        #print(i)
        c.execute(query)

if __name__ == "__main__":
    con = connect()
    c = con.cursor()
    read_file(c)
    close(con)
