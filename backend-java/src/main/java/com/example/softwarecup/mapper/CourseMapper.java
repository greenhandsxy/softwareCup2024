package com.example.softwarecup.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.softwarecup.pojo.Course;
import com.example.softwarecup.pojo.CourseType;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * @author SaoE
 * @date 2024/4/19 12:56
 */
@Mapper
@Repository
public interface CourseMapper extends BaseMapper<Course> {

    /**
     * 查询所有课程
     * @return
     */
    @Select("SELECT * FROM course")
    List<Course> selectAll();

    /**
     * 根据课程类型查询课程
     * @param courseType
     * @return
     */
    @Select("SELECT id, course_id, course_name, prerequisites, course_description, course_type, teacher_name\n" +
            "FROM course\n" +
            "WHERE course_type = #{courseType};\n")
    List<Course> selectCourseByType(@Param("courseType") String courseType);

    /**
     * 根据课程名查询课程信息
     * @param courseName
     * @return
     */
    @Select("SELECT * FROM course WHERE course_name = #{courseName}")
    Course getCourseDetail(@Param("courseName") String courseName);

    /**
     * 教师添加课程
     */
    @Select("INSERT INTO course (course_id, course_name, prerequisites, course_description, course_type, teacher_name)\n" +
            "VALUES (#{courseId}, #{courseName}, #{prerequisites}, #{courseDescription}, #{courseType}, #{teacherName});\n")
    void teacherAddCourse(@Param("courseId") String courseId,
                          @Param("courseName") String courseName,
                          @Param("prerequisites") String prerequisites,
                          @Param("courseDescription") String courseDescription,
                          @Param("courseType") String courseType,
                          @Param("teacherName") String teacherName);

    /**
     * 查询所有课程类别
     */
    @Select("SELECT *\n" +
            "FROM type\n" +
            "ORDER BY \n" +
            "    CASE \n" +
            "        WHEN type = '其他' THEN 2 \n" +
            "        ELSE 1 \n" +
            "    END,\n" +
            "    num DESC")
    List<CourseType> getAllCourseType();

}
