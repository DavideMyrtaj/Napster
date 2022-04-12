-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 12, 2022 at 10:21 PM
-- Server version: 10.3.34-MariaDB-0ubuntu0.20.04.1
-- PHP Version: 8.0.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `DIRECTORY`
--

-- --------------------------------------------------------

--
-- Table structure for table `DOWNLOAD`
--

CREATE TABLE `DOWNLOAD` (
  `ID` int(11) NOT NULL,
  `SESSION_ID` varchar(16) CHARACTER SET utf8 DEFAULT NULL,
  `MD5` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `IP` varchar(15) CHARACTER SET utf8 DEFAULT NULL,
  `PORT` varchar(5) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `FILE`
--

CREATE TABLE `FILE` (
  `MD5` varchar(32) CHARACTER SET utf8 NOT NULL,
  `DESCRIZIONE` varchar(100) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `FILE`
--

INSERT INTO `FILE` (`MD5`, `DESCRIZIONE`) VALUES
('1C4068C628E1D428B220C44987AB5251', '.DS_Store                                                                                           '),
('C01AB39740BECB1E5034EF62EC34D13C', 'DIRECTORY.sql                                                                                       '),
('D5275CBC5F14AB90B27D1174696452BA', 'prova.txt                                                                                           ');

-- --------------------------------------------------------

--
-- Table structure for table `FILE_PEER`
--

CREATE TABLE `FILE_PEER` (
  `MD5` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `SESSION_ID` varchar(32) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `PEER`
--

CREATE TABLE `PEER` (
  `SESSION_ID` varchar(16) CHARACTER SET utf8 NOT NULL,
  `IP` varchar(15) CHARACTER SET utf8 DEFAULT NULL,
  `PORTA` varchar(5) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `DOWNLOAD`
--
ALTER TABLE `DOWNLOAD`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `FILE`
--
ALTER TABLE `FILE`
  ADD PRIMARY KEY (`MD5`);

--
-- Indexes for table `FILE_PEER`
--
ALTER TABLE `FILE_PEER`
  ADD UNIQUE KEY `FILE_PER_PEER` (`MD5`,`SESSION_ID`),
  ADD KEY `file_peer_ibfk_2` (`SESSION_ID`);

--
-- Indexes for table `PEER`
--
ALTER TABLE `PEER`
  ADD PRIMARY KEY (`SESSION_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `DOWNLOAD`
--
ALTER TABLE `DOWNLOAD`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `FILE_PEER`
--
ALTER TABLE `FILE_PEER`
  ADD CONSTRAINT `file_peer_ibfk_1` FOREIGN KEY (`MD5`) REFERENCES `FILE` (`MD5`) ON DELETE CASCADE,
  ADD CONSTRAINT `file_peer_ibfk_2` FOREIGN KEY (`SESSION_ID`) REFERENCES `PEER` (`SESSION_ID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
