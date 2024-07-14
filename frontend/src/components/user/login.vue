<template>
    <div id="bg">
        <div id="title_bar">
          <span class="title_con">龙兴启智</span>
          <span class="title_con_para">--更懂学生的智教平台</span>
          <img id="logo" src="../../assets/loginLogo.png">
        </div>
        <div id="hengline"></div>
        <div id="main">
            <div id="title_blank"><span class="con_title_sp">欢迎登录</span></div>
            <el-form :model="form" :rules="rules" ref="formRef" class="w-[300px]">
                <el-form-item prop="username" class="form-item-up">
                <el-text class="w-150px mb-2" truncated>
                    用户名：
                </el-text>
                <el-input
                    v-model="form.username"
                    style="width: 240px"
                    placeholder="请输入用户名"
                    clearable
                    @focus="clearValidationMessage('username')"
                />
                </el-form-item>
                <el-form-item prop="password" class="form-item" >
                <el-text class="w-150px mb-2" truncated>
                    密&nbsp;&nbsp;&nbsp;码&nbsp;:&nbsp;&nbsp;   
                </el-text>
                <el-input
                    v-model="form.password"
                    style="width: 240px"
                    type="password"
                    placeholder="请输入密码"
                    show-password
                    @keyup.enter.prevent="login"
                />
                </el-form-item>
                <el-form-item class="form-item">
                <el-button round color="#1343db" class="login-btn" @click="login" :loading="loading">
                    登 录
                </el-button>
                </el-form-item>
                <el-form-item>
                <el-button  @click="drawer = true" class="register-btn" :style="{ opacity: dynamicOpacity }" >注 册</el-button>
                <el-dialog v-model="drawer" size = '100%' direction='btt'
                            :before-close="handleClose">
        
                    <register></register>
                </el-dialog>
                </el-form-item>
            </el-form>
    
        </div>
    </div>
  </template>

<script>
  import { ref, reactive} from 'vue'
  import api from "../../api"
  import { toast } from "../../utils/popup"
  import register from "@/components/user/register"
  import { ElMessageBox } from 'element-plus'
  import { useRouter } from "vue-router";
  import store from '../../store'

  export default {
    dynamicOpacity: 0.4,
    name: "login",
    components:{
      register
    },
    setup() {
      const router = useRouter()
      const form = reactive({
        username: "",
        password: "",
      });
      const drawer = ref(false)
      const rules = {
        username: [
          { required: true, message: "用户名不能为空", trigger: "focus" },
        ],
        password: [
          {
            required: true,
            message: "密码不能为空",
            trigger: "submit",
          },
          {message: "密码不能为空",
            trigger: "input",}
        ],
      };
      const clearValidationMessage = (field) => {
            // 设置该字段的验证消息为空
            form[field + 'ErrorMessage'] = ''
        }
      const formRef = ref(null)
      const loading = ref(false)
      function login() {
        formRef.value.validate((valid) => {
          if (valid) {
            loading.value = true
            if (form.username == "admin"){
              if(form.password == "admin"){
                toast("杰，别想用双admin来混我哈哈哈哈！或许你可以试试密码123456", "error")
              }else if (form.password == "123456"){
                toast("这么简单的账号密码？不存在的！换个密码试试吧", "error")
              }else{
                toast("你可不是admin！！快去注册吧！（狗头）", "error")
              }
              return
            }
            api.login(form.username, form.password).then((res) => {
              if(res.data.code == 200){
                toast("登录成功，正在跳转")
                const token = res.data.data.token; // 假设 token 在这个位置
  
                if (token) {
                  localStorage.setItem("access_token", token); // 设置 token 到 localStorage
                }
                // 调用 Vuex 中的 login action
                store.dispatch('login', res.data.data)
  
                if(res.data.data.role == 1){
                  setTimeout(() => {
                    router.push("/");
                  }, 1000)
                }else if(res.data.data.role == 2){
                  setTimeout(() => {
                    router.push("/teacherHome");
                  }, 1000)
                }else{
                  setTimeout(() => {
                    router.push("/adminHome");
                  }, 1000)
                }
              }else {
                toast(res.data.msg, "error")
              }
            }).finally(() => {
              loading.value = false
            })
          } else {
            toast("表单有误，请正确填写表单", "error")
          }
        })
      }
      const handleClose = (done) => {
        ElMessageBox.confirm('确定要取消注册？')
            .then(() => {
              done()
            })
            .catch(() => {
            })
      }
  
      return {
        form,
        login,
        rules,
        formRef,
        drawer,
        handleClose,
        clearValidationMessage
      }
    }
  }
  </script>
  
  <style scoped>
    #main{
        text-align: center;
        background-color: #fff;
        border-radius: 20px;
        width: 400px;
        height: 300px;
        margin: auto;
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
    }
    #logo{
        margin-left: 70%;
        width: 165px;
        height: 55px;
    }
    #app{
      margin-top: 0;
    }
    #bg{
        width: 100%;
      min-height: 100vh;
        background-color: #6495ed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
    }
    #title_blank{
        width: 100%;
        height: 60px;
        background-color: #1343db;
        border-top-left-radius: 20px;
        border-top-right-radius: 20px;
        display: flex;
        align-items: center;
    }
    #title_bar{
        background-color: white;
      display: flex; /* 使用 Flexbox 布局 */
      justify-content: space-between; /* 在两端对齐，中间自动分配空间 */
      align-items: center; /* 垂直居中对齐 */
    }
    #hengline{
        margin-top: 5px;
        background-color: white;
        height: 3px;
    }
    .title_con{
        margin-left: 30px;
        color: black;
        font-size: 40px;
        font-family: 隶书;
    }
    .title_con_para{
        color: black;
        font-size: 25px;
        font-family: 隶书;
      margin-right: 10px;
    }
    .con_title_sp{
        color: #fff;
        display: flex;
        align-items: center;
        margin-left: 32%;
        font-size: 30px;
        font-family: 隶书;
    }
    .form-item {
        margin-left: 50px;
        margin-right: 50px;
        display: flex;
        align-items: center;
    }
    .form-item-up {
        margin-top: 40px;
        margin-left: 50px;
        margin-right: 50px;
        display: flex;
        align-items: center;
    }
    .login-btn {
        width: 100%;
    }
    .login-btn:hover {
        transform: scale(1.1,1.1);
    }
    .register-btn {
        width: 80%;
        margin-left: 50px;
        margin-right: 50px;
        border-radius: 20px;
    }
    .register-btn:hover {
        transform: scale(1.1,1.1);
    }

  </style>