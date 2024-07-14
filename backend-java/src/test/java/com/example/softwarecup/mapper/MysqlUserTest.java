package com.example.softwarecup.mapper;

import com.example.softwarecup.service.UserService;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

/**
 * @author SaoE
 * @date 2024/4/18 11:41
 */

//@EnableAutoConfiguration(exclude={DataSourceAutoConfiguration.class})
@RunWith(SpringRunner.class)
@SpringBootTest
//@RunWith(SpringJUnit4ClassRunner.class)
public class MysqlUserTest {

//    @Autowired
//    private UserMapper userMapper;

    @Autowired
    private UserService userService;

//    @Test
//    public void testSelect() {
//        System.out.println(("----- selectAll method test ------"));
//        List<User> userList = userMapper.selectList(null);
//        Assertions.assertEquals(5, userList.size());
//        userList.forEach(System.out::println);
//    }


    @Test
    public void testInsert() {
//        User user = new User();
//        System.out.println(user.getCreate_time());
//        user.setUsername("test");
//        user.setGender(Boolean.TRUE);
//        user.setPhone("16712866996");
//        user.setPassword("tanyongfeng");
//        user.setSalt("md555555");
//        user.setRole(1);
//        userService.register(user);
//        Assertions.assertNotNull(user.getCreate_time());
//        String filePath = "D:\\A_MASTER\\softwareCup\\src\\test\\java\\com\\example\\softwarecup\\mapper\\teacher.txt"; // Replace 'path_to_your_teacher.txt' with the actual file path
//
//        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
//            String line;
//            while ((line = reader.readLine()) != null) {
//                User user = new User();
//                user.setUsername(line);
//                user.setPassword("666666");
//                user.setSalt("md555555");
//                user.setRole(2);
//                userService.register(user);
//            }
//        } catch (IOException e) {
//            e.printStackTrace();
//        }
    }

    @Test
    public void login(){
//        User user = new User();
//        user.setUsername("于泽");
//        user.setPassword("666666");
//        userService.login(user);
    }

    @Test
    public void update(){

    }

}
