import pandas
import sqlite3
import datetime
import csv

# songID = 1
# albumID = 2
# artistID = 4
# songName = 16
# albumName = 3
# artistName = 8
# artistLocation = 6
# year = 17
userIdList = []
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

    with open ('user_ids.csv') as datafile:
        reader = csv.reader(datafile)
        for z in reader:
            z = str(z)
            u_id = z[-(len(z)-2):-2]
            userIdList.append(u_id)
            print(u_id)

    count = 0
    with open('image_links.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for x in csvReader:
            link = str(x)
            src = link[-(len(link)-2):-2]
            #print(src)
            c.execute("UPDATE Artist SET Image_Src = (?) WHERE User_ID =" + "'" + str(userIdList[count]) + "'", (src,))
            count = count + 1

if __name__ == "__main__":
    con = connect()
    c = con.cursor()
    read_file(c)
    close(con)
