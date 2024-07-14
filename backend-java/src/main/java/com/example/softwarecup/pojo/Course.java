package com.example.softwarecup.pojo;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * @author SaoE
 * @date 2024/4/19 12:51
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@TableName("course")
@Api(value = "课程详细信息")
public class Course {
    @TableId
    @ApiModelProperty("主键ID")
    private Integer id;

    @ApiModelProperty("课程ID")
    private String courseId;
    @ApiModelProperty("课程名")
    private String courseName;
    @ApiModelProperty("先修要求")
    private String prerequisites;
    @ApiModelProperty("课程描述")
    private String courseDescription;
    @ApiModelProperty("课程类型")
    private String courseType;
    @ApiModelProperty("授课教师/单位")
    private String teacherName;

    public Course(String courseId, String courseName, String prerequisites, String courseDescription, String courseType, String teacherName) {
        this.courseId = courseId;
        this.courseName = courseName;
        this.prerequisites = prerequisites;
        this.courseDescription = courseDescription;
        this.courseType = courseType;
        this.teacherName = teacherName;
    }
}
