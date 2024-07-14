package com.example.softwarecup.pojo;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
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
 * @date 2024/4/18 10:50
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@TableName("user")
@Api(value = "用户详细信息")
public class User {

    @NotBlank(message = "用户名不能为空")
    @Length(min = 6, max = 50, message = "用户名长度在6-50之间")
    @TableId
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
    @ApiModelProperty("盐值")
    private String salt;

    @NotBlank(message = "昵称不能为空")
    @Length(min = 6, max = 50, message = "昵称长度在6-50之间")
    @ApiModelProperty("昵称")
    private String nickname;
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

    @TableField(fill = FieldFill.INSERT)
    @ApiModelProperty("头像URL")
    private String avatar;

    @TableField(fill = FieldFill.INSERT)
//    @TableField(update="now()")
    @ApiModelProperty("创建时间")
    private String create_time;

    @TableField(fill = FieldFill.INSERT_UPDATE)
//    @TableField(update="now()")
    @ApiModelProperty("更新时间")
    private String update_time;


    public User(String username, String password) {
        this.username = username;
        this.password = password;
    }

    public User(String username, String password, String email, Boolean gender, String phone, int role, String nickname) {
        this.username = username;
        this.password = password;
        this.email = email;
        this.gender = gender;
        this.phone = phone;
        this.role = role;
        this.nickname = nickname;

    }
}
