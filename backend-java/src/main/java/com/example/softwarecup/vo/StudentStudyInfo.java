package com.example.softwarecup.vo;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Data;

/**
 * @author SaoE
 * @date 2024/5/5 13:39
 */
@Data
@AllArgsConstructor
@Api(value = "学生学习情况")
public class StudentStudyInfo {
    @ApiModelProperty("课程名")
    private String courseName;
    @ApiModelProperty("学生名")
    private String studentName;
    @ApiModelProperty("课程学习总时长")
    private Integer studyTimeSum;
    @ApiModelProperty("活跃天数")
    private Integer studyDay;
    @ApiModelProperty("视频播放数量")
    private Integer todayStudyTime;
    @ApiModelProperty("最近两周学习情况")
    private String twoWeekStudy;
    @ApiModelProperty("预测成绩")
    private Integer score;
}
