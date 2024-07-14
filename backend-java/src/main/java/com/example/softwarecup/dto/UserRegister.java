package com.example.softwarecup.dto;

import com.baomidou.mybatisplus.annotation.TableId;
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
 * @date 2024/4/23 22:53
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
@Api(value = "用户注册信息")
public class UserRegister {

    @NotBlank(message = "用户名不能为空")
    @Length(min = 6, max = 20, message = "用户名长度在6-20之间")
    @ApiModelProperty("用户名")
    private String username;

    @NotBlank(message = "密码不能为空")
    @Length(min = 6, max = 20, message = "密码长度在6-20之间")
    @ApiModelProperty("密码")
    private String password;

    @NotBlank(message = "邮箱不能为空")
    @Email(message = "邮箱格式错误")
    @ApiModelProperty("邮箱")
    private String email;

    @NotBlank(message = "手机号不能为空")
    @Length(min = 11, max = 11, message = "手机号长度格式错误")
    @ApiModelProperty("联系方式")
    private String phone;

    /**
     * value 0 : female
     * value 1 : male
     */
    @ApiModelProperty("性别")
    private Boolean gender;
    /**
     * value 0 : 管理员
     * value 1 : 普通用户
     * value 2 : 教师
     */
    @ApiModelProperty("角色")
    private int role;
}
