package com.example.softwarecup.pojo;

import com.baomidou.mybatisplus.annotation.TableName;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * @author SaoE
 * @date 2024/5/8 12:15
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
@TableName("type")
@Api(value = "课程类型及数量")
public class CourseType {
    @ApiModelProperty("课程类型")
    private String type;

    @ApiModelProperty("课程数量")
    private Integer num;
}
