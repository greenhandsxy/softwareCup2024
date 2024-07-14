package com.example.softwarecup.vo;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * @author SaoE
 * @date 2024/4/29 17:59
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
@Api(value = "用户登录信息")
public class UserLoginVo {
    @ApiModelProperty("用户名")
    String username;
    @ApiModelProperty("昵称")
    String nickname;
    @ApiModelProperty("token")
    String token;
    @ApiModelProperty("角色")
    Integer role;
    @ApiModelProperty("邮箱")
    String email;
    @ApiModelProperty("联系方式")
    String phone;
    @ApiModelProperty("性别")
    Boolean gender;
    @ApiModelProperty("头像URL")
    String avatar;

}
