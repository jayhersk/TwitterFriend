/* Can manually insert dummy data for testing here */

INSERT INTO users(username, fullname, num_friends)
VALUES('jayhersk', 'jaylin herskovitz', 2);

INSERT INTO user_friends(f_username, username)
VALUES('austin', 'jayhersk');

INSERT INTO user_friends(f_username, username)
VALUES('starr', 'jayhersk');