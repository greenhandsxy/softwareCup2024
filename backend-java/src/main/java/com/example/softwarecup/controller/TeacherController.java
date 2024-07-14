package com.example.softwarecup.controller;

import com.example.softwarecup.dto.NewCourseInfo;
import com.example.softwarecup.pojo.Course;
import com.example.softwarecup.pojo.User;
import com.example.softwarecup.service.CourseService;
import com.example.softwarecup.service.UserService;
import com.example.softwarecup.tools.Result;
import com.example.softwarecup.vo.CourseStudyInfo;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * @author SaoE
 * @date 2024/5/5 13:12
 */
@RestController
@RequestMapping("/tea")
@Slf4j
@Api(value = "教师功能模块", tags = "教师功能模块")
public class TeacherController {

    @Autowired
    private CourseService courseService;

    @Autowired
    private UserService userService;

    /**
     * 教师发布新课程
     * @param newCourseInfo
     * @param token
     * @return
     */
    @PostMapping("/releaseCourse")
    @ApiOperation(value = "教师发布新课程", notes = "教师发布新课程")
    public Result<Course> teacherReleaseCourse(
            @ApiParam(name = "newCourseInfo", value = "课程信息", required = true)
            @RequestBody NewCourseInfo newCourseInfo,
            @ApiParam(name = "token", value = "用户认证令牌", required = true)
            @RequestParam("token") String token) {
        User current_user = userService.getByToken(token);
        Course newCourse = new Course(newCourseInfo.getCourseId(),
                newCourseInfo.getCourseName(),
                newCourseInfo.getPrerequisites(),
                newCourseInfo.getCourseDescription(),
                newCourseInfo.getCourseType(),
                current_user.getUsername());
        courseService.teacherAddCourse(newCourse);
        return Result.success(newCourse);
    }

    /**
     * 查看自己开课的选课的情况
     * @param token
     * @return
     */
    @GetMapping("/getCourseStudyInfo")
    @ApiOperation(value = "查看自己开课的选课情况", notes = "查看自己开课的选课情况")
    public Result<List<CourseStudyInfo>> teacherGetCourseStudyInfo(
            @ApiParam(name = "token", value = "用户认证令牌", required = true)
            @RequestParam("token") String token){
        User current_user = userService.getByToken(token);
        List<CourseStudyInfo> courseStudyInfos = courseService.teacherGetCourseStudyInfo(current_user.getUsername());
        return Result.success(courseStudyInfos);
    }

    /**
     * 教师查看自己开课的课程
     * @param token
     * @return
     */
    @GetMapping("/getCourses")
    @ApiOperation(value = "教师查看自己开课的课程", notes = "教师查看自己开课的课程")
    public Result<List<Course>> getCourseByTeacherName(
            @ApiParam(name = "token", value = "用户认证令牌", required = true)
            @RequestParam("token") String token){
        User current_user = userService.getByToken(token);
        List<Course> courses = courseService.getCourseByTeacherName(current_user.getUsername());
        return Result.success(courses);
    }

}
