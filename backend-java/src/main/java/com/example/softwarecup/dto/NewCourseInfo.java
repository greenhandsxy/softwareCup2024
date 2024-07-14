package com.example.softwarecup.dto;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;

/**
 * @author SaoE
 * @date 2024/5/5 12:37
 */
@Data
@Api(value = "新增课程信息")
public class NewCourseInfo {
    @ApiModelProperty("课程ID")
    private String courseId;

    @ApiModelProperty("课程名")
    private String courseName;

    @ApiModelProperty("课程类型")
    private String courseType;

    @ApiModelProperty("课程先修要求")
    private String prerequisites;

    @ApiModelProperty("课程描述")
    private String courseDescription;
}
