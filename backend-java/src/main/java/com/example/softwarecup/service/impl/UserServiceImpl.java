package com.example.softwarecup.service.impl;

import cn.hutool.core.util.IdUtil;
import cn.hutool.json.JSONUtil;
import com.aliyun.oss.OSS;
import com.aliyun.oss.model.GeneratePresignedUrlRequest;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.softwarecup.config.AliyunConfig;
import com.example.softwarecup.dto.UserUpdateInfo;
import com.example.softwarecup.exception.BizException;
import com.example.softwarecup.mapper.UserMapper;
import com.example.softwarecup.pojo.User;
import com.example.softwarecup.service.UserService;

import com.example.softwarecup.tools.Result;
import com.example.softwarecup.tools.SecurityUtil;
import com.example.softwarecup.vo.UserLoginVo;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.Date;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

import static com.example.softwarecup.exception.ExceptionEnum.LOGIN_ERROR;
import static com.example.softwarecup.exception.ExceptionEnum.NOT_LOGIN;

/**
 * @author SaoE
 * @date 2024/4/18 11:19
 */
@Service
@Slf4j
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {

    @Autowired
    private UserMapper userMapper;

    @Autowired
    private RedisTemplate redisTemplate;

    @Autowired
    private AliyunConfig aliyunConfig;

    @Autowired
    private OSS ossClient;

    @Override
    public void register(User user) {
        String salt = IdUtil.simpleUUID();
        String password = SecurityUtil.crypto(salt, user.getPassword());
        user.setPassword(password);
        user.setNickname(user.getUsername());
        user.setSalt(salt);
        user.setAvatar(aliyunConfig.getTargetUrl() + "/" + aliyunConfig.getTargetPath() + "default.png");
        userMapper.insert(user);
    }

    @Override
    public UserLoginVo login(User formUser) {
        QueryWrapper<User> wrapper = new QueryWrapper<>();
        wrapper.eq("username", formUser.getUsername());
        User dbUser = userMapper.selectOne(wrapper);
        if (dbUser == null || !SecurityUtil.crypto(dbUser.getSalt(), formUser.getPassword()).equals(dbUser.getPassword()))
            throw new BizException(LOGIN_ERROR.getResultCode(), LOGIN_ERROR.getResultMsg());
        //todo: generate token to user
        String token = IdUtil.simpleUUID();
        redisTemplate.opsForValue().set(TOKEN_PREFIX + token, JSONUtil.toJsonStr(dbUser), 12, TimeUnit.HOURS);
        UserLoginVo userLoginVo = new UserLoginVo(
                formUser.getUsername(),
                dbUser.getNickname(),
                token,
                dbUser.getRole(),
                dbUser.getEmail(),
                dbUser.getPhone(),
                dbUser.getGender(),
                dbUser.getAvatar()
        );
        return userLoginVo;
    }

    @Override
    public void logout(String token) {
        redisTemplate.delete(TOKEN_PREFIX + token);
    }

    @Override
    public User userInfo(User u) {
        if(u == null){
            throw new BizException("502", "请先登录");
        }
        QueryWrapper<User> wrapper = new QueryWrapper<>();
        wrapper.eq("username", u.getUsername());
        User dbUser = userMapper.selectOne(wrapper);
        dbUser.setPassword("");
        return dbUser;
    }

    @Override
    public Result<User> updateUserInfo(UserUpdateInfo userUpdateInfo) {
        QueryWrapper<User> wrapper = new QueryWrapper<>();
        wrapper.eq("username", userUpdateInfo.getUsername());
        User dbUser = userMapper.selectOne(wrapper);
        dbUser.setEmail(userUpdateInfo.getEmail());
        dbUser.setPhone(userUpdateInfo.getPhone());
        dbUser.setNickname(userUpdateInfo.getNickname());
        userMapper.updateById(dbUser);
        dbUser.setPassword("");
        return Result.success(dbUser);
    }

    @Override
    public Boolean isAuth(String token) {
        return redisTemplate.hasKey(TOKEN_PREFIX + token);
    }

    @Override
    public User getByToken(String token) {
        Object o = redisTemplate.opsForValue().get(TOKEN_PREFIX + token);
        if (o == null) {
            throw new BizException(NOT_LOGIN.getResultCode(), NOT_LOGIN.getResultMsg());
        } else {
            User usertemp = JSONUtil.toBean((String) o, User.class);
            return userInfo(usertemp);
        }
    }

    @Override
    public String uploadAvatar(User user, MultipartFile file) {
        String originalFilename = file.getOriginalFilename();
        //获取文件后缀名
        String fileSuffix = originalFilename.substring(originalFilename.lastIndexOf("."));
        //新生成文件名
        //简单使用
        String fileName = UUID.randomUUID().toString() + System.currentTimeMillis() + fileSuffix;
        String targetPath;
        try (InputStream fr = file.getInputStream()) {
            // 10年后的日期
            Date expiration = new Date(new Date().getTime() + 3600l * 1000 * 24 * 365 * 10);
            String savePath = aliyunConfig.getTargetPath() + fileName;
            GeneratePresignedUrlRequest request = new GeneratePresignedUrlRequest(aliyunConfig.getBucketName(), savePath);
            request.setExpiration(expiration);
            URL url = ossClient.generatePresignedUrl(request);

            ossClient.putObject(aliyunConfig.getBucketName(), savePath, fr);
//            targetPath = aliyunConfig.getTargetUrl() + "/" + savePath;

            targetPath = url.toString();
            QueryWrapper<User> wrapper = new QueryWrapper<>();
            wrapper.eq("username", user.getUsername());
            User dbUser = userMapper.selectOne(wrapper);
            dbUser.setAvatar(targetPath);
            userMapper.updateById(dbUser);

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return targetPath;
    }

    @Override
    public void updateAvatarUrl(User user, String avatarUrl) {
        QueryWrapper<User> wrapper = new QueryWrapper<>();
        wrapper.eq("username", user.getUsername());
        User dbUser = userMapper.selectOne(wrapper);
        dbUser.setAvatar(avatarUrl);
        userMapper.updateById(dbUser);
    }
}
