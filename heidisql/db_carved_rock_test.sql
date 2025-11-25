-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               8.1.0 - MySQL Community Server - GPL
-- Server OS:                    Linux
-- HeidiSQL Version:             12.13.0.7147
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

-- Dumping database structure for carved_rock_test
CREATE DATABASE IF NOT EXISTS `carved_rock_test` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `carved_rock_test`;

-- Dumping structure for table carved_rock_test.alembic_version
CREATE TABLE IF NOT EXISTS `alembic_version` (
    `version_num` varchar(32) NOT NULL,
    PRIMARY KEY (`version_num`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Dumping data for table carved_rock_test.alembic_version: ~2 rows (approximately)
INSERT INTO
    `alembic_version` (`version_num`)
VALUES ('6392fde05718'),
    ('87c3441b8c45');

-- Dumping structure for table carved_rock_test.post
CREATE TABLE IF NOT EXISTS `post` (
    `id` int NOT NULL AUTO_INCREMENT,
    `author_id` int NOT NULL,
    `created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `title` text NOT NULL,
    `body` text NOT NULL,
    PRIMARY KEY (`id`),
    KEY `author_id` (`author_id`),
    CONSTRAINT `post_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 92 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Dumping data for table carved_rock_test.post: ~17 rows (approximately)
INSERT INTO
    `post` (
        `id`,
        `author_id`,
        `created`,
        `title`,
        `body`
    )
VALUES (
        75,
        1,
        '2021-06-07 00:00:00',
        'Class: Bouldering for Beginners',
        'We will be running a class aimed at members climbing at lower than v4...'
    ),
    (
        76,
        4,
        '2021-05-02 00:00:00',
        'Class: Safety at Carved Rock',
        'Here is an opportunity to have your safety license renewed for the next...'
    ),
    (
        77,
        3,
        '2021-01-17 00:00:00',
        'How to Conquer Harder Grades',
        'Stuck on v6 and need some help? Follow these 5 tips to try and break your plateau...'
    ),
    (
        78,
        4,
        '2021-02-10 00:00:00',
        'Valentines Day Climbing',
        'On Feb 14 we will be holding a special evening of climbing and fun events for you and...'
    ),
    (
        79,
        5,
        '2020-12-02 00:00:00',
        'Holiday Season Opening Hours',
        'During the holiday season Carved Rock will be open on the following schedule...'
    ),
    (
        80,
        3,
        '2020-11-15 00:00:00',
        'Happy Thanksgiving from Carved Rock',
        'Carved Rock wish you and your family a very happy Thanksgiving 2020...'
    ),
    (
        81,
        7,
        '2021-02-27 00:00:00',
        'Class: Top Rope II',
        'The second level of our popular top rope class will be run again on May 14, to book your...'
    ),
    (
        82,
        8,
        '2021-05-30 00:00:00',
        'Demo Kit Sale!',
        'Our friends at The South Tree Kit Co. will be selling ex-demo kit at heavy discounts on June...'
    ),
    (
        83,
        9,
        '2021-02-14 00:00:00',
        'Talk: Ian Parkes - K2',
        'Evening talks continue at Carved Rock with special guest Ian Parkes. Ian has climbed K2...'
    ),
    (
        84,
        1,
        '2021-03-04 00:00:00',
        'Talk: Libbie Melendez - Van Life & Climbing',
        'Libbie Melendez joins Carved Rock for an evening talk on the challenges of van...'
    ),
    (
        85,
        2,
        '2021-05-08 00:00:00',
        'Use of Loose Chalk',
        'We would like member feedback on their use of loose chalk at the center. We have had recent complaints...'
    ),
    (
        86,
        6,
        '2021-04-06 00:00:00',
        'New Membership Options',
        'From July 2021 you can sign up as a Carved Rock member with the following options...'
    ),
    (
        87,
        4,
        '2021-03-23 00:00:00',
        'Guest Climbers',
        'After some recent discussions with members, we need to remind you all of the rules for guest...'
    ),
    (
        88,
        1,
        '2020-12-25 00:00:00',
        'Happy Holidays from Carved Rock',
        'Happy Holidays from Carved Rock! See you all in the new year!'
    ),
    (
        89,
        9,
        '2021-01-01 00:00:00',
        '2021 Q1 Training Schedule',
        'Training sessions for our competition teams will be ramping up in the first quarter...'
    ),
    (
        90,
        6,
        '2021-02-06 00:00:00',
        'Kids Spring Weekend Camps',
        'Plan for the better weather and sign your kids up for our Spring Weekend Camps. From...'
    ),
    (
        91,
        7,
        '2021-04-15 00:00:00',
        'Bouldering Etiquette',
        'To help everyone on the boulders have a fun and safe time at Carved Rock, please be aware of...'
    );

-- Dumping structure for table carved_rock_test.tag
CREATE TABLE IF NOT EXISTS `tag` (
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(64) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Dumping data for table carved_rock_test.tag: ~0 rows (approximately)

-- Dumping structure for table carved_rock_test.tags_association
CREATE TABLE IF NOT EXISTS `tags_association` (
    `tag_id` int DEFAULT NULL,
    `post_id` int DEFAULT NULL,
    KEY `post_id` (`post_id`),
    KEY `tag_id` (`tag_id`),
    CONSTRAINT `tags_association_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`) ON DELETE CASCADE,
    CONSTRAINT `tags_association_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Dumping data for table carved_rock_test.tags_association: ~0 rows (approximately)

-- Dumping structure for table carved_rock_test.user
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

-- Dumping data for table carved_rock_test.user: ~11 rows (approximately)
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
        '29a1c607-ca3a-11f0-908d-0242ac110002',
        NULL
    ),
    (
        2,
        'Cleo',
        'pbkdf2:sha256:150000$6ExJIyka$099bc8963e17d2c19e313db176de51b6ac2785d7c0677a7a7cd21735c74f7371',
        '29a1c926-ca3a-11f0-908d-0242ac110002',
        NULL
    ),
    (
        3,
        'Rea',
        'pbkdf2:sha256:150000$6ExJIyka$099bc8963e17d2c19e313db176de51b6ac2785d7c0677a7a7cd21735c74f7371',
        '29a1c9b3-ca3a-11f0-908d-0242ac110002',
        NULL
    ),
    (
        4,
        'Serenity',
        'pbkdf2:sha256:150000$6ExJIyka$099bc8963e17d2c19e313db176de51b6ac2785d7c0677a7a7cd21735c74f7371',
        '29a1ca11-ca3a-11f0-908d-0242ac110002',
        NULL
    ),
    (
        5,
        'Jorja',
        'pbkdf2:sha256:150000$6ExJIyka$099bc8963e17d2c19e313db176de51b6ac2785d7c0677a7a7cd21735c74f7371',
        '29a1ca63-ca3a-11f0-908d-0242ac110002',
        NULL
    ),
    (
        6,
        'Arian',
        'pbkdf2:sha256:150000$6ExJIyka$099bc8963e17d2c19e313db176de51b6ac2785d7c0677a7a7cd21735c74f7371',
        '29a1caba-ca3a-11f0-908d-0242ac110002',
        NULL
    ),
    (
        7,
        'Kai',
        'pbkdf2:sha256:150000$6ExJIyka$099bc8963e17d2c19e313db176de51b6ac2785d7c0677a7a7cd21735c74f7371',
        '29a1cb0b-ca3a-11f0-908d-0242ac110002',
        NULL
    ),
    (
        8,
        'Kaitlin',
        'pbkdf2:sha256:150000$6ExJIyka$099bc8963e17d2c19e313db176de51b6ac2785d7c0677a7a7cd21735c74f7371',
        '29a1cb58-ca3a-11f0-908d-0242ac110002',
        NULL
    ),
    (
        9,
        'David',
        'pbkdf2:sha256:150000$6ExJIyka$099bc8963e17d2c19e313db176de51b6ac2785d7c0677a7a7cd21735c74f7371',
        '29a1cba4-ca3a-11f0-908d-0242ac110002',
        NULL
    ),
    (
        10,
        'Joakim',
        'scrypt:32768:8:1$Zme5yKIc3k1qHdMv$2fe263ae496b445b912aa90ba20f0bf4edf823b259c48275ef85917924fa4fbcd9ee5c06546da9e358f666e94bc5a68399d3b8df5ce65a8f505337d1a0d023d4',
        '29a1cbf9-ca3a-11f0-908d-0242ac110002',
        NULL
    ),
    (
        137,
        'Johnny',
        'scrypt:32768:8:1$anOumwB0EWu6IGZW$8564f4da28eb2187ccbf199c44dbc9268115c9460e29dd35c7f6baf6d213d7f21e31e0684f1ccd7904c36514e4c2e0bd2ea6b9ed8e1a844ebffe85a2b30a2fb1',
        '29a1cc56-ca3a-11f0-908d-0242ac110002',
        NULL
    );

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