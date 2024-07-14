package com.example.softwarecup.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.example.softwarecup.pojo.Course;
import com.example.softwarecup.pojo.CourseChosen;
import com.example.softwarecup.vo.CourseStudyInfo;

import java.util.List;

/**
 * @author SaoE
 * @date 2024/4/19 12:57
 */
public interface CourseService extends IService<Course> {

    /**
     * 获取全部课程
     */
    List<Course> getAllCourses();

    /**
     * 根据分类获取课程
     * @param courseType
     * @return
     */
    List<Course> getCourseByType(String courseType);

    Course getCourseDetail(String courseName);

    /**
     * 学生选课
     * @param courseName
     * @param studentName
     */
    CourseChosen studentAddCourse(String courseName, String studentName);

    /**
     * 学生退选
     * @param courseName
     * @param studentName
     * @return
     */
    void studentDeleteCourse(String courseName, String studentName);

    /**
     * 学生查看自己选课学习情况
     * @return
     */
    List<CourseChosen> studentGetCourseStudyInfo(String studentName);

    /**
     * 更新学生预测得分
     */
    void updateStudentPredictScore(String studentName, String courseName, Integer score);

    /**
     * 教师发布课程
     * @param newCourse
     */
    void teacherAddCourse(Course newCourse);

    /**
     * 教师查看自己开课的选课的情况
     */
    List<CourseStudyInfo> teacherGetCourseStudyInfo(String teacherName);

    /**
     * 教师查看自己开课信息
     * @param teacherName
     * @return
     */
    List<Course> getCourseByTeacherName(String teacherName);

}
