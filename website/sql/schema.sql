CREATE TABLE users(
	uid 			   INTEGER PRIMARY KEY AUTOINCREMENT,

  /* UNIQUE username -> index on username, efficient lookup */
  username        VARCHAR(40) UNIQUE,
  fullname        VARCHAR(40) NOT NULL,

  token           VARCHAR(128),
  token_secret    VARCHAR(128)
);
