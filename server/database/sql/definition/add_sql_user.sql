CREATE USER IF NOT EXISTS 'bm_admin'@'localhost' IDENTIFIED BY 'kou46490603';
GRANT ALL PRIVILEGES ON book_manage.* TO 'bm_admin'@'localhost';
FLUSH PRIVILEGES;