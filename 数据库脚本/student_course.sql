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

 Date: 06/07/2024 16:45:08
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for student_course
-- ----------------------------
DROP TABLE IF EXISTS `student_course`;
CREATE TABLE `student_course`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '学生用户名',
  `course_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '课程名称',
  `teacher_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '教师用户名',
  `study_time_sum` int(11) UNSIGNED ZEROFILL NOT NULL DEFAULT 00000000000 COMMENT '学习时长总和（小时）',
  `study_day` int(11) NOT NULL DEFAULT 1 COMMENT '连续学习天数',
  `today_study_time` int(11) NOT NULL DEFAULT 0 COMMENT '今日学习时长',
  `two_week_study` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '前14天学习序列',
  `score` int(1) UNSIGNED ZEROFILL NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `student_name_index`(`student_name`) USING BTREE,
  INDEX `course_name_index`(`course_name`) USING BTREE,
  INDEX `teacher_name_index`(`teacher_name`) USING BTREE,
  CONSTRAINT `student_course_ibfk_1` FOREIGN KEY (`student_name`) REFERENCES `user` (`username`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `student_course_ibfk_2` FOREIGN KEY (`course_name`) REFERENCES `course` (`course_name`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2099208195 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of student_course
-- ----------------------------
INSERT INTO `student_course` VALUES (-2110951423, 'xiaoyi', '操作系统', 'xulaoshi', 00000000017, 12, 13, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 70);
INSERT INTO `student_course` VALUES (-1683202046, 'aaaaaa', '文物精品与文化中国（自主模式）', '彭林', 00000000019, 7, 19, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 99);
INSERT INTO `student_course` VALUES (-1259507711, 'duxiaolong', '云计算技术与大数据', 'xulaoshi', 00000000016, 5, 13, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 95);
INSERT INTO `student_course` VALUES (-1192398847, 'xiaoyi', '云计算技术与大数据', 'xulaoshi', 00000000013, 5, 10, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 79);
INSERT INTO `student_course` VALUES (-929107966, 'aaaaaa', '数据结构(上)(自主模式)', '邓俊辉', 00000000011, 14, 15, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 55);
INSERT INTO `student_course` VALUES (-635514878, 'cccccc', 'e时代的大佬师——慕课教师的修炼心法（自主模式）', '肖星', 00000000000, 0, 0, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 0);
INSERT INTO `student_course` VALUES (-627118078, 'aaaaaa', '不朽的艺术：走进大师与经典（自主模式）', '肖鹰', 00000000012, 7, 13, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 79);
INSERT INTO `student_course` VALUES (-617779199, 'duxiaolong', '操作系统', 'xulaoshi', 00000000017, 5, 13, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 98);
INSERT INTO `student_course` VALUES (-487755775, 'aaaaaa', 'testCourse', '韩海花', 00000000017, 11, 14, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 72);
INSERT INTO `student_course` VALUES (-203456510, 'bbbbbb', '大学计算机基础与应用', '韩海花', 00000000000, 0, 0, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 0);
INSERT INTO `student_course` VALUES (-118726654, 'ljjjjj', '云计算技术与大数据', 'xulaoshi', 00000000014, 11, 17, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 60);
INSERT INTO `student_course` VALUES (95182850, 'aaaaaa', '现代礼仪（自主模式）', '袁涤非', 00000000018, 10, 10, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 72);
INSERT INTO `student_course` VALUES (203390978, 'cccccc', '大学计算机基础与应用', '韩海花', 00000000000, 0, 0, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 0);
INSERT INTO `student_course` VALUES (459153410, 'aaaaaa', '大学计算机基础与应用', '韩海花', 00000000017, 7, 19, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 99);
INSERT INTO `student_course` VALUES (682455041, 'linziyang', '云计算技术与大数据', 'xulaoshi', 00000000016, 7, 14, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 86);
INSERT INTO `student_course` VALUES (720134145, 'strong_bear_1', '模拟电子技术基础(应用部分)（自主模式）', '耿华', 00000000012, 11, 17, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 57);
INSERT INTO `student_course` VALUES (807333890, 'aaaaaa', '足球运动与科学（自主模式）', '赖柳明', 00000000014, 8, 17, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 91);
INSERT INTO `student_course` VALUES (861859842, 'aaaaaa', '大气污染控制工程（自主模式）', '郝吉明', 00000000015, 12, 13, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 64);
INSERT INTO `student_course` VALUES (997040130, 'ljjjjj', '宝宝🐖养成课', 'bbbbbb', 00000000013, 9, 18, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 84);
INSERT INTO `student_course` VALUES (1122856961, 'linziyang', '操作系统', 'xulaoshi', 00000000014, 10, 13, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 66);
INSERT INTO `student_course` VALUES (1613520897, 'ljjjjj', '园林植物景观学原理与方法(自主模式)', '张德顺', 00000000018, 5, 10, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 93);
INSERT INTO `student_course` VALUES (1969192961, 'cccccc', '教＆学微辞典', '李曼丽', 00000000012, 14, 16, '0,0,0,0,0,0,0,0,0,0,0,0,0,0', 0);

SET FOREIGN_KEY_CHECKS = 1;
