package com.example.softwarecup.pojo;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Random;

/**
 * @author SaoE
 * @date 2024/5/4 20:43
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@TableName("student_course")
@Api(value = "学生选课信息")
public class CourseChosen {
    @TableId
    @ApiModelProperty("主键ID")
    private Integer id;

    @ApiModelProperty("学生名")
    private String studentName;
    @ApiModelProperty("课程名")
    private String courseName;
    @ApiModelProperty("教师名")
    private String teacherName;
    /**
     * 章节完成数
     */
    @ApiModelProperty("章节完成数")
    private Integer studyTimeSum;
    /**
     * 活跃天数
     */
    @ApiModelProperty("活跃天数")
    private Integer studyDay;
    /**
     * 视频播放数量
     */
    @ApiModelProperty("视频播放数量")
    private Integer todayStudyTime;

    @ApiModelProperty("最近两周学习情况")
    private String twoWeekStudy;

    @ApiModelProperty("预测成绩")
    private Integer score;

    public CourseChosen(String studentName, String courseName, String teacherName) {
        this.studentName = studentName;
        this.courseName = courseName;
        this.teacherName = teacherName;
        Random random = new Random();
        this.studyTimeSum = random.nextInt(10) + 10;
        this.studyDay = random.nextInt(10) + 5;
        this.todayStudyTime = random.nextInt(10) + 10;
        this.twoWeekStudy = "0,0,0,0,0,0,0,0,0,0,0,0,0,0";
        this.score = 0;
    }


}
