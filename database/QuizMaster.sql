-- MySQL Script generated by MySQL Workbench
-- Wed May 24 14:50:50 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema `stud_v23_tda072`
-- -----------------------------------------------------

CREATE SCHEMA IF NOT EXISTS `stud_v23_tda072` DEFAULT CHARACTER SET utf8 ;
USE `stud_v23_tda072`;

-- -----------------------------------------------------
-- Table `spørsmålskategori`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spørsmålskategori` ;

CREATE TABLE IF NOT EXISTS `spørsmålskategori` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `navn` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `navn_UNIQUE` (`navn` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bruker`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bruker` ;

CREATE TABLE IF NOT EXISTS `bruker` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(50) NOT NULL,
  `passord` VARCHAR(102) NOT NULL,
  `fornavn` VARCHAR(50) NOT NULL,
  `etternavn` VARCHAR(50) NOT NULL,
  `admin` TINYINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `login_UNIQUE` (`login` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `quiz`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `quiz` ;

CREATE TABLE IF NOT EXISTS `quiz` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `navn` VARCHAR(50) NOT NULL,
  `beskrivelse` TEXT(1000) NULL,
  `admin_id` INT UNSIGNED NULL,
  PRIMARY KEY (`id`),
  INDEX `quiz_admin_id_idx` (`admin_id` ASC) VISIBLE,
  CONSTRAINT `quiz_admin_id`
    FOREIGN KEY (`admin_id`)
    REFERENCES `bruker` (`id`)
    ON DELETE SET NULL
    ON UPDATE SET NULL)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `quiz_sesjon`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `quiz_sesjon` ;

CREATE TABLE IF NOT EXISTS `quiz_sesjon` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `quiz_id` INT UNSIGNED NOT NULL,
  `student_id` INT UNSIGNED NOT NULL,
  `godkjent` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  INDEX `sesjon_quiz_id_idx` (`quiz_id` ASC) VISIBLE,
  INDEX `sesjon_student_id_idx` (`student_id` ASC) VISIBLE,
  CONSTRAINT `sesjon_quiz_id`
    FOREIGN KEY (`quiz_id`)
    REFERENCES `quiz` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `sesjon_student_id`
    FOREIGN KEY (`student_id`)
    REFERENCES `bruker` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spørsmål`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spørsmål` ;

CREATE TABLE IF NOT EXISTS `spørsmål` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `spørsmål` TEXT(500) NOT NULL,
  `kategori_id` INT UNSIGNED NOT NULL,
  `admin_id` INT UNSIGNED NULL,
  PRIMARY KEY (`id`),
  INDEX `spørsmål_kategori_id_idx` (`kategori_id` ASC) VISIBLE,
  INDEX `spørsmål_admin_id_idx` (`admin_id` ASC) VISIBLE,
  CONSTRAINT `spørsmål_kategori_id`
    FOREIGN KEY (`kategori_id`)
    REFERENCES `spørsmålskategori` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `spørsmål_admin_id`
    FOREIGN KEY (`admin_id`)
    REFERENCES `bruker` (`id`)
    ON DELETE SET NULL
    ON UPDATE SET NULL)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `svarmulighet`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `svarmulighet` ;

CREATE TABLE IF NOT EXISTS `svarmulighet` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `svar` TEXT(500) NOT NULL,
  `korrekt` TINYINT NOT NULL,
  `spørsmål_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `svarmulighet_spørsmål_id_idx` (`spørsmål_id` ASC) VISIBLE,
  CONSTRAINT `svarmulighet_spørsmål_id`
    FOREIGN KEY (`spørsmål_id`)
    REFERENCES `spørsmål` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `spørsmål_har_quiz`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `spørsmål_har_quiz` ;

CREATE TABLE IF NOT EXISTS `spørsmål_har_quiz` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `spørsmål_id` INT UNSIGNED NOT NULL,
  `quiz_id` INT UNSIGNED NOT NULL,
  INDEX `shq_quiz_id_idx` (`quiz_id` ASC) VISIBLE,
  PRIMARY KEY (`id`),
  CONSTRAINT `shq_spørsmål_id`
    FOREIGN KEY (`spørsmål_id`)
    REFERENCES `spørsmål` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `shq_quiz_id`
    FOREIGN KEY (`quiz_id`)
    REFERENCES `quiz` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `quiz_sesjon_svar`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `quiz_sesjon_svar` ;

CREATE TABLE IF NOT EXISTS `quiz_sesjon_svar` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `quiz_sesjon_id` INT UNSIGNED NOT NULL,
  `spørsmål_id` INT UNSIGNED NOT NULL,
  `svarmulighet_id` INT UNSIGNED NULL,
  `tekstsvar` TEXT(1000) NULL,
  `godkjent` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  INDEX `qss_quiz_sesjon_id_idx` (`quiz_sesjon_id` ASC) VISIBLE,
  INDEX `qss_svarmulighet_id_idx` (`svarmulighet_id` ASC) VISIBLE,
  INDEX `qss_spørsmål_id_idx` (`spørsmål_id` ASC) VISIBLE,
  CONSTRAINT `qss_quiz_sesjon_id`
    FOREIGN KEY (`quiz_sesjon_id`)
    REFERENCES `quiz_sesjon` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `qss_svarmulighet_id`
    FOREIGN KEY (`svarmulighet_id`)
    REFERENCES `svarmulighet` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `qss_spørsmål_id`
    FOREIGN KEY (`spørsmål_id`)
    REFERENCES `spørsmål` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `quiz_kommentar`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `quiz_kommentar` ;

CREATE TABLE IF NOT EXISTS `quiz_kommentar` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `quiz_sesjon_id` INT UNSIGNED NOT NULL,
  `bruker_id` INT UNSIGNED NULL,
  `tekst` TEXT(1000) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `qk_quiz_sesjon_id_idx` (`quiz_sesjon_id` ASC) VISIBLE,
  INDEX `qk_bruker_id_idx` (`bruker_id` ASC) VISIBLE,
  CONSTRAINT `qk_quiz_sesjon_id`
    FOREIGN KEY (`quiz_sesjon_id`)
    REFERENCES `quiz_sesjon` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `qk_bruker_id`
    FOREIGN KEY (`bruker_id`)
    REFERENCES `bruker` (`id`)
    ON DELETE SET NULL
    ON UPDATE SET NULL)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `svar_kommentar`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `svar_kommentar` ;

CREATE TABLE IF NOT EXISTS `svar_kommentar` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `quiz_sesjon_svar_id` INT UNSIGNED NOT NULL,
  `bruker_id` INT UNSIGNED NULL,
  `tekst` TEXT(1000) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `qk_bruker_id_idx` (`bruker_id` ASC) VISIBLE,
  INDEX `sk_quiz_sesjon_svar_id_idx` (`quiz_sesjon_svar_id` ASC) VISIBLE,
  CONSTRAINT `sk_quiz_sesjon_svar_id`
    FOREIGN KEY (`quiz_sesjon_svar_id`)
    REFERENCES `quiz_sesjon_svar` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `sk_bruker_id`
    FOREIGN KEY (`bruker_id`)
    REFERENCES `bruker` (`id`)
    ON DELETE SET NULL
    ON UPDATE SET NULL)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
