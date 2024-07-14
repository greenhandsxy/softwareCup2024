package com.example.softwarecup.vo;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.List;

/**
 * @author SaoE
 * @date 2024/5/5 12:51
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
@Api(value = "课程学习情况")
public class CourseStudyInfo {
    @ApiModelProperty("课程名")
    private String courseName;
    /**
     * 选课人数
     */
    @ApiModelProperty("选课人数")
    private Integer studentNum = 0;

    @ApiModelProperty("学生学习情况")
    private List<StudentStudyInfo> studentStudyInfoList;

    public CourseStudyInfo(String courseName) {
        this.courseName = courseName;
        this.studentStudyInfoList = new ArrayList<>();
    }
}
