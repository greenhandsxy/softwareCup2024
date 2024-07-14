package com.example.softwarecup.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.softwarecup.dto.PageInfo;
import com.example.softwarecup.mapper.CourseMapper;
import com.example.softwarecup.pojo.Course;
import com.example.softwarecup.pojo.CourseType;
import com.example.softwarecup.service.CourseService;
import com.example.softwarecup.tools.Result;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * @author SaoE
 * @date 2024/4/20 17:19
 */
@RestController
@RequestMapping("/course")
@Slf4j
@Api(value = "课程功能接口", tags = "课程功能接口")
public class CourseController {

    @Autowired
    private CourseService courseService;

    @Autowired
    private CourseMapper courseMapper;

    /**
     * 获取所有课程
     * @return
     */
    @PostMapping("/list")
    @ApiOperation(value = "获取所有课程", notes = "获取所有课程")
    public Result<Page<Course>> getAllCourses(
            @ApiParam(name = "pageInfo", value = "分页信息", required = true)
            @RequestBody PageInfo pageInfo,
            @RequestParam(value = "token", required = false) String token,
            @RequestParam(value = "courseType", required = false) String courseType) {
        Page<Course> coursePage;
        if (!"".equals(courseType) && courseType != null){
            LambdaQueryWrapper<Course> wrapper = new LambdaQueryWrapper<>();
            wrapper.like(Course::getCourseType, courseType);
            Page<Course> page = new Page<>(
                            pageInfo.getPageNum(),
                            pageInfo.getPageSize()
            );
            coursePage = courseMapper.selectPage(page, wrapper);
        }else {
            Page<Course> page = new Page<>(
                    pageInfo.getPageNum(),
                    pageInfo.getPageSize()
            );
            coursePage = courseMapper.selectPage(page, null);
        }


        return Result.success(coursePage);
    }
    /**
     * 获取指定类型的课程
     * @param courseType
     * @return
     */
    @GetMapping("/getCourseByType")
    @ApiOperation(value = "获取指定类型的课程", notes = "获取指定类型的课程")
    public Result<String> getCourseByType(
            @ApiParam(name = "courseType", value = "课程类型", required = true)
            @RequestParam("courseType") String courseType) {
        List<Course> courses = courseService.getCourseByType(courseType);
        return Result.success(courses);
    }

    /**
     * 获取课程详情
     * @param courseName
     * @return
     */
    @GetMapping("/courseDetail")
    @ApiOperation(value = "获取课程详情", notes = "获取课程详情")
    public Result<Course> getCourseDetail(
            @ApiParam(name = "courseName", value = "课程名称", required = true)
            @RequestParam("courseName") String courseName){
        return Result.success(courseService.getCourseDetail(courseName));
    }



    /**
     * // 将数组转换为字符串
     * List<Double> studyTimes = ...; // 假设这是14天的学习时长
     * String studyTimeStr = String.join(",", studyTimes.stream().map(String::valueOf).collect(Collectors.toList()));
     *
     * // 从数据库读取后，将字符串转换回数组
     * String dbValue = ...; // 从数据库获取的字符串
     * List<Double> parsedStudies = Arrays.stream(dbValue.split(","))
     *     .map(Double::parseDouble)
     *     .collect(Collectors.toList());
     */

    /**
     * 获取所有课程类别
     * @return
     */
    @GetMapping("/getAllCourseType")
    @ApiOperation(value = "获取所有课程类别", notes = "获取所有课程类别")
    public Result<List<CourseType>> getAllCourseType() {
        List<CourseType> courseTypes = courseMapper.getAllCourseType();
        return Result.success(courseTypes);
    }

}
