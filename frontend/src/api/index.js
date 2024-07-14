import path  from "./path"
import axios from "../utils/request";

const api = {
    //-----------------------------用户接口-----------------------------------
    //用户登录
    login(username, password){
        return axios.post(path.baseUrl + path.login, null, {
            params:{
                username: username,
                password: password
            },
            headers: {
                "Content-Type":"application/json;charset=utf-8"
            },
        })
    },

    register(user){
        return axios.post(path.baseUrl + path.register, {
            username: user.username,
            password: user.password,
            email: user.email,
            phone: user.phone,
            gender: user.gender,
            role: user.role
        }
        )
    },

    logout(){
        return axios.get(path.baseUrl + path.logout, {
            params:{
                token: localStorage.getItem("access_token")
            }
        })
    },

    updateUserInfo(userUpdateInfo){
        return axios.post(path.baseUrl + path.updateUserInfo, {
            username: userUpdateInfo.username,
            nickname: userUpdateInfo.nickname,
            email: userUpdateInfo.email,
            phone: userUpdateInfo.phone,
            }
        )
    },


    //查看用户信息
    getUserInfo(){
        return axios.get(path.baseUrl + path.userInfo, {
            params:{
                token: localStorage.getItem("access_token")
            }
        })
    },

    //上传用户头像
    uploadAvatar(formData){
        return axios.post(path.baseUrl + path.uploadAvatar, formData, {
            headers: {
                "Content-Type":"multipart/form-data"
            },
        })
    },

    updateAvatarUrl(avatarUrl){
        return axios.post(path.baseUrl + path.updateAvatarUrl, null, {
            params:{
                avatarUrl: avatarUrl,
                token: localStorage.getItem("access_token")
            }
        })
    },



    //--------------------------课程相关接口------------------------------------
    //获取所有课程
    getCourses(pageInfo, courseType){
        return axios.post(path.baseUrl + path.getAllCourses,{
            pageNum: pageInfo.pageNum,
            pageSize: pageInfo.pageSize},
            {
                params:{
                    courseType: courseType

                }
        })
    },

    //获取所有课程类别
    getAllCourseType(){
        return axios.get(path.baseUrl + path.getAllCourseType)
    },

    //根据课程类别获取课程
    getCourseByType(type, pageInfo){
        return axios.post(path.baseUrl + path.getCourseByType, {
            type: type,
            pageNum: pageInfo.pageNum,
            pageSize: pageInfo.pageSize
        })
    },

    //获取课程详情
    getCourseDetail(courseName){
        return axios.get(path.baseUrl + path.courseDetail, {
            params:{
                courseName: courseName
            }
            })
    },

    //---------------------------学生相关接口------------------------------------
    selectCourse(courseName){
        return axios.get(path.baseUrl + path.selectCourse, {
            params:{
                courseName: courseName,
                token: localStorage.getItem("access_token")
            }
        })
    },
    getCourseStudyInfo(){
        return axios.get(path.baseUrl + path.getCourseStudyInfo, {
            params:{
                token: localStorage.getItem("access_token")
            }
        })
    },
    stuDeleteCourse(courseName){
        return axios.get(path.baseUrl + path.stuDeleteCourse, {
            params:{
                courseName: courseName,
                token: localStorage.getItem("access_token")
            }
        })
    },
    updateStudentPredictScore(courseName, score){
        return axios.get(path.baseUrl + path.updateStudentPredictScore, {
            params:{
                courseName: courseName,
                score: score,
                token: localStorage.getItem("access_token")
            }
        })
    },

    //---------------------------教师相关接口------------------------------------
    teaGetCourses(){
        return axios.get(path.baseUrl + path.teaGetCourses, {
            params:{
                token: localStorage.getItem("access_token")
            }
        })
    },

    teaGetCourseStudyInfo(){
        return axios.get(path.baseUrl + path.teaGetCourseStudyInfo, {
            params:{
                token: localStorage.getItem("access_token")
            }
        })
    },
    teaReleaseCourse(newCourseInfo){
        return axios.post(path.baseUrl + path.teaReleaseCourse, {
            courseId: newCourseInfo.courseId,
            courseName: newCourseInfo.courseName,
            courseType: newCourseInfo.courseType,
            prerequisites: newCourseInfo.prerequisites,
            courseDescription: newCourseInfo.courseDescription,
        }, {
            params:{
                token: localStorage.getItem("access_token")
            }
        })
    }

}

export default api