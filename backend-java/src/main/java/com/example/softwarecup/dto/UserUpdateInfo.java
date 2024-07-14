package com.example.softwarecup.dto;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiModelProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.validator.constraints.Length;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;

/**
 * @author SaoE
 * @date 2024/4/23 15:06
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
@Api(value = "用户信息更新模块")
public class UserUpdateInfo {
    @ApiModelProperty("用户名")
    private String username;

    @Email(message = "邮箱格式错误")
    @ApiModelProperty("邮箱")
    private String email;

    @Length(min = 11, max = 11, message = "手机号长度格式错误")
    @ApiModelProperty("联系方式")
    private String phone;

    @Length(min = 6, max = 20, message = "昵称长度在6-20之间")
    @ApiModelProperty("昵称")
    private String nickname;
}
