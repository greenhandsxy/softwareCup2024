package com.example.softwarecup.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.softwarecup.exception.BizException;
import com.example.softwarecup.mapper.CourseChosenMapper;
import com.example.softwarecup.mapper.CourseMapper;
import com.example.softwarecup.pojo.Course;
import com.example.softwarecup.pojo.CourseChosen;
import com.example.softwarecup.service.CourseService;
import com.example.softwarecup.vo.CourseStudyInfo;
import com.example.softwarecup.vo.StudentStudyInfo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static com.example.softwarecup.exception.ExceptionEnum.*;

/**
 * @author SaoE
 * @date 2024/4/19 12:59
 */
@Service
public class CourseServiceImpl extends ServiceImpl<CourseMapper, Course>  implements CourseService {

    @Autowired
    private CourseMapper courseMapper;

    @Autowired
    private CourseChosenMapper courseChosenMapper;

    @Override
    public List<Course> getAllCourses() {
        List<Course> courses = courseMapper.selectAll();
        return courses;
    }

    @Override
    public List<Course> getCourseByType(String courseType) {
        List<Course> courses = courseMapper.selectCourseByType(courseType);
        return courses;
    }

    @Override
    public Course getCourseDetail(String courseName) {
        return courseMapper.getCourseDetail(courseName);
    }

    @Override
    public CourseChosen studentAddCourse(String courseName, String studentName) {
        String teacherName = courseMapper.getCourseDetail(courseName).getTeacherName().replace("\r", "");
        for (CourseChosen courseChosen : courseChosenMapper.allChosenCourse(studentName)) {
            if (courseChosen.getCourseName().equals(courseName)) {
                throw new BizException(Course_Has_Been_Chosen.getResultCode(), Course_Has_Been_Chosen.getResultMsg());
            }
        }
        CourseChosen courseChosen = new CourseChosen(studentName, courseName, teacherName);
        courseChosenMapper.insert(courseChosen);
        return courseChosen;
    }

    @Override
    public void studentDeleteCourse(String courseName, String studentName) {
        for (CourseChosen courseChosen : courseChosenMapper.allChosenCourse(studentName)) {
            if (courseChosen.getCourseName().equals(courseName)) {
                courseChosenMapper.deleteChosenCourse(studentName, courseName);
                return;
            }
        }
        throw new BizException(Course_Has_Not_Been_Chosen.getResultCode(), Course_Has_Not_Been_Chosen.getResultMsg());

    }

    @Override
    public List<CourseChosen> studentGetCourseStudyInfo(String studentName) {
        List<CourseChosen> courseChosens = courseChosenMapper.studentChosenCourseInfo(studentName);
        if (courseChosens.isEmpty()){
            throw new BizException(NOT_SELECT_ANY_COURSES.getResultCode(), NOT_SELECT_ANY_COURSES.getResultMsg());
        }
        return courseChosens;
    }

    @Override
    public void updateStudentPredictScore(String studentName, String courseName, Integer score) {
        courseChosenMapper.updateStudentPredictScore(studentName, courseName, score);
    }

    @Override
    public void teacherAddCourse(Course newCourse) {
        courseMapper.teacherAddCourse(newCourse.getCourseId(),
                newCourse.getCourseName(),
                newCourse.getPrerequisites(),
                newCourse.getCourseDescription(),
                newCourse.getCourseType(),
                newCourse.getTeacherName());


    }

    @Override
    public List<CourseStudyInfo> teacherGetCourseStudyInfo(String teacherName) {
        List<CourseChosen> courseChosens = courseChosenMapper.teacherChosenCourseInfo(teacherName);
        Map<String, CourseStudyInfo> courseStudyInfoMap = new HashMap<>();

        for (CourseChosen courseChosen : courseChosens) {
            String courseName = courseChosen.getCourseName();

            // 如果Map中还没有该课程信息，则创建新的CourseStudyInfo对象
            CourseStudyInfo courseStudyInfo = courseStudyInfoMap.computeIfAbsent(courseName, k -> new CourseStudyInfo(k));

            // 更新CourseStudyInfo的选课人数（假设CourseChosen中没有直接的选课人数，需要统计）
            courseStudyInfo.setStudentNum(courseStudyInfo.getStudentNum() == null ? 1 : courseStudyInfo.getStudentNum() + 1);

            // 创建StudentStudyInfo并添加到CourseStudyInfo的列表中
            StudentStudyInfo studentStudyInfo = new StudentStudyInfo(
                    courseName,
                    courseChosen.getStudentName(),
                    courseChosen.getStudyTimeSum(),
                    courseChosen.getStudyDay(),
                    courseChosen.getTodayStudyTime(),
                    courseChosen.getTwoWeekStudy(),
                    courseChosen.getScore()
            );
            courseStudyInfo.getStudentStudyInfoList().add(studentStudyInfo);
        }

        // 将Map的值转换为List并返回
        return new ArrayList<>(courseStudyInfoMap.values());
    }

    @Override
    public List<Course> getCourseByTeacherName(String teacherName) {
        QueryWrapper<Course> wrapper = new QueryWrapper<>();
        wrapper.eq("teacher_name", teacherName)
                .or()
                .eq("teacher_name", teacherName + "\r");
        return courseMapper.selectList(wrapper);
    }
}
