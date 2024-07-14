package com.example.softwarecup.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.example.softwarecup.dto.UserUpdateInfo;
import com.example.softwarecup.pojo.User;
import com.example.softwarecup.tools.Result;
import com.example.softwarecup.vo.UserLoginVo;
import org.springframework.web.multipart.MultipartFile;

/**
 * @author SaoE
 * @date 2024/4/18 10:49
 */
public interface UserService extends IService<User>{
    String COOKIE_NAME_TOKEN = "token";
    /**
     * token前缀
     */
    String TOKEN_PREFIX = "cup:token:";

    void register(User user);

    UserLoginVo login(User user);

    void logout(String token);

    User userInfo(User u);

    Result<User> updateUserInfo(UserUpdateInfo userUpdateInfo);

    Boolean isAuth(String token);

    User getByToken(String token);

    String uploadAvatar(User user, MultipartFile file);

    void updateAvatarUrl(User user, String avatarUrl);
}
