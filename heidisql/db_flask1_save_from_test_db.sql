-- Copies data from the testdatabase 'carved_rock_test' to the
-- production database 'db_flask1' in HeidiSQL.

-- -------------------------------
-- 1. Create tables without uuid
-- -------------------------------

USE `db_flask1`;

-- alembic_version
CREATE TABLE IF NOT EXISTS `alembic_version` (
    `version_num` VARCHAR(32) NOT NULL,
    PRIMARY KEY (`version_num`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- user (without uuid)
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(150) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `api_key` VARCHAR(64) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_user_username` (`username`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- post
CREATE TABLE IF NOT EXISTS `post` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `author_id` INT NOT NULL,
    `created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `title` TEXT NOT NULL,
    `body` TEXT NOT NULL,
    PRIMARY KEY (`id`),
    KEY `author_id` (`author_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- tag
CREATE TABLE IF NOT EXISTS `tag` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(64) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- tags_association
CREATE TABLE IF NOT EXISTS `tags_association` (
    `tag_id` INT DEFAULT NULL,
    `post_id` INT DEFAULT NULL,
    KEY `post_id` (`post_id`),
    KEY `tag_id` (`tag_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- -------------------------------
-- 2. Copy data from db_flask1
-- -------------------------------

INSERT INTO
    `alembic_version` (`version_num`)
SELECT `version_num`
FROM `carved_rock_test`.`alembic_version`;

INSERT INTO
    `user` (
        `id`,
        `username`,
        `password`,
        `api_key`
    )
SELECT
    `id`,
    `username`,
    `password`,
    `api_key`
FROM `carved_rock_test`.`user`;

INSERT INTO
    `post` (
        `id`,
        `author_id`,
        `created`,
        `title`,
        `body`
    )
SELECT
    `id`,
    `author_id`,
    `created`,
    `title`,
    `body`
FROM `carved_rock_test`.`post`;

INSERT INTO
    `tag` (`id`, `name`)
SELECT `id`, `name`
FROM `carved_rock_test`.`tag`;

INSERT INTO
    `tags_association` (`tag_id`, `post_id`)
SELECT `tag_id`, `post_id`
FROM `carved_rock_test`.`tags_association`;

-- -------------------------------
-- 3. Add foreign keys with cascade rules
-- -------------------------------

-- Delete user → delete their posts
ALTER TABLE `post`
ADD CONSTRAINT `post_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`) ON DELETE CASCADE;

-- Delete post → delete tag associations
ALTER TABLE `tags_association`
ADD CONSTRAINT `tags_association_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`) ON DELETE CASCADE,
ADD CONSTRAINT `tags_association_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`);

-- -------------------------------
-- 4. Add uuid column to user table
-- -------------------------------

ALTER TABLE `user`
ADD COLUMN `uuid` VARCHAR(64) NULL AFTER `password`;

-- Populate uuid for all users
UPDATE `user` SET `uuid` = UUID() WHERE `uuid` IS NULL;

-- Make uuid NOT NULL and unique
ALTER TABLE `user`
MODIFY COLUMN `uuid` VARCHAR(64) NOT NULL,
ADD UNIQUE KEY `uq_user_uuid` (`uuid`);