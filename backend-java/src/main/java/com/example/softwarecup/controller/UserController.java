package com.example.softwarecup.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.softwarecup.dto.UserQuery;
import com.example.softwarecup.dto.UserRegister;
import com.example.softwarecup.dto.UserUpdateInfo;
import com.example.softwarecup.pojo.User;
import com.example.softwarecup.service.UserService;
import com.example.softwarecup.tools.Result;
import com.example.softwarecup.vo.UserLoginVo;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import springfox.documentation.annotations.ApiIgnore;

import static com.example.softwarecup.exception.ExceptionEnum.AUTH_NOT_ENOUGH;

/**
 * @author SaoE
 * @date 2024/4/18 17:26
 */
@RestController
@RequestMapping("/user")
@Slf4j
@Api(value = "用户通用功能接口", tags = "用户通用功能接口")
@CrossOrigin
public class UserController {

    @Autowired
    private UserService userService;

    /**
     * 用户注册页
     * @param userRegister
     * @return
     */
    @PostMapping("/register")
    @ApiOperation(value = "用户注册", notes = "用户注册")
    public Result<User> register(
            @ApiParam(name = "userRegister", value = "用户注册信息", required = true)
            @Validated @RequestBody UserRegister userRegister) {
        User user = new User(userRegister.getUsername(),
                userRegister.getPassword(),
                userRegister.getEmail(),
                userRegister.getGender(),
                userRegister.getPhone(),
                userRegister.getRole(),
                userRegister.getUsername());
        userService.register(user);
        return Result.success(user);
    }

    /**
     * 用户登录页
     * @param username
     * @param password
     * @return
     */
    @PostMapping("/login")
    @ApiOperation(value = "用户登录", notes = "用户登录")
    public Result<UserLoginVo> login(
            @ApiParam(name = "username", value = "用户名", required = true)
            @RequestParam("username") String username,
            @ApiParam(name = "password", value = "密码", required = true)
            @RequestParam("password") String password
                                     ) {
        User formUser = new User(username, password);
        UserLoginVo userLoginVo= userService.login(formUser);
        log.info(userLoginVo.getToken());
        return Result.success(userLoginVo);
    }

    /**
     * 用户登出页
     * @param token
     * @return
     */
    @GetMapping("/logout")
    @ApiOperation(value = "用户登出", notes = "用户登出")
    public Result<Boolean> logout(
            @ApiParam(name = "token", value = "用户认证令牌", required = true)
            @RequestParam("token") String token) {
        userService.logout(token);
        return Result.success(true);
    }

    /**
     * 获取用户信息
     * @param token
     * @return
     */
    @GetMapping("/userinfo")
    @ApiOperation(value = "获取用户信息", notes = "获取用户信息")
    public Result<User> userInfo(
            @ApiParam(name = "token", value = "用户认证令牌", required = true)
            @RequestParam("token") String token){
        User user = userService.getByToken(token);
        return Result.success(user);
    }

    /**
     * 更新用户信息
     * @param userUpdateInfo
     * @return
     */
    @PostMapping("/updateUserInfo")
    @ApiOperation(value = "更新用户信息", notes = "更新用户信息")
    public Result<User> updateUserInfo(
            @ApiParam(name = "userUpdateInfo", value = "用户更新信息", required = true)
            @Validated @RequestBody UserUpdateInfo userUpdateInfo){
        return userService.updateUserInfo(userUpdateInfo);
    }

    /**
     * 管理员功能
     * 分页模糊查询用户
     * @param userQuery
     * @return
     *
     */
    @PostMapping("/page")
    @ApiIgnore
    public Result<?> findPage(@RequestBody UserQuery userQuery,
                              @RequestParam("token") String token){

        User current_user = userService.getByToken(token);
        User user = userService.getOne(new LambdaQueryWrapper<User>().eq(User::getUsername, current_user.getUsername()));
        if(user.getRole() != 0){
            return Result.error(Integer.parseInt(AUTH_NOT_ENOUGH.getResultCode()), AUTH_NOT_ENOUGH.getResultMsg());
        }

        LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
        wrapper.orderByDesc(User::getCreate_time);

        if(!"".equals(userQuery.getUsername()) && userQuery.getUsername() != null){
            wrapper.like(User::getUsername, userQuery.getUsername());
        }

        Page<User> page = userService.page(
                new Page<>(
                        userQuery.getPageNum(),
                        userQuery.getPageSize()
                ),
                wrapper
        );
        return Result.success(page);
    }

    /**
     * 上传头像
     * @param file
     * @param token
     * @return
     */
    @PostMapping("/uploadAvatar")
    @ApiOperation(value = "图片文件更新头像", notes = "图片文件更新头像")
    public Result<String> uploadAvatar(
            @ApiParam(name = "file", value = "图片文件", required = true)
            @RequestParam("file") MultipartFile file,
            @ApiParam(name = "token", value = "用户认证令牌", required = true)
            @RequestParam("token") String token){
        User current_user = userService.getByToken(token);
        return Result.success(userService.uploadAvatar(current_user, file));
    }

    /**
     * 更新头像url，用于表情包拍摄后单独更新头像url
     * @param avatarUrl
     * @param token
     * @return
     */
    @PostMapping("/updateAvatarUrl")
    @ApiOperation(value = "更新头像URL", notes = "更新头像URL")
    public Result<String> updateAvatarUrl(
            @ApiParam(name = "avatarUrl", value = "头像URL", required = true)
            @RequestParam("avatarUrl") String avatarUrl,
            @ApiParam(name = "token", value = "用户认证令牌", required = true)
            @RequestParam("token") String token){
        User current_user = userService.getByToken(token);
        userService.updateAvatarUrl(current_user, avatarUrl);
        return Result.success(avatarUrl);
    }

}