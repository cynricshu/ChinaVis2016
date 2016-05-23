/*
 Navicat Premium Data Transfer

 Source Server         : local_MariaDB
 Source Server Type    : MariaDB
 Source Server Version : 100114
 Source Host           : localhost
 Source Database       : chinavis

 Target Server Type    : MariaDB
 Target Server Version : 100114
 File Encoding         : utf-8

 Date: 05/22/2016 23:44:43 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `t_mail`
-- ----------------------------
DROP TABLE IF EXISTS `t_mail`;
CREATE TABLE `t_mail` (
  `mailid` bigint(255) NOT NULL AUTO_INCREMENT,
  `subject` varchar(500) DEFAULT NULL,
  `fromdisplay` varchar(255) DEFAULT NULL,
  `fromaddress` varchar(255) DEFAULT NULL,
  `todisplay` text DEFAULT NULL,
  `toaddress` text DEFAULT NULL,
  `ccdisplay` text DEFAULT NULL,
  `ccaddress` text DEFAULT NULL,
  `bccdisplay` varchar(3000) DEFAULT NULL,
  `bccaddress` text DEFAULT NULL,
  `creatorname` varchar(255) DEFAULT NULL,
  `importance` int(5) DEFAULT NULL,
  `datesent` datetime DEFAULT NULL,
  `datereceive` datetime DEFAULT NULL,
  `size` int(255) DEFAULT NULL,
  `attachmentnames` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`mailid`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `t_user`
-- ----------------------------
DROP TABLE IF EXISTS `t_user`;
CREATE TABLE `t_user` (
  `userid` int(100) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `t_user_mail`
-- ----------------------------
DROP TABLE IF EXISTS `t_user_mail`;
CREATE TABLE `t_user_mail` (
  `userid` int(255) DEFAULT NULL,
  `mailid` bigint(255) DEFAULT NULL,
  `id` bigint(255) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;

