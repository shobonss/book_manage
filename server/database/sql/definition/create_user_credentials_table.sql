USE book_manage;
CREATE TABLE hashed_user_credentials (
  user_id  VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (user_id)
);