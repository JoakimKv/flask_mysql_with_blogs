-- Drop tables if they exist

DROP TABLE IF EXISTS `post`;

DROP TABLE IF EXISTS `user`;

-- User table
CREATE TABLE `user` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
) ENGINE = InnoDB;

-- Post table
CREATE TABLE `post` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    author_id INT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    CONSTRAINT fk_post_author FOREIGN KEY (author_id) REFERENCES `user` (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;