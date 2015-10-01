-- script to create a new user with root privelages identified by
-- readingisfun
CREATE USER 'readingnet_admin'@'localhost' IDENTIFIED BY 'readingisfun';

CREATE DATABASE READINGNET;
-- grant privileges on readingnet
GRANT ALL PRIVILEGES ON  READINGNET.* TO 'readingnet_admin'@'localhost';
-- reload privileges
FLUSH PRIVILEGES;
