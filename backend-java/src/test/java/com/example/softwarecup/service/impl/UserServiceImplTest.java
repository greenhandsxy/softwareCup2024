package com.example.softwarecup.service.impl;

import com.example.softwarecup.service.UserService;
import org.junit.jupiter.api.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

/**
 * @author SaoE
 * @date 2024/4/23 15:15
 */
@RunWith(SpringRunner.class)
@SpringBootTest
class UserServiceImplTest {

    @Autowired
    private UserService userService;

    @Test
    public void updateUserInfo() {
//        userService.updateUserInfo(new UserUpdateInfo("123456", "111", "111", "222"));
    }
}