DROP TABLE Users;
CREATE TABLE Users (
  User_ID VARCHAR(30),
  Email VARCHAR(30),
  Name VARCHAR(30),
  Password VARCHAR(30),
  PRIMARY KEY (User_ID)
);

DROP TABLE Basic;
CREATE TABLE Basic (
  User_ID VARCHAR(30) NOT NULL,
  DOB DATE NOT NULL,
  PRIMARY KEY (User_ID),
  FOREIGN KEY (User_ID) REFERENCES Users(User_ID)
  ON DELETE CASCADE
);

DROP TABLE Artist;
CREATE TABLE Artist (
  User_ID VARCHAR(30) NOT NULL,
  Name VARCHAR(30) NOT NULL,
  Location VARCHAR(30) NOT NULL,
  Most_Popular_Album_Name VARCHAR(30),
  Most_Popular_Song_ID VARCHAR(30),
  Image_Src VARCHAR(100000),
  PRIMARY KEY (User_ID)
  --FOREIGN KEY (Most_Popular_Song_ID) REFERENCES Song(Song_ID),
  --FOREIGN KEY (Most_Popular_Album_Name) REFERENCES Album(Name)
  --ON DELETE CASCADE
);

DROP TABLE Song;
CREATE TABLE Song (
  Song_ID VARCHAR(30) NOT NULL,
  User_ID VARCHAR(30) NOT NULL,
  Album_Name VARCHAR(30) NOT NULL,
  Name VARCHAR(30) NOT NULL,
  Plays INTEGER NOT NULL,
  PRIMARY KEY(Song_ID)
  --FOREIGN KEY (User_ID) REFERENCES Artist (User_ID)
  --FOREIGN KEY (Album_Name) REFERENCES Album (Name)
  --ON DELETE CASCADE
);

DROP TABLE Album;
CREATE TABLE Album (
  User_ID VARCHAR(30) NOT NULL,
  Name VARCHAR(30) NOT NULL,
  Year INTEGER NOT NULL,
  PRIMARY KEY(User_ID, Name)
  --FOREIGN KEY(User_ID) REFERENCES Artist(User_ID)
  --ON DELETE CASCADE
);

DROP TABLE Admin;
CREATE TABLE Admin (
  Admin_ID INTEGER NOT NULL,
  Admin_Email VARCHAR(30) NOT NULL,
  Name VARCHAR(30) NOT NULL,
  PRIMARY KEY(Admin_ID)
);

DROP TABLE Review;
CREATE TABLE Review (
  Review_ID INTEGER NOT NULL,
  Song_ID VARCHAR(30) NOT NULL,
  Admin_ID INTEGER,
  Deleted INTEGER NOT NULL,
  Reviewed INTEGER NOT NULL,
  Flagged_Date DATE NOT NULL,
  Review_Date DATE,
  PRIMARY KEY(Review_ID),
  FOREIGN KEY (Song_ID) REFERENCES Song(Song_ID)
  ON DELETE CASCADE,
  FOREIGN KEY (Admin_ID) REFERENCES Admin(Admin_ID)
);

DROP TABLE RateAlbums;
CREATE TABLE RateAlbums (
  Rate_Album_ID INTEGER NOT NULL,
  Rater_User_ID VARCHAR(30) NOT NULL,
  Owner_User_ID VARCHAR(30) NOT NULL,
  Name VARCHAR(30) NOT NULL,
  Stars INTEGER NOT NULL,
  Rate_Date DATE NOT NULL,
  PRIMARY KEY (Rate_Album_ID)
  --FOREIGN KEY (Name, Owner_User_ID) REFERENCES Album(Name, User_ID)
  --ON DELETE CASCADE
  --FOREIGN KEY (Rater_User_ID) REFERENCES Users(User_ID)
  --FOREIGN KEY (Owner_User_ID) REFERENCES Artist(User_ID)
  --ON DELETE CASCADE
);

DROP TABLE RateSongs;
CREATE TABLE RateSongs (
  Rate_Song_ID INTEGER NOT NULL,
  Rater_User_ID VARCHAR(30) NOT NULL,
  Song_ID VARCHAR(30) NOT NULL,
  Stars INTEGER NOT NULL,
  Rate_Date DATE NOT NULL,
  PRIMARY KEY(Rate_Song_ID),
  --FOREIGN KEY (Rater_User_ID) REFERENCES Users(User_ID),
  FOREIGN KEY (Song_ID) REFERENCES Song(Song_ID)
  ON DELETE CASCADE
);
