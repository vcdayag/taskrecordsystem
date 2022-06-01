CREATE USER 'tsruser'@'localhost' IDENTIFIED BY 'tsrpassword'; 
CREATE DATABASE IF NOT EXISTS taskrecordsystem;
GRANT ALL ON taskrecordsystem.* TO 'tsruser'@'localhost';

USE taskrecordsystem;
-- Create table category
CREATE TABLE IF NOT EXISTS `category`(
  `category_id` INT UNSIGNED AUTO_INCREMENT,
  `name` VARCHAR(16) NOT NULL,
  `description` VARCHAR(128) DEFAULT NULL,
  CONSTRAINT `category_category_id_pk` PRIMARY KEY(`category_id`)
);
-- Create table tasks
CREATE TABLE IF NOT EXISTS `task`(
  `task_id` INT UNSIGNED AUTO_INCREMENT,
  `title` VARCHAR(64),
  `details` VARCHAR(1024),
  `deadline` TIMESTAMP,
  `finished` TINYINT DEFAULT 0,
  `category_id` INT UNSIGNED DEFAULT NULL,
  CONSTRAINT `task_task_id_pk` PRIMARY KEY(`task_id`),
  CONSTRAINT `task_category_id_fk` FOREIGN KEY(`category_id`) REFERENCES `category`(`category_id`)
);