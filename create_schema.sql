
CREATE TABLE Users (
  User_ID VARCHAR(30) NOT NULL,
  Email VARCHAR(30) NOT NULL,
  Name VARCHAR(30) NOT NULL,
  Password VARCHAR(30) NOT NULL,
  Is_Artist INTEGER NOT NULL,
  PRIMARY KEY (User_ID)
);

CREATE TABLE Basic (
  User_ID VARCHAR(30) NOT NULL,
  DOB DATE NOT NULL,
  PRIMARY KEY (User_ID),
  FOREIGN KEY (User_ID) REFERENCES Users(User_ID)
  ON DELETE CASCADE
);

CREATE TABLE Artist (
  User_ID VARCHAR(30) NOT NULL,
  Location VARCHAR(30) NOT NULL,
  Most_Popular_Album_Name VARCHAR(30),
  Most_Popular_Song_ID VARCHAR(30),
  PRIMARY KEY (User_ID),
  FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
  FOREIGN KEY (Most_Popular_Song_ID) REFERENCES Song(Song_ID),
  FOREIGN KEY (Most_Popular_Album_Name) REFERENCES Album(Name)
  ON DELETE CASCADE
);

CREATE TABLE Song (
  Song_ID VARCHAR(30) NOT NULL,
  User_ID VARCHAR(30) NOT NULL,
  Album_Name VARCHAR(30) NOT NULL,
  Name VARCHAR(30) NOT NULL,
  Plays INTEGER NOT NULL,
  PRIMARY KEY(Song_ID),
  FOREIGN KEY (User_ID) REFERENCES Album (User_ID)
  FOREIGN KEY (Album_Name) REFERENCES Album (Name)
  ON DELETE CASCADE
);

CREATE TABLE Album (
  User_ID VARCHAR(30) NOT NULL,
  Name VARCHAR(30) NOT NULL,
  Year INTEGER NOT NULL,
  PRIMARY KEY(User_ID, Name),
  FOREIGN KEY(User_ID) REFERENCES Artist(User_ID)
  ON DELETE CASCADE
);

CREATE TABLE Admin (
  Admin_ID INTEGER NOT NULL,
  Admin_Email VARCHAR(30) NOT NULL,
  Name VARCHAR(30) NOT NULL,
  PRIMARY KEY(Admin_ID)
);

CREATE TABLE Review (
  Review_ID INTEGER NOT NULL,
  Song_ID VARCHAR(30) NOT NULL,
  Admin_ID INTEGER NOT NULL,
  Deleted INTEGER NOT NULL,
  Reviewed INTEGER NOT NULL,
  Flagged_Date DATE NOT NULL,
  Review_Date DATE NOT NULL,
  PRIMARY KEY(Review_ID),
  FOREIGN KEY (Song_ID) REFERENCES Songs(Song_ID)
  ON DELETE CASCADE,
  FOREIGN KEY (Admin_ID) REFERENCES Admin(Admin_ID)
);

CREATE TABLE RateAlbums (
  Rate_Album_ID VARCHAR(30) NOT NULL,
  Rater_User_ID VARCHAR(30) NOT NULL,
  Owner_User_ID VARCHAR(30) NOT NULL,
  Name VARCHAR(30) NOT NULL,
  Emoji VARCHAR(30) NOT NULL,
  Stars INTEGER NOT NULL,
  Rate_Date DATE NOT NULL,
  PRIMARY KEY (Rate_Album_ID),
  FOREIGN KEY (Name) REFERENCES Album(Name)
  ON DELETE CASCADE,
  FOREIGN KEY (Rater_User_ID) REFERENCES Users(User_ID),
  FOREIGN KEY (Owner_User_ID) REFERENCES Artists(User_ID)
  ON DELETE CASCADE
);

CREATE TABLE RateSongs (
  Rate_Song_ID VARCHAR(30) NOT NULL,
  Rater_User_ID VARCHAR(30) NOT NULL,
  Song_ID VARCHAR(30) NOT NULL,
  Emoji VARCHAR(30) NOT NULL,
  Stars INTEGER NOT NULL,
  Rate_Date DATE NOT NULL,
  PRIMARY KEY(Rate_Song_ID),
  FOREIGN KEY (Rater_User_ID) REFERENCES Users(User_ID),
  FOREIGN KEY (Song_ID) REFERENCES Songs(Song_ID)
  ON DELETE CASCADE
);
