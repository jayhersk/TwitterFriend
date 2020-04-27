/* Table of all users who have logges into the app*/
CREATE TABLE users(
	uid 			   INTEGER PRIMARY KEY AUTOINCREMENT,

  /* UNIQUE username -> index on username, efficient lookup */
  username        VARCHAR(40) UNIQUE,
  fullname        VARCHAR(40) NOT NULL,

  token           VARCHAR(128),
  token_secret    VARCHAR(128),
  num_friends     INTEGER
);

/* Friends of a user */
CREATE TABLE user_friends(
  fid         INTEGER PRIMARY KEY AUTOINCREMENT,
  f_username  VARCHAR(40),

  uid         INTEGER,
  username    VARCHAR(40),

  stressed    BOOLEAN,
  checked     DATETIME,

  FOREIGN KEY(uid) REFERENCES users(uid),
  FOREIGN KEY(username) REFERENCES users(username)
);

/* Wellnes scores for each month for each friend */
CREATE TABLE scores(
  fid         INTEGER,
  month_name  VARCHAR(40),
  score       REAL,

  FOREIGN KEY(fid) REFERENCES user_friends(fid)
)
