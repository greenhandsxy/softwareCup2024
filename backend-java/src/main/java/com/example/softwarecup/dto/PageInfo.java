package com.example.softwarecup.dto;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiModelProperty;
import lombok.Builder;
import lombok.Data;
import lombok.NonNull;
import lombok.Value;

/**
 * @author SaoE
 * @date 2024/4/23 14:19
 */
@Data
@Api(value = "分页信息")
public class PageInfo {

    /**
     * 当前页码
     */
    @ApiModelProperty("当前页码")
    private int pageNum;

    /**
     * 每页显示条数
     */
    @ApiModelProperty("每页显示条数")
    private int pageSize;


}
