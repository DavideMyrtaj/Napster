-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Creato il: Apr 10, 2022 alle 14:39
-- Versione del server: 10.6.4-MariaDB
-- Versione PHP: 8.1.3

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
-- Struttura della tabella `FILE`
--

CREATE TABLE `FILE` (
  `MD5` varchar(32) CHARACTER SET utf8mb3 NOT NULL,
  `DESCRIZIONE` varchar(100) CHARACTER SET utf8mb3 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `FILE`
--

INSERT INTO `FILE` (`MD5`, `DESCRIZIONE`) VALUES
('27C749230E8F93B76FA0A4B9DC3CC450', 'prova.txt');

-- --------------------------------------------------------

--
-- Struttura della tabella `FILE_PEER`
--

CREATE TABLE `FILE_PEER` (
  `MD5` varchar(32) CHARACTER SET utf8mb3 DEFAULT NULL,
  `SESSION_ID` varchar(32) CHARACTER SET utf8mb3 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `FILE_PEER`
--

INSERT INTO `FILE_PEER` (`MD5`, `SESSION_ID`) VALUES
('27C749230E8F93B76FA0A4B9DC3CC450', '28WOTTRYXP7NZIWU'),
('27C749230E8F93B76FA0A4B9DC3CC450', 'EPWBEI1L4WK4TTX4');

-- --------------------------------------------------------

--
-- Struttura della tabella `PEER`
--

CREATE TABLE `PEER` (
  `SESSION_ID` varchar(16) CHARACTER SET utf8mb3 NOT NULL,
  `IP` varchar(15) CHARACTER SET utf8mb3 DEFAULT NULL,
  `PORTA` varchar(5) CHARACTER SET utf8mb3 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `PEER`
--

INSERT INTO `PEER` (`SESSION_ID`, `IP`, `PORTA`) VALUES
('28WOTTRYXP7NZIWU', '192.168.001.079', '59606'),
('2TIO0UIH6HGQ9B49', '192.168.001.079', '54365'),
('35KB2NLVHLZ00IB5', '192.168.001.079', '52656'),
('EPWBEI1L4WK4TTX4', '192.168.001.079', '63130'),
('F677FF67RFTFTY', NULL, NULL),
('HJGECS3DECMKD68M', '192.168.001.079', '61333');

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `FILE`
--
ALTER TABLE `FILE`
  ADD PRIMARY KEY (`MD5`);

--
-- Indici per le tabelle `FILE_PEER`
--
ALTER TABLE `FILE_PEER`
  ADD UNIQUE KEY `FILE_PER_PEER` (`MD5`,`SESSION_ID`),
  ADD KEY `file_peer_ibfk_2` (`SESSION_ID`);

--
-- Indici per le tabelle `PEER`
--
ALTER TABLE `PEER`
  ADD PRIMARY KEY (`SESSION_ID`);

--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `FILE_PEER`
--
ALTER TABLE `FILE_PEER`
  ADD CONSTRAINT `file_peer_ibfk_1` FOREIGN KEY (`MD5`) REFERENCES `FILE` (`MD5`) ON DELETE CASCADE,
  ADD CONSTRAINT `file_peer_ibfk_2` FOREIGN KEY (`SESSION_ID`) REFERENCES `PEER` (`SESSION_ID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
