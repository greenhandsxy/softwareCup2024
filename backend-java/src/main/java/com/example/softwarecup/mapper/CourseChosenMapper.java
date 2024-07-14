package com.example.softwarecup.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.softwarecup.pojo.CourseChosen;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

/**
 * @author SaoE
 * @date 2024/5/4 20:56
 */
@Mapper
public interface CourseChosenMapper extends BaseMapper<CourseChosen> {

    /**
     * 学生所有选课情况
     * @param studentName
     * @return
     */
    @Select("SELECT * FROM student_course WHERE student_name = #{studentName}")
    List<CourseChosen> allChosenCourse(String studentName);

    /**
     * 删除选课
     * @param studentName
     * @param courseName
     */
    @Delete("DELETE FROM student_course WHERE student_name = #{studentName} AND course_name = #{courseName}")
    void deleteChosenCourse(String studentName, String courseName);

    /**
     * 学生查看自己选课学习情况
     */
    @Select("SELECT * FROM student_course " +
            "WHERE student_name = #{studentName} " +
            "ORDER BY course_name")
    List<CourseChosen> studentChosenCourseInfo(@Param("studentName")String studentName);

    /**
     * 教师查看自己开的课程的选课情况
     */
    @Select("SELECT * FROM student_course " +
            "WHERE teacher_name = #{teacherName} " +
            "ORDER BY course_name")
    List<CourseChosen> teacherChosenCourseInfo(@Param("teacherName")String teacherName);

    /**
     * 更新学生预测分数
     */
    @Select("UPDATE student_course " +
            "SET score = #{score} " +
            "WHERE student_name = #{studentName} " +
            "AND course_name = #{courseName}")
    void updateStudentPredictScore(String studentName, String courseName, Integer score);
}
