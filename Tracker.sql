-- phpMyAdmin SQL Dump
-- version 4.1.13
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 27, 2014 at 05:24 PM
-- Server version: 10.0.11-MariaDB-1~saucy-log
-- PHP Version: 5.5.12-2+deb.sury.org~saucy+1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `Tracker`
--
CREATE DATABASE IF NOT EXISTS `Tracker` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `Tracker`;

-- --------------------------------------------------------

--
-- Table structure for table `Resources`
--

DROP TABLE IF EXISTS `Resources`;
CREATE TABLE IF NOT EXISTS `Resources` (
  `RID` int(11) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `Type` varchar(50) NOT NULL,
  UNIQUE KEY `RID` (`RID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Transactions`
--

DROP TABLE IF EXISTS `Transactions`;
CREATE TABLE IF NOT EXISTS `Transactions` (
  `TID` int(10) NOT NULL AUTO_INCREMENT,
  `LoginName` varchar(50) DEFAULT NULL,
  `SerialNumber` varchar(50) DEFAULT NULL,
  `LaptopModel` varchar(50) DEFAULT NULL,
  `CaseNumber` varchar(50) DEFAULT NULL,
  `TransDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `TransType` varchar(50) DEFAULT NULL,
  `Notes` longtext,
  PRIMARY KEY (`TID`),
  UNIQUE KEY `TID` (`TID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3146 ;

-- --------------------------------------------------------

--
-- Table structure for table `TransType`
--

DROP TABLE IF EXISTS `TransType`;
CREATE TABLE IF NOT EXISTS `TransType` (
  `TransOrder` int(11) DEFAULT '0',
  `TransTypeDesc` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
CREATE TABLE IF NOT EXISTS `Users` (
  `UID` int(11) NOT NULL AUTO_INCREMENT,
  `Username` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL,
  PRIMARY KEY (`UID`),
  KEY `UID` (`UID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
