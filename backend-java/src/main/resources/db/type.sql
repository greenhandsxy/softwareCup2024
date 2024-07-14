/*
 Navicat Premium Data Transfer

 Source Server         : 云服务器
 Source Server Type    : MySQL
 Source Server Version : 50650
 Source Host           : 139.196.253.125:3306
 Source Schema         : softwarecup

 Target Server Type    : MySQL
 Target Server Version : 50650
 File Encoding         : 65001

 Date: 06/07/2024 16:45:14
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for type
-- ----------------------------
DROP TABLE IF EXISTS `type`;
CREATE TABLE `type`  (
  `type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '文章分类',
  `num` int(11) NOT NULL,
  PRIMARY KEY (`type`) USING BTREE,
  INDEX `type`(`type`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of type
-- ----------------------------
INSERT INTO `type` VALUES ('世界历史', 1);
INSERT INTO `type` VALUES ('其他', 1);
INSERT INTO `type` VALUES ('农学', 2);
INSERT INTO `type` VALUES ('化学', 20);
INSERT INTO `type` VALUES ('医学', 17);
INSERT INTO `type` VALUES ('地理学', 3);
INSERT INTO `type` VALUES ('地质学', 1);
INSERT INTO `type` VALUES ('建筑学', 34);
INSERT INTO `type` VALUES ('心理学', 12);
INSERT INTO `type` VALUES ('教育学', 15);
INSERT INTO `type` VALUES ('数学', 60);
INSERT INTO `type` VALUES ('机械工程', 30);
INSERT INTO `type` VALUES ('材料科学技术', 3);
INSERT INTO `type` VALUES ('物理学', 31);
INSERT INTO `type` VALUES ('电子学', 8);
INSERT INTO `type` VALUES ('电气工程', 5);
INSERT INTO `type` VALUES ('管理科学技术', 321);
INSERT INTO `type` VALUES ('自然辩证法', 32);
INSERT INTO `type` VALUES ('计算机科学技术', 29);
INSERT INTO `type` VALUES ('语言学', 16);

SET FOREIGN_KEY_CHECKS = 1;
