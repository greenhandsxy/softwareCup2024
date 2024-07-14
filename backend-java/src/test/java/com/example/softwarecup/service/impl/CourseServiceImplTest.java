package com.example.softwarecup.service.impl;

import com.example.softwarecup.service.CourseService;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

/**
 * @author SaoE
 * @date 2024/4/20 17:00
 */
@RunWith(SpringRunner.class)
@SpringBootTest
class CourseServiceImplTest {
    @Autowired
    private CourseService courseService;

//    @org.junit.jupiter.api.Test
//    void getAllCourses() {
//        List<Course> allCourses = courseService.getAllCourses();
//        for(Course c : allCourses){
//            System.out.println(c.getCourseName());
//            System.out.println(c.getCourseDescription());
//        }
//    }

}