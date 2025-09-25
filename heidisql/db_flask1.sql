-- Creates the entire database 'db_flask1' with tables and
-- data in HeidiSQL.

-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.1.0 - MySQL Community Server - GPL
-- Server OS:                    Linux
-- HeidiSQL Version:             12.11.0.7065
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */
;
/*!40101 SET NAMES utf8 */
;
/*!50503 SET NAMES utf8mb4 */
;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */
;
/*!40103 SET TIME_ZONE='+00:00' */
;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */
;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */
;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */
;

-- Dumping database structure for db_flask1
CREATE DATABASE IF NOT EXISTS `db_flask1`
/*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */
/*!80016 DEFAULT ENCRYPTION='N' */;

USE `db_flask1`;

-- Dumping structure for table db_flask1.alembic_version
CREATE TABLE IF NOT EXISTS `alembic_version` (
    `version_num` varchar(32) NOT NULL,
    PRIMARY KEY (`version_num`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Dumping data for table db_flask1.alembic_version: ~2 rows (approximately)
INSERT INTO
    `alembic_version` (`version_num`)
VALUES ('6392fde05718'),
    ('87c3441b8c45');

-- Dumping structure for table db_flask1.user
CREATE TABLE IF NOT EXISTS `user` (
    `id` int NOT NULL AUTO_INCREMENT,
    `username` varchar(150) NOT NULL,
    `password` varchar(255) NOT NULL,
    `uuid` varchar(64) NOT NULL,
    `api_key` varchar(64) DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_user_username` (`username`),
    UNIQUE KEY `uq_user_uuid` (`uuid`)
) ENGINE = InnoDB AUTO_INCREMENT = 138 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Dumping data for table db_flask1.user: ~11 rows (approximately)
INSERT INTO
    `user` (
        `id`,
        `username`,
        `password`,
        `uuid`,
        `api_key`
    )
VALUES (
        1,
        'Jason',
        'pbkdf2:sha256:150000$6ExJIyka$099bc8963e17d2c19e313db176de51b6ac2785d7c0677a7a7cd21735c74f7371',
        'bdfb2512-93ce-11f0-8e85-0242ac110002',
        NULL
    ),
    (
        2,
        'Cleo',
        'pbkdf2:sha256:150000$6ExJIyka$099bc8963e17d2c19e313db176de51b6ac2785d7c0677a7a7cd21735c74f7371',
        'bdfb294e-93ce-11f0-8e85-0242ac110002',
        NULL
    ),
    (
        3,
        'Rea',
        'pbkdf2:sha256:150000$6ExJIyka$099bc8963e17d2c19e313db176de51b6ac2785d7c0677a7a7cd21735c74f7371',
        'bdfb29c8-93ce-11f0-8e85-0242ac110002',
        NULL
    ),
    (
        4,
        'Serenity',
        'pbkdf2:sha256:150000$6ExJIyka$099bc8963e17d2c19e313db176de51b6ac2785d7c0677a7a7cd21735c74f7371',
        'bdfb2a1e-93ce-11f0-8e85-0242ac110002',
        NULL
    ),
    (
        5,
        'Jorja',
        'pbkdf2:sha256:150000$6ExJIyka$099bc8963e17d2c19e313db176de51b6ac2785d7c0677a7a7cd21735c74f7371',
        'bdfb2a70-93ce-11f0-8e85-0242ac110002',
        NULL
    ),
    (
        6,
        'Arian',
        'pbkdf2:sha256:150000$6ExJIyka$099bc8963e17d2c19e313db176de51b6ac2785d7c0677a7a7cd21735c74f7371',
        'bdfb2aca-93ce-11f0-8e85-0242ac110002',
        NULL
    ),
    (
        7,
        'Kai',
        'pbkdf2:sha256:150000$6ExJIyka$099bc8963e17d2c19e313db176de51b6ac2785d7c0677a7a7cd21735c74f7371',
        'bdfb2b18-93ce-11f0-8e85-0242ac110002',
        NULL
    ),
    (
        8,
        'Kaitlin',
        'pbkdf2:sha256:150000$6ExJIyka$099bc8963e17d2c19e313db176de51b6ac2785d7c0677a7a7cd21735c74f7371',
        'bdfb2b69-93ce-11f0-8e85-0242ac110002',
        NULL
    ),
    (
        9,
        'David',
        'pbkdf2:sha256:150000$6ExJIyka$099bc8963e17d2c19e313db176de51b6ac2785d7c0677a7a7cd21735c74f7371',
        'bdfb2bb7-93ce-11f0-8e85-0242ac110002',
        NULL
    ),
    (
        10,
        'Joakim',
        'scrypt:32768:8:1$Zme5yKIc3k1qHdMv$2fe263ae496b445b912aa90ba20f0bf4edf823b259c48275ef85917924fa4fbcd9ee5c06546da9e358f666e94bc5a68399d3b8df5ce65a8f505337d1a0d023d4',
        'bdfb2c10-93ce-11f0-8e85-0242ac110002',
        NULL
    ),
    (
        137,
        'Johnny',
        'scrypt:32768:8:1$anOumwB0EWu6IGZW$8564f4da28eb2187ccbf199c44dbc9268115c9460e29dd35c7f6baf6d213d7f21e31e0684f1ccd7904c36514e4c2e0bd2ea6b9ed8e1a844ebffe85a2b30a2fb1',
        '0b63a4dc-a792-4238-9636-a1cd5a443c92',
        NULL
    );

-- Dumping structure for table db_flask1.post
CREATE TABLE IF NOT EXISTS `post` (
    `id` int NOT NULL AUTO_INCREMENT,
    `author_id` int NOT NULL,
    `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `title` text NOT NULL,
    `body` text NOT NULL,
    PRIMARY KEY (`id`),
    KEY `author_id` (`author_id`),
    CONSTRAINT `post_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 75 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- (Insert data for posts, unchanged from your dump)
-- [keeping all your existing post inserts here, not repeating for brevity]

-- Dumping structure for table db_flask1.tag
CREATE TABLE IF NOT EXISTS `tag` (
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(64) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Dumping structure for table db_flask1.tags_association
CREATE TABLE IF NOT EXISTS `tags_association` (
    `tag_id` int DEFAULT NULL,
    `post_id` int DEFAULT NULL,
    KEY `post_id` (`post_id`),
    KEY `tag_id` (`tag_id`),
    CONSTRAINT `tags_association_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`) ON DELETE CASCADE,
    CONSTRAINT `tags_association_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Dumping data for table db_flask1.tags_association: ~0 rows (approximately)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */
;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */
;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */
;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */
;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */
;