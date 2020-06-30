-- MySQL dump 10.13  Distrib 5.7.30, for Linux (x86_64)
--
-- Host: localhost    Database: covid_internet_controls
-- ------------------------------------------------------
-- Server version	5.7.30-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `countries`
--

DROP TABLE IF EXISTS `countries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `countries` (
  `country_code` varchar(2) NOT NULL,
  `country_name` varchar(64) NOT NULL,
  `continent` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`country_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `countries`
--

LOCK TABLES `countries` WRITE;
/*!40000 ALTER TABLE `countries` DISABLE KEYS */;
INSERT INTO `countries` VALUES ('AU','Australia','Australia'),('CN','China','Asia'),('HK','Hong_Kong','Asia'),('KR','Korea','Asia'),('PE','Peru','South_America'),('ZA','South_Africa','Africa');
/*!40000 ALTER TABLE `countries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `request`
--

DROP TABLE IF EXISTS `request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `request` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `worker_ip` varchar(32) NOT NULL,
  `domain` varchar(256) NOT NULL,
  `path` varchar(256) NOT NULL,
  `response_id` int(11) DEFAULT NULL,
  `protocol` varchar(5) NOT NULL,
  `censored` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `worker_ip` (`worker_ip`),
  KEY `response_id` (`response_id`),
  CONSTRAINT `request_ibfk_1` FOREIGN KEY (`worker_ip`) REFERENCES `workers` (`worker_ip`),
  CONSTRAINT `request_ibfk_2` FOREIGN KEY (`response_id`) REFERENCES `response` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request`
--

LOCK TABLES `request` WRITE;
/*!40000 ALTER TABLE `request` DISABLE KEYS */;
INSERT INTO `request` VALUES (12,'111.231.28.232','www.google.com','/',NULL,'http',1),(13,'49.233.48.214','www.google.com','/',NULL,'http',1),(14,'111.230.200.28','www.google.com','/',NULL,'http',1),(15,'139.155.74.236','www.google.com','/',NULL,'http',1),(16,'124.156.101.160','www.google.com','/',2,'http',0),(17,'102.67.140.37','www.google.com','/',2,'http',0);
/*!40000 ALTER TABLE `request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `response`
--

DROP TABLE IF EXISTS `response`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `response` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `success` tinyint(1) NOT NULL,
  `status_code` int(11) NOT NULL,
  `content` longblob NOT NULL,
  `content_hash` char(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `response`
--

LOCK TABLES `response` WRITE;
/*!40000 ALTER TABLE `response` DISABLE KEYS */;
INSERT INTO `response` VALUES (2,1,302,_binary '<HTML><HEAD><meta http-equiv=\"content-type\" content=\"text/html;charset=utf-8\">\n<TITLE>302 Moved</TITLE></HEAD><BODY>\n<H1>302 Moved</H1>\nThe document has moved\n<A HREF=\"https://www.google.com/?gws_rd=ssl\">here</A>.\r\n</BODY></HTML>\r\n','68a006996ece55adef2db478ed631ea5');
/*!40000 ALTER TABLE `response` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workers`
--

DROP TABLE IF EXISTS `workers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `workers` (
  `worker_ip` varchar(32) NOT NULL,
  `country_code` varchar(2) NOT NULL,
  `city` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`worker_ip`),
  KEY `country_code` (`country_code`),
  CONSTRAINT `workers_ibfk_1` FOREIGN KEY (`country_code`) REFERENCES `countries` (`country_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workers`
--

LOCK TABLES `workers` WRITE;
/*!40000 ALTER TABLE `workers` DISABLE KEYS */;
INSERT INTO `workers` VALUES ('102.67.140.37','ZA',NULL),('103.140.45.134','KR',NULL),('109.201.143.179','AU',NULL),('111.230.200.28','CN','Guangzhou'),('111.231.28.232','CN','Shanghai'),('124.156.101.160','HK',NULL),('129.21.183.10','CN','Shanghai'),('129.28.202.97','CN','Chongqing'),('139.155.74.236','CN','Chengdu'),('45.7.230.136','PE',NULL),('49.233.48.214','CN','Beijing');
/*!40000 ALTER TABLE `workers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-10 14:28:20
