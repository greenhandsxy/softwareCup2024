package com.example.softwarecup.controller;

import com.example.softwarecup.pojo.CourseChosen;
import com.example.softwarecup.pojo.User;
import com.example.softwarecup.service.CourseService;
import com.example.softwarecup.service.UserService;
import com.example.softwarecup.tools.Result;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * @author SaoE
 * @date 2024/5/5 13:12
 */
@RestController
@RequestMapping("/stu")
@Slf4j
@Api(value = "学生功能接口", tags = "学生功能接口")
public class StudentController {

    @Autowired
    private CourseService courseService;

    @Autowired
    private UserService userService;

    /**
     * 添加选课
     * @param courseName
     * @param token
     * @return
     */
    @GetMapping("/selectCourse")
    @ApiOperation(value = "学生添加选课", notes = "添加选课")
    public Result<CourseChosen> selectCourse(
            @ApiParam(name = "courseName", value = "课程名称", required = true)
            @RequestParam("courseName") String courseName,
            @ApiParam(name = "token", value = "用户认证令牌", required = true)
            @RequestParam("token") String token) {
        User user = userService.getByToken(token);
        CourseChosen courseChosen = courseService.studentAddCourse(courseName, user.getUsername());
        return Result.success(courseChosen);
    }

    /**
     * 删除选课
     * @param courseName
     * @param token
     * @return
     */
    @GetMapping("/deleteCourse")
    @ApiOperation(value = "学生删除选课", notes = "删除选课")
    public Result<String> deleteCourse(
            @ApiParam(name = "courseName", value = "课程名称", required = true)
            @RequestParam("courseName") String courseName,
            @ApiParam(name = "token", value = "用户认证令牌", required = true)
            @RequestParam("token") String token) {
        User user = userService.getByToken(token);
        courseService.studentDeleteCourse(courseName, user.getUsername());
        return Result.success("退选成功");
    }

    /**
     * 获取学生选课信息
     * @param token
     * @return
     */
    @GetMapping("/getCourseStudyInfo")
    @ApiOperation(value = "学生获取选课信息", notes = "获取学生选课信息")
    public Result<List<CourseChosen>> getCourseStudyInfo(
            @ApiParam(name = "token", value = "用户认证令牌", required = true)
            @RequestParam("token") String token) {
        User user = userService.getByToken(token);
        List<CourseChosen> courseChosens = courseService.studentGetCourseStudyInfo(user.getUsername());
        return Result.success(courseChosens);
    }

    /**
     * 更新学生预测成绩
     * @param courseName
     * @param score
     * @param token
     * @return
     */
    @GetMapping("/updateStudentPredictScore")
    @ApiOperation(value = "学生更新预测成绩", notes = "更新学生预测成绩")
    public Result<String> updateStudentPredictScore(
            @ApiParam(name = "courseName", value = "课程名称", required = true)
            @RequestParam("courseName") String courseName,
            @ApiParam(name = "score", value = "预测成绩", required = true)
            @RequestParam("score") Integer score,
            @ApiParam(name = "token", value = "用户认证令牌", required = true)
            @RequestParam("token") String token) {
        User user = userService.getByToken(token);
        courseService.updateStudentPredictScore(user.getUsername(), courseName, score);
        return Result.success("更新成功");
    }

}
