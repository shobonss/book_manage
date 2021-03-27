USE book_manage;
CREATE TABLE user_informations (
  user_id VARCHAR(255) NOT NULL,
  user_name VARCHAR(255) NOT NULL,
  age INT,
  mail_address VARCHAR(255),
  PRIMARY KEY(user_id),
  CONSTRAINT fk_user_id
  FOREIGN KEY (user_id)
  REFERENCES hashed_user_credentials(user_id)
);